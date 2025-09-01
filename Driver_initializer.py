from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class Driver_initializer:

    def config_driver():
        #configurações do driver(pra não aparecer avisos no terminal)
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=3")  # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL

        service = Service(ChromeDriverManager().install(), log_path="NUL")  # em Windows
        # ou log_path="/dev/null" no Linux/macOS

        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def config_wait(driver, max_time):
        wait = WebDriverWait(driver, max_time)
        return wait