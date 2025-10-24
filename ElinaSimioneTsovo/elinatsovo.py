#!/usr/bin/env python3
# rpa_scraper_filtrado.py
"""
Scraper RPA com logs em console e arquivo:
 - Baixa todos os ficheiros .txt da página
 - Extrai campos: nome, email, contacto, estado civil, salario liquido
 - Salva CSV na mesma pasta do script
 - Regista logs no console e em arquivo rpa_scraper.log
"""

import re
import time
import csv
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIGURACÕES ==========
URL = "http://rpa.xidondzo.com"
DOWNLOAD_DIR = Path.cwd()
OUTPUT_CSV = DOWNLOAD_DIR / "R1000_filtrado.csv"
LOG_FILE = DOWNLOAD_DIR / "rpa_scraper.log"
TIMEOUT = 60


FIELD_PATTERNS = {
    "nome": r"Nome[:\s]*([^\n]+)",
    "contacto": r"Contacto\s*/\s*Tel[:\s]*([\d\-\+\s]+)",
    "email": r"E-?mail[:\s]*([\w\.-]+@[\w\.-]+)",
    "estado_civil": r"Estado Civil[:\s]*([A-Za-zÀ-ÿ]+)",
    "salario_liquido": r"Sal[aá]rio\s+L[ií]quido[:\s]*([0-9\.,]+)",
}

# ========== LOGS ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ========== FUNÇÕES ==========
def normalize_number(text: str) -> str:
    """Converte '16.050,00' -> '16050.00'"""
    if not text:
        return ""
    t = text.strip().replace(" ", "").replace(".", "").replace(",", ".")
    return t

def wait_for_file(path: Path, timeout: int = TIMEOUT) -> bool:
    end_time = time.time() + timeout
    while time.time() < end_time:
        if path.exists() and path.stat().st_size > 0:
            size1 = path.stat().st_size
            time.sleep(0.5)
            size2 = path.stat().st_size
            if size1 == size2:
                return True
        time.sleep(0.5)
    return False

def find_downloaded_txt(download_dir: Path):
    files = [p for p in download_dir.iterdir() if p.is_file() and p.suffix == ".txt"]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None

def extrair_registros(texto: str):
    blocos = re.split(r"---\s*Registro:?", texto, flags=re.IGNORECASE)
    registros = []
    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue
        reg = {}
        for campo, patt in FIELD_PATTERNS.items():
            try:
                m = re.search(patt, bloco, flags=re.IGNORECASE | re.MULTILINE)
                valor = m.group(1).strip() if m else ""
                if campo == "salario_liquido":
                    valor = normalize_number(valor)
                reg[campo] = valor
            except Exception as e:
                logging.error(f"Erro ao extrair campo {campo}: {e}")
                reg[campo] = ""
        
        if reg.get("email") and reg.get("contacto"):
            registros.append(reg)
        else:
            logging.warning(f"Registro ignorado por falta de email ou contacto: {reg.get('nome','<sem nome>')}")
    return registros

def salvar_csv(dados, caminho):
    if not dados:
        logging.warning("Nenhum dado para salvar.")
        return
    fieldnames = list(FIELD_PATTERNS.keys())
    try:
        with caminho.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in dados:
                writer.writerow({k: item.get(k, "") for k in fieldnames})
        logging.info(f"CSV salvo: {caminho}")
    except Exception as e:
        logging.error(f"Erro ao salvar CSV: {e}")

# ========== NAVEGANDO NO CHOME ==========
def setup_chrome(download_dir: Path):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        prefs = {
            "download.default_directory": str(download_dir.resolve()),
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        logging.info("ChromeDriver iniciado com sucesso.")
        return driver
    except WebDriverException as e:
        logging.error(f"Erro ao iniciar ChromeDriver: {e}")
        raise

def baixar_txt(driver, url: str, download_dir: Path):
    try:
        driver.get(url)
        time.sleep(2)
        anchors = driver.find_elements(By.TAG_NAME, "a")
        links_txt = [a for a in anchors if (a.get_attribute("href") or "").lower().endswith(".txt")]
        ficheiros = []
        for link in links_txt:
            href = link.get_attribute("href")
            logging.info(f"A descarregar: {href}")
            driver.execute_script("arguments[0].click();", link)
            end_time = time.time() + TIMEOUT
            while time.time() < end_time:
                cand = find_downloaded_txt(download_dir)
                if cand and wait_for_file(cand, timeout=5) and cand not in ficheiros:
                    ficheiros.append(cand)
                    break
                time.sleep(1)
        return ficheiros
    except Exception as e:
        logging.error(f"Erro ao baixar ficheiros: {e}")
        return []

# ========== FLUXO PRINCIPAL ==========
def main():
    driver = None
    try:
        driver = setup_chrome(DOWNLOAD_DIR)
        ficheiros_txt = baixar_txt(driver, URL, DOWNLOAD_DIR)
        if not ficheiros_txt:
            logging.warning("Nenhum ficheiro baixado.")
            return

        todos = []
        for f in ficheiros_txt:
            try:
                texto = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                try:
                    texto = f.read_text(encoding="latin-1", errors="ignore")
                except Exception as e:
                    logging.error(f"Erro ao ler ficheiro {f.name}: {e}")
                    continue
            registros = extrair_registros(texto)
            todos.extend(registros)

        salvar_csv(todos, OUTPUT_CSV)
        logging.info(f"Total de registros extraídos: {len(todos)}")
    except Exception as e:
        logging.error(f"Erro no fluxo principal: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("ChromeDriver fechado.")

if __name__ == "__main__":
    main()
