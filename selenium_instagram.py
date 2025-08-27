from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import json
from lxml import etree
import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)
tag = "#uece"
num_posts = 25 #numero desejado de posts a serem extraidos
url = 'https://www.instagram.com/'


def main():
    driver.get('https://www.instagram.com/')
    delete_previous_json() #files
    credenciais = get_credentials() 
    login(*credenciais) #web
    not_now() #web
    driver.get('https://www.instagram.com/explore/search/keyword/?q=%23uece') #tag uece 
    click_on_first_post() #web
    driver.fullscreen_window()
    post_counter = 0
    for post in range(num_posts):
        post_counter += 1
        open_all_comments() #web
        post_html = get_post_html() #web
        print("raspando post nº" + post_counter)
        scrape_post_text(post_html) #scrape + files
        go_to_next_post() #web
    print("raspagem terminada")
    input()

def get_credentials():
     #credenciais
    with open("credenciais.xml", "r", encoding="utf-8") as f:
        credenciais = f.read()

    sel = Selector(text=credenciais)
    # Extrai o texto das tags <email> e <senha>
    email = sel.xpath("//instagram/email/text()").get()
    senha =sel.xpath("//instagram/senha/text()").get()
    return email, senha

def loading():
    #espera o fim do carregamento, se algo estiver carregando
    loading = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
    if loading:
        WebDriverWait(driver, 90).until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
        ))


def get_credentials():
    #credenciais
    with open("credenciais.xml", "r", encoding="utf-8") as f:
        credenciais = f.read()

    sel = Selector(text=credenciais)
    # Extrai o texto das tags <email> e <senha>
    email = sel.xpath("//instagram/email/text()").get()
    senha =sel.xpath("//instagram/senha/text()").get()
    return email, senha


def login(email,senha):
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
        loading()
        login_error = driver.find_elements(By.XPATH, "//[text()='Sua senha está incorreta. Confira-a.'] or //[text()='Houve um problema ao entrar no Instagram. Tente novamente em breve']")
        if login_error:
            print("Falha no login")
    except:
        print("Falha no login")


def not_now():
    not_now_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, '//div[text()="Agora não"]'
    )))
    not_now_button.click()

    wait.until(EC.url_to_be('https://www.instagram.com/')) 


def search_tag(tag):
    #Pesquisa manual(caso url direto não funcione)
    driver.fullscreen_window()

    search_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'a svg[aria-label="Pesquisa"]'
    )))
    search_button.click() #clica no botao de pesquisa

    search_input = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'input[aria-label="Entrada da pesquisa"]'
    )))
    search_input.send_keys(tag)

    tag = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, f'a[href="/explore/tags/{tag}/"]'
    )))
    tag.click()
    #só funciona se a tag existir exatamente como digitado


def click_on_first_post():
    #clica no primeiro post encontrado
    first_post = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'div[style="--x-width: 100%;"] > a'
    )))
    first_post.click()


def open_more_comments():
    while True:
            try:
                more_comments_button = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, '[aria-label = "Carregar mais comentários"]'
                )))
                more_comments_button = more_comments_button.find_element(By.XPATH, './ancestor::button[1]')
                more_comments_button.click()      
                loading()
            except:
                print("Não há mais comentários não ocultos")
                break


def open_hidden_comments():
    hidden_comments_button = driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span')
    
    if hidden_comments_button:
        try:
            hidden_comments_button = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span'
                )))
            try:
                hidden_comments_button.click() #tenta clicar normalmente
                loading()
            except:
                driver.execute_script("arguments[0].click();", hidden_comments_button) #clique com JavaScript(se o Selenium não conseguir sozinho)
                loading()
        except:
            print("Não há comentários ocultos.")
    else:
        print("Não há comentários ocultos.")


def open_replies():
    try:
        see_replies_buttons = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, '//button[span[contains(., "Ver respostas")]]'
        )))
        for button in see_replies_buttons:
            previous_count = len(driver.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) #número de respostas antes de abrir as respostas
            button.click()
            loading()
            wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) > previous_count) #espera até que o número de respostas aumente
    except:
        print("Não há respostas para os comentários.")


def open_all_comments():
    open_more_comments()
    open_hidden_comments()
    open_replies()    


def get_post_html():
    #pega o html da parte textual do post
    post_html = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'div[role = "presentation"]'
    )))
    post_html = post_html.get_attribute('outerHTML')
    return post_html


def save_post_html(post_html):
    # Parsing do HTML
    parser = etree.HTMLParser()
    post_html_tree = etree.fromstring(post_html, parser)

    # Salvar com indentação correta
    with open("post.html", "wb") as f:
        f.write(etree.tostring(post_html_tree, pretty_print=True, encoding="utf-8"))


def delete_previous_json():
    json_filename = f"{tag}_posts_data.json"

    if os.path.exists(json_filename):
        os.remove(json_filename)
        print(f"Arquivo {json_filename} antigo foi apagado.")


def save_on_json(post_data):
    json_filename = f"{tag}_posts_data.json"

    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    # adiciona o novo post
    all_data.append(post_data)

    # salva de volta
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)


def scrape_post_text(post_html):
    post_selector = Selector(text=post_html)

    post_description = post_selector.xpath('string(.//h1)').get() #[role="presentation"] div > h1::text

    comment_blocks = post_selector.css(':not(li) > ul')[1:] 

    comments = []
    for comment_block in comment_blocks:
        comment_text = comment_block.xpath('string(.//h3/following-sibling::div/span)').get()
        if comment_text.endswith("ResponderOpções de comentários"): #ignora não comentários
            continue
        # respostas associadas a esse comentário
        replies_block = comment_block.xpath('.//ul[1]')
        replies_text = []
        for reply in replies_block.xpath('.//h3/following-sibling::div/span'):
            reply_text = reply.xpath('string()').get()
            if reply_text and not reply_text.endswith("ResponderOpções de comentários"):  # ignora vazios e não comentários
                replies_text.append(reply_text)

        comments.append({
            "comentario": comment_text,
            "respostas": replies_text
        })

    post_data = {
        "descricao": post_description,
        "comentarios": comments
    }
    save_on_json(post_data)
    


def go_to_next_post():
    try:
        next_post_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'svg[aria-label="Avançar"]' #encontra o filho do botão
        )))
        next_post_button = next_post_button.find_element(By.XPATH, '..') #sobe a hierarquia para encontrar o botão
        next_post_button.click()
        loading()
    except:
        print("fim dos posts")


#main()

#TODO: json manager
from Facade import Facade
def main_oop():
    instagram_text_scraper = Facade(driver, wait, tag)
    instagram_text_scraper.login()
    instagram_text_scraper.go_to_posts()
    instagram_text_scraper.scrape_posts_text(25)

main_oop()