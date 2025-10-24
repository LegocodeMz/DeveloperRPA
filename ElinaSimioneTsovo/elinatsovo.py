import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# ===================== CONFIGURAÇÕES =====================
URL = "http://rpa.xidondzo.com"
OUTPUT_FILE = "dados_j_output.csv"
FILE_NAME = "R1000.txt"
CAMPOS_OBRIGATORIOS = ["nome", "email", "contacto", "estado_civil", "salario_liquido"]

LOCATORS = {
    "DOWNLOAD_LINK": (By.CSS_SELECTOR, "a.btn-success[href$='.txt']"),
    "FILE_TYPE_HINT": (By.TAG_NAME, "body")
}



# ===================== FUNÇÃO PRINCIPAL =====================
def executar_scraper():
    print("INÍCIO DO SCRAPER")
    driver = None
    
    try:
                
        # ===================== DEFININDO O DOWNLOAD =====================
        download_path = os.path.abspath(os.path.dirname(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"download.default_directory": download_path}

        # ===================== INICIANDO O CHROME =====================

        options.add_experimental_option("prefs", prefs)
        print("Inicializando o Chrome Driver...")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(15)
        wait = WebDriverWait(driver, 10)

        
        print(f"[ACESSO] Navegando para {URL}")
        driver.get(URL)
        print("[SUCESSO] Página carregada.")




        # ===================== IDENTIFICAR O TIPO PELO HINT =====================
        hint_element = driver.find_element(*LOCATORS["FILE_TYPE_HINT"])
        hint_text = hint_element.text.lower()
        print(f"[HINT] Texto encontrado na página: '{hint_text}'")

        if 'csv' in hint_text:
            tipo_identificado = "CSV (Identificado por Texto)"
        elif 'txt' in hint_text:
            tipo_identificado = "TXT (Identificado por Texto)"
        elif 'json' in hint_text:
            tipo_identificado = "JSON (Identificado por Texto)"
        else:
            tipo_identificado = f"Hint genérico: {hint_text}"

        print(f"[INFO] Tipo provável: {tipo_identificado}")



        # ===================== BAIXAR FICHEIRO =====================
        print("[AÇÃO] Clicando para baixar o ficheiro...")
        download_btn = driver.find_element(*LOCATORS["DOWNLOAD_LINK"])
        download_btn.click()

        
        download_path = os.path.abspath(os.path.dirname(__file__))
        caminho = os.path.join(download_path, FILE_NAME)
        time.sleep(5)  

        if not os.path.exists(caminho):
            print(f"\n[FALHA] Ficheiro '{FILE_NAME}' não encontrado após o clique.")
            return False

        print(f"\n[SUCESSO] Ficheiro '{FILE_NAME}' descarregado em:\n{download_path}")

        # ===================== IDENTIFICAR FORMATO =====================
        tipo = "Desconhecido"
        if FILE_NAME.lower().endswith('.txt') or 'txt' in hint_text:
            tipo = "TXT"
        elif FILE_NAME.lower().endswith('.csv') or 'csv' in hint_text:
            tipo = "CSV"
        print(f"[INFO] Formato final identificado: {tipo}")



        # ===================== LER E EXTRAIR DADOS =====================
        if tipo == "TXT":
            dados_filtrados = []
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    
                    if ',' in linha:
                        colunas = linha.split(',')
                    else:
                        colunas = linha.split('\t')

                   
                    registro = {}
                    for item in colunas:
                        if ':' in item:
                            chave, valor = item.split(':', 1)
                            chave = chave.strip().lower()
                            valor = valor.strip()
                            if chave in CAMPOS_OBRIGATORIOS:
                                registro[chave] = valor
                    if registro:
                        dados_filtrados.append(registro)

            # ===================== SALVAR CSV =====================
            if dados_filtrados:
                with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=CAMPOS_OBRIGATORIOS)
                    writer.writeheader()
                    for registro in dados_filtrados:
                        
                        linha = {campo: registro.get(campo, "") for campo in CAMPOS_OBRIGATORIOS}
                        writer.writerow(linha)
                print(f"[SUCESSO] Dados filtrados salvos em {OUTPUT_FILE}")
            else:
                print("[AVISO] Nenhum dado válido encontrado no ficheiro.")

    except WebDriverException as e:
        print(f"\n[ERRO CRÍTICO DRIVER] {e}")
    except NoSuchElementException as e:
        print(f"\n[ERRO FATAL LOCALIZADOR] {e}")
    except TimeoutException:
        print("\n[ERRO TEMPO] Timeout.")
    except Exception as e:
        print(f"\n[ERRO GERAL] {e}")
    finally:
        if driver:
            driver.quit()
            print("[FIM] Driver encerrado.")

# ===================== EXECUTANDO O RPA =====================
if __name__ == "__main__":
    executar_scraper()
