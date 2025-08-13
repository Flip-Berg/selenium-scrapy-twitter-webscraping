from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from parsel import Selector
import random

def human_typing(element, text):
    for c in text:
        element.send_keys(c)
        sleep(random.uniform(0.01, 0.05))  # delay aleatório entre teclas

#credenciais
with open("credenciais.xml", "r", encoding="utf-8") as f:
    credenciais = f.read()

sel = Selector(text=credenciais)
# Extrai o texto da tag <email>
email = sel.xpath("//twitter/email/text()").get()
#senha =sel.xpath("//twitter/senha/text()").get()

#login no twitter
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")  # remove flag de automação
# você também pode adicionar user-agent realista
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)
driver.get('https://x.com') #url desejada
"""
firefox
pop_up_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//path[@d='M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z']"
)))
pop_up_button.click() #fecha pop-up
"""
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Entrar']"
)))
login_button.click() #encontra e clica no login

login_input = WebDriverWait(driver,10).until(EC.element_to_be_clickable((
    By.TAG_NAME, "input"
)))
human_typing(login_input, email) #preenche email

login_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, "//span[text()='Avançar']"
)))
login_button2.click() #clica em avançar


sleep(3)
driver.quit()