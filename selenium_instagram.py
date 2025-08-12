from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from parsel import Selector

#credenciais
with open("credenciais.xml", "r", encoding="utf-8") as f:
    credenciais = f.read()

sel = Selector(text=credenciais)
# Extrai o texto das tags <email> e <senha>
email = sel.xpath("//instagram/email/text()").get()
senha =sel.xpath("//instagram/senha/text()").get()

#login no instagram
driver = webdriver.Chrome()
driver.get('https://www.instagram.com/')

email_input = WebDriverWait(driver,10).until(EC.element_to_be_clickable((
    By.NAME, "username"
)))
email_input.send_keys(email) #preenche email

senha_input = WebDriverWait(driver,10).until(EC.element_to_be_clickable((
    By.NAME, "password"
)))
senha_input.send_keys(senha) #preenche senha

login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//div[text()='Entrar']"
)))
login_button.click() #clica em entrar

WebDriverWait(driver, 10).until(EC.url_to_be('https://www.instagram.com/accounts/onetap/?next=%2F'))

not_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//div[text()='Agora não' or tabindex='0']"
)))
not_now_button.click()


input()
sleep(1)