from urllib.parse import urljoin
import requests
from config import Config
from selenium.webdriver.common.by import By
from util import RequestResult

def get_table_lines(driver):
    driver.get(Config.BASE_URL)
    lines = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    return lines

def get_file_url(line):
    columns = line.find_elements(By.TAG_NAME, "td")
    link_element = columns[5].find_element(By.TAG_NAME, "a")
    link_txt = link_element.get_attribute("href")

    # Garante URL completa
    file_url = urljoin(Config.BASE_URL, link_txt)
    return file_url

def get_file_txt(file_url: str) -> RequestResult:
    try:
        response = requests.get(file_url, timeout=Config.TIMEOUT)

        if not response.ok:
            return RequestResult(False, error=f"Erro de requisicao {response.status_code} ao baixar arquivo: {file_url}")

        if not response.content or len(response.content) == 0:
            return RequestResult(False, error="Arquivo vazio")

        text = response.text
        try:
            text = text.encode("latin1").decode("utf-8")
            pass
        except UnicodeDecodeError:
            return RequestResult(False, error="Falha ao decodificar UTF-8 (possível arquivo corrompido)")

        if not text:
            return RequestResult(False, error="Arquivo só contém espaços em branco")

        return RequestResult(True, text=text)

    except requests.exceptions.RequestException as e:
        return RequestResult(False, error=str(e))
