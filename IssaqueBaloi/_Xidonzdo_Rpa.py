from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import re
import csv
import unittest
import tempfile

def handle_popups(driver, wait):
    """Detecta e gere pop-ups no website, permitindo interação manual se necessário."""
    try:
        popup_selectors = [
            '//div[contains(text(), "top-up")]',
            '//div[contains(text(), "recarregar")]',
            '//button[contains(text(), "OK")]',
            '//button[contains(text(), "Fechar")]',
            '//button[contains(text(), "Continuar")]',
            '//a[contains(text(), "Prosseguir")]'
        ]
        for selector in popup_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                print(f"Pop-up detectado: {selector}")
                try:
                    elements[0].click()
                    print("Pop-up fechado automaticamente.")
                    time.sleep(2)
                except Exception:
                    print("Pop-up requer intervenção manual.")
                    input("Pressiona Enter após fechar o pop-up manualmente...")
                return True
    except Exception as e:
        print(f"Erro ao verificar pop-ups: {str(e)}")
    return False

def identificar_formato(caminho_ficheiro):
    """Verifica se o ficheiro é .txt."""
    _, extensao = os.path.splitext(caminho_ficheiro)
    if extensao.lower() == ".txt":
        print("✅ Ficheiro no formato correto (.txt)")
        return True
    else:
        print(f"⚠️ Formato incorreto: {extensao}. Esperado: .txt")
        return False

def ler_e_extrair_campos(caminho_ficheiro):
    """Lê o ficheiro .txt e extrai os campos Nome, Email, Contacto, Estado Civil e Salário Líquido."""
    campos_extraidos = []
    try:
        with open(caminho_ficheiro, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        print(f"Erro ao ler ficheiro: {str(e)}")
        return campos_extraidos

    registos = re.split(r"--- END Registro: .*? ---", conteudo)
    for reg in registos:
        if not reg.strip():
            continue

        nome = re.search(r"Nome:\s*(.*)", reg)
        email = re.search(r"E-mail:\s*(.*)", reg)
        contacto = re.search(r"Contacto\s*/\s*Tel:\s*(.*)", reg)
        estado_civil = re.search(r"Estado Civil:\s*(.*)", reg)
        salario = re.search(r"Salário Líquido:\s*([\d.,]+)", reg)

        if nome and email and contacto and estado_civil and salario:
            campos_extraidos.append({
                "Nome": nome.group(1).strip(),
                "Email": email.group(1).strip(),
                "Contacto": contacto.group(1).strip(),
                "Estado Civil": estado_civil.group(1).strip(),
                "Salário Líquido": salario.group(1).strip()
            })
    return campos_extraidos

def validar_dados(lista_dados):
    """Valida campos de email, contacto e salário."""
    dados_validos = []
    for d in lista_dados:
        email_valido = re.match(r"[^@]+@[^@]+\.[^@]+", d["Email"])
        contacto_valido = re.match(r"8[23456789]-\d{3}-\d{3}", d["Contacto"])
        salario_valido = re.match(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?", d["Salário Líquido"])

        if email_valido and contacto_valido and salario_valido:
            d["Validação"] = "✅ Válido"
        else:
            d["Validação"] = "⚠️ Inválido"
        dados_validos.append(d)
    return dados_validos

def transformar_dados(lista_dados):
    """Normaliza e transforma dados para CSV."""
    dados_transformados = []
    for d in lista_dados:
        nome = d["Nome"].title()
        email = d["Email"].lower()
        contacto = re.sub(r"[^0-9]", "", d["Contacto"])
        estado_civil = d["Estado Civil"].capitalize()

        try:
            # Remove separadores de milhar e converte decimal para ponto
            salario = d["Salário Líquido"]
            salario = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", salario)  # remove pontos/vírgulas de milhar
            salario = salario.replace(",", ".")  # decimal sempre com ponto
            salario = "{:.2f}".format(float(salario))
        except ValueError:
            salario = "0.00"

        dados_transformados.append({
            "Nome": nome,
            "Email": email,
            "Contacto": contacto,
            "Estado Civil": estado_civil,
            "Salário Líquido (MZN)": salario
        })
    return dados_transformados

def gerar_csv(dados_transformados, caminho_saida):
    """Cria ficheiro CSV com codificação UTF-8 BOM e delimitador ponto e vírgula."""
    cabecalhos = ["Nome", "Email", "Contacto", "Estado Civil", "Salário Líquido (MZN)"]

    try:
        with open(caminho_saida, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=cabecalhos, delimiter=";")
            writer.writeheader()
            for row in dados_transformados:
                writer.writerow(row)
        print(f"✅ Ficheiro CSV criado com sucesso em:\n   {caminho_saida}")
    except Exception as e:
        print(f"Erro ao gerar CSV: {str(e)}")

def download_document(download_dir=None):
    """Acede ao site, descarrega ficheiro, processa e gera CSV."""
    if download_dir is None:
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        print("A aceder ao website: rpa.xidondzo.com ...")
        driver.get("https://www.rpa.xidondzo.com")

        handle_popups(driver, wait)

        print("A procurar o link para download do GenericReport.txt...")
        download_link = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="docs/GenericReport.txt"]'))
        )
        download_link.click()
        print("Download iniciado...")
        time.sleep(3)

        caminho_ficheiro = os.path.join(download_dir, "GenericReport.txt")

        if not os.path.exists(caminho_ficheiro) or os.path.getsize(caminho_ficheiro) == 0:
            print(f"⚠️ Ficheiro não encontrado ou vazio: {caminho_ficheiro}")
            return

        if identificar_formato(caminho_ficheiro):
            dados = ler_e_extrair_campos(caminho_ficheiro)
            if not dados:
                print("⚠️ Nenhum dado extraído do ficheiro.")
                return
            dados_validados = validar_dados(dados)
            dados_transformados = transformar_dados(dados_validados)
            caminho_saida = os.path.join(download_dir, "Relatorio_Filtrado.csv")
            gerar_csv(dados_transformados, caminho_saida)

            # Validação simples do CSV
            if os.path.exists(caminho_saida):
                with open(caminho_saida, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f, delimiter=";")
                    rows = list(reader)
                    if len(rows) != len(dados_transformados):
                        print("⚠️ Verificação do CSV: Número de linhas incorreto.")
            else:
                print("⚠️ Verificação do CSV: Ficheiro não encontrado.")

    except TimeoutException:
        print("❌ Link para download não encontrado a tempo.")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {str(e)}")
    finally:
        driver.quit()

# --------------------- TESTES UNITÁRIOS --------------------- #
class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.sample_content = """
Nome: João Silva
E-mail: joao@example.com
Contacto / Tel: 82-123-456
Estado Civil: Solteiro
Salário Líquido: 10,000.00
--- END Registro: 1 ---

Nome: Maria Oliveira
E-mail: maria@example.com
Contacto / Tel: 84-789-012
Estado Civil: Casada
Salário Líquido: 15.500,50
--- END Registro: 2 ---
"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.temp_file.write(self.sample_content.encode('utf-8'))
        self.temp_file.close()
        self.temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv').name

    def tearDown(self):
        os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_csv):
            os.unlink(self.temp_csv)

    def test_identificar_formato(self):
        self.assertTrue(identificar_formato(self.temp_file.name))
        temp_wrong = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_wrong.close()
        self.assertFalse(identificar_formato(temp_wrong.name))
        os.unlink(temp_wrong.name)

    def test_ler_e_extrair_campos(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        self.assertEqual(len(dados), 2)
        self.assertEqual(dados[0]['Nome'], 'João Silva')
        self.assertEqual(dados[1]['Salário Líquido'], '15.500,50')

    def test_validar_dados(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        self.assertEqual(dados_validados[0]['Validação'], '✅ Válido')
        self.assertEqual(dados_validados[1]['Validação'], '✅ Válido')

    def test_transformar_dados(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        dados_transformados = transformar_dados(dados_validados)
        self.assertEqual(dados_transformados[0]['Salário Líquido (MZN)'], '10000.00')
        self.assertEqual(dados_transformados[1]['Salário Líquido (MZN)'], '15500.50')

    def test_gerar_csv(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        dados_transformados = transformar_dados(dados_validados)
        gerar_csv(dados_transformados, self.temp_csv)
        self.assertTrue(os.path.exists(self.temp_csv))
        with open(self.temp_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            rows = list(reader)
            self.assertEqual(rows[0]['Salário Líquido (MZN)'], '10000.00')
            self.assertEqual(rows[1]['Salário Líquido (MZN)'], '15500.50')

# --------------------- EXECUÇÃO --------------------- #
if __name__ == "__main__":
    download_document()
    print("\nExecutando testes de validação...")
    unittest.main(argv=[''], verbosity=2, exit=False)
    print("\n✅ Execução concluída. Pressione Enter para fechar o terminal...")
    input()
