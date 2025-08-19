from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from parsel import Selector
import json

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

wait = WebDriverWait(driver, 15)

email_input = wait.until(EC.element_to_be_clickable((
    By.NAME, "username"
)))
email_input.send_keys(email) #preenche email

senha_input = wait.until(EC.element_to_be_clickable((
    By.NAME, "password"
)))
senha_input.send_keys(senha) #preenche senha

try:
    login_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[text()='Entrar']"
    )))
    login_button.click() #clica em entrar
except:
    print("Falha no login")

#wait.until(EC.url_to_be('https://www.instagram.com/accounts/onetap/?next=%2F'))

not_now_button = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[text()='Agora não' or tabindex='0']"
)))
not_now_button.click()

#wait.until(EC.url_to_be('https://www.instagram.com/')) 

driver.get('https://www.instagram.com/explore/search/keyword/?q=%23uece') #tag uece
"""
Pesquisa manual -> caso url direto não funcione


driver.fullscreen_window()

search_button = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, 'a svg[aria-label="Pesquisa"]'
)))
search_button.click() #clica no botao de pesquisa

search_input = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, 'input[aria-label="Entrada da pesquisa"]'
)))
search_input.send_keys('#uece')

uece_tag = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, 'a[href="/explore/tags/uece/"]'
)))
uece_tag.click()
"""

first_post = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, 'div[style="--x-width: 100%;"] > a'
)))
first_post.click()

driver.fullscreen_window()

#_ap3a _aaco _aacu _aacx _aad7 _aade: classe do span que contém os textos do post(instável, mas direto)
post_text = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR, 'div > h1'
)))
post_text = post_text.text
print(post_text)

#Antes de pegar os comentários, clica em "mais comentários" até que carreguem todos
while True:
    try:
        more_comments_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'svg[aria-label="Carregar mais comentários"]'
        )))
        # sobe direto para o <button>
        more_comments_button = more_comments_button.find_element(By.XPATH, './ancestor::button[1]')
        more_comments_button.click()
    except:
        print("Não há mais comentários não ocultos.")
        break

#Abre comentários ocultos, se existirem
try:
    hidden_comments_button = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span'
        )))
    driver.execute_script("arguments[0].click();", hidden_comments_button) #clique com JavaScript(Selenium não conseguiu sozinho)
except:
    print("Não há comentários ocultos.")

#pega todos os comentários
try:
    comments = wait.until(EC.presence_of_all_elements_located(( 
        By.CSS_SELECTOR, 'h3 + div > span'
    )))
except:
    print("Não há comentários neste post.")
    comments = []

#abre as respostas
try:
    see_replies_buttons = wait.until(EC.presence_of_all_elements_located((
        By.XPATH, '//button[span[contains(text(), "Ver respostas")]]'
    )))
    for button in see_replies_buttons:
        button.click()
except:
    print("Não há respostas para os comentários.")
"""
#esperar as respostas carregarem
hide_replies_button = wait.until(EC.presence_of_all_elements_located((
    By.XPATH, '//button[span[text() = "Ocultar respostas")]]'
)))
"""
comments_data = []

#TODO: fix respostas não aparecendo
for comment in comments:
    comment_text = comment.text
    """
    # sobe até o <ul> mais próximo e pega as respostas dentro dos <li>
    try:
        replies = wait.until(
            lambda d: comment.find_elements(By.XPATH, './ancestor::ul[1]/li//h3/../span')
        )
        replies_text = [reply.text for reply in replies]
    except:
        replies_text = []    

    """
    comments_data.append({
        "comentario": comment_text,
        #"respostas": replies_text
    })

with open("comments_data.json", "w", encoding="utf-8") as f:
    json.dump(comments_data, f, ensure_ascii=False, indent=4)


next_post_button = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, 'svg[aria-label="Avançar"]' #encontra o filho do botão
)))
next_post_button = next_post_button.find_element(By.XPATH, '..') #sobe a hierarquia para encontrar o botão
next_post_button.click()

input()
