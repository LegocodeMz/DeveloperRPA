from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import Config

def get_driver(headless=True, browser="chrome"):
    if browser.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        if headless:
            options.headless = True
        driver = webdriver.Firefox(options=options)

    driver.set_page_load_timeout(Config.TIMEOUT)
    driver.implicitly_wait(1)
    return driver
