from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector

#credenciais
with open("conta.xml", "r", encoding="utf-8") as f:
    credenciais = f.read()

sel = Selector(text=credenciais)
# Extrai o texto da tag <email>
email = sel.xpath("//email/text()").get()
senha =sel.xpath("//senha/text()").get()

#login no twitter
driver = webdriver.Chrome() #inicialização
driver.get('https://x.com') #url desejada

login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Entrar']"
)))
login_button.click() #encontra e clica no login

login_input = WebDriverWait(driver,10).until(EC.element_to_be_clickable((
    By.TAG_NAME, "input"
)))
login_input.send_keys(email) #preenche email

login_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Avançar']"
)))
login_button2.click() #clica em avançar


sleep(3)
driver.quit()