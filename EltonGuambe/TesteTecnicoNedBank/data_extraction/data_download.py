import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, UnexpectedAlertPresentException
import constants as const

class DataDownload:
    def __init__(self, download_folder=None):
        if download_folder is None:
            project_root = os.path.dirname(os.path.abspath(__file__))
            download_folder = os.path.join(project_root, "downloads")
        self.download_folder = download_folder
        os.makedirs(self.download_folder, exist_ok=True)
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def download_file(self, url=None, link_text=None):
        url = url or const.BASE_URL
        link_text = const.BASE_URL
        self.driver.get(url)
        time.sleep(2)

        try:
            download_element = self.driver.find_element("link text", "aqui")
            download_element.click()
            print("Clique no link de download realizado.")
        except NoSuchElementException:
            print("Elemento de download não encontrado.")
            return None
        except ElementClickInterceptedException:
            print("Clique interceptado, tentando scroll...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", download_element)
            download_element.click()
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            download_element.click()

        # Esperar download completar
        file_path = None
        timeout = 30
        start = time.time()
        while time.time() - start < timeout:
            files = os.listdir(self.download_folder)
            txt_files = [f for f in files if f.endswith(".txt")]
            if txt_files:
                file_path = os.path.join(self.download_folder, txt_files[0])
                break
            time.sleep(1)

        if file_path:
            print(f"Ficheiro baixado com sucesso: {file_path}")
        else:
            print("Tempo limite atingido. Download falhou.")

        return file_path

    def close(self):
        self.driver.quit()


# Teste
if __name__ == "__main__":
    downloader = DataDownload()
    path = downloader.download_file()
    downloader.close()
    print(f"Ficheiro final: {path}")
