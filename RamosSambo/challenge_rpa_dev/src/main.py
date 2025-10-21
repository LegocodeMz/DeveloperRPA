from config import Config
from logger import setup_logger
from extractor import extract_info
from csv_writer import write_to_csv
from driver_mananger import get_driver
from navigation_files_access import get_table_lines, get_file_url, get_file_txt
from validator import validate_info

def main():
    logger = setup_logger()
    logger.info("=== Início do processo de automação ===")

    driver = get_driver(headless=Config.HEADLESS)

    try:
        table_lines = get_table_lines(driver)
        logger.info(f"Encontradas {len(table_lines)}  linhas na tabela.")

        data = []
        for line in table_lines:
            file_url = get_file_url(line)

            logger.info(f"Processando url {file_url}")
            result = get_file_txt(file_url)

            if not result.success:
                logger.error(result.error)
                continue

            extracted_info = extract_info(result.text)

            if not extracted_info:
                logger.error(f"Nenhum dos campos solicitados foi encontrado no arquivo obtido na url: {file_url}")
                continue

            validation_result = validate_info(extracted_info)

            if not validation_result.is_valid:
                logger.warning(validation_result.errors)

            data.append(extracted_info)

        csv_file = write_to_csv(data, Config.OUTPUT_PATH)
        logger.info(f"Dados salvos em {csv_file}")
    except Exception as e:
        logger.error(f"Exception {e}")
    finally:
        driver.quit()
        logger.info("=== Navegador encerrado. ===")

if __name__ == "__main__":
    main()
