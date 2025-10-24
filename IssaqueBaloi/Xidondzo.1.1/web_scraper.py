from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

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

def download_file(download_dir):
    """Acede ao site e descarrega o ficheiro GenericReport.txt."""
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
            return None
        return caminho_ficheiro

    except TimeoutException:
        print("❌ Link para download não encontrado a tempo.")
        return None
    except Exception as e:
        print(f"❌ Ocorreu um erro: {str(e)}")
        return None
    finally:
        driver.quit()