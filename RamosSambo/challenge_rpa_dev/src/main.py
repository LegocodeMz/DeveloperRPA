# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from warnings import catch_warnings

from selenium.webdriver.common.by import By
from config import Config
from logger import setup_logger
from extractor import extrair_informacoes
from urllib.parse import urljoin
from csv_writer import write_to_csv
from driver_mananger import get_driver
import requests

def main():
    logger = setup_logger()
    logger.info("=== Início do processo de automação ===")

    driver = get_driver(headless=Config.HEADLESS)

    try:
        driver.get(Config.BASE_URL)
        linhas = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        logger.info(f"🔍 Encontradas {len(linhas)}  linhas na tabela.\n")

        data = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            link_elemento = colunas[5].find_element(By.TAG_NAME, "a")
            link_txt = link_elemento.get_attribute("href")

            # Garante URL completa
            url_arquivo = urljoin(Config.BASE_URL, link_txt)

            logger.info(f"📥 Processando url")

            # === Baixar e processar o conteúdo do .txt ===
            response = requests.get(url_arquivo)
            conteudo_txt = response.text

            # Exemplo de extração simples: procurar palavras-chave
            info_extraida = extrair_informacoes(conteudo_txt)
            if info_extraida:
                data.append(info_extraida)

        csv_file = write_to_csv(data, Config.OUTPUT_PATH)
        logger.info(f"Dados salvos em {csv_file}")
    except Exception as e:
        logger.info(f"Exception {e}")
    finally:
        driver.quit()
        logger.info("Navegador encerrado.")

if __name__ == "__main__":
    main()
