from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from parsel import Selector
import json
from lxml import etree
import os


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

wait = WebDriverWait(driver, 30)

def loading():
    #espera o fim do carregamento, se algo estiver carregando
    loading = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
    if loading:
        wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
        ))

#data visual completion = loading state


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
    login_error = driver.find_elements(By.XPATH, "//[text()='Sua senha está incorreta. Confira-a.']")
    #Houve um problema ao entrar no Instagram. Tente novamente em breve.
    if login_error:
        print("Falha no login")
except:
    print("Falha no login")

not_now_button = wait.until(EC.element_to_be_clickable((
    By.XPATH, '//div[text()="Agora não"]'
)))
not_now_button.click()

wait.until(EC.url_to_be('https://www.instagram.com/')) 

driver.get('https://www.instagram.com/explore/search/keyword/?q=%23uece') #tag uece
#TODO: parametrizar
tag = "#uece"
json_filename = f"{tag}_posts_data.json"

if os.path.exists(json_filename):
    os.remove(json_filename)
    print(f"Arquivo {json_filename} antigo foi apagado.")


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

num_posts = 3 #numero desejado de posts a serem extraidos

for post in range(num_posts):

    #Antes de pegar os comentários, clica em "mais comentários" até que carreguem todos
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

    #Abre comentários ocultos, se existirem
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

    #abre as respostas
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

    #esperar as respostas carregarem
    """previous_loop = 0
    while True:
        replies = driver.find_elements(By.CSS_SELECTOR, "li > ul > div > li")
        if len(replies) == previous_loop: #só para de verificar quando o número de respostas estabiliza
            break
        previous_loop = len(replies)
        sleep(1)
"""
    post_text = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'div[role = "presentation"]'
    )))
    post_text = post_text.get_attribute('outerHTML')
    """
    # Parsing do HTML
    parser = etree.HTMLParser()
    post_text_tree = etree.fromstring(post_text, parser)

    # Salvar com indentação correta
    with open("post.html", "wb") as f:
        f.write(etree.tostring(post_text_tree, pretty_print=True, encoding="utf-8"))
    """
    #Extrair descrição, comentários e respostas

    """post_description = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'div > h1'
    )))
    post_description = post_description.text"""

    post_selector = Selector(text=post_text)
    post_description = post_selector.xpath('string(.//h1)').get() #[role="presentation"] div > h1::text

    # --- comentários principais ---
    #comment_blocks = [li.xpath('ancestor::ul[1]') for li in post_selector.css(':not(li) > ul > div > li')[1:]] #pega o <li> de cada comentário e sobe até seu respectivo <ul>(onde realmente fica o bloco do comentário)(o primeiro é a descrição)
    comment_blocks = post_selector.css(':not(li) > ul')[1:] 

    comments = []
    for comment_block in comment_blocks:
        comment_text = comment_block.xpath('string(.//h3/following-sibling::div/span)').get()
        if comment_text.endswith("ResponderOpções de comentários"): #ignora não comentários
            continue
        # respostas associadas a esse comentário
        replies_block = comment_block.xpath('.//ul[1]')
        replies_text = []
        is_odd = True
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

    # salvar em JSON
    # se o arquivo já existe, carrega o conteúdo
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

    """try:
        comments = wait.until(EC.presence_of_all_elements_located(( 
            By.CSS_SELECTOR, 'h3 + div > span'
        )))
    except:
        print("Não há comentários neste post.")
        comments = []

    comments = post_selector.css('h3 + div > span::text').getall()


    for comment in comments:
        comment_text = comment.text
        
        # sobe até o <ul> mais próximo e pega as respostas dentro dos <li>
        try:
            replies = wait.until(
                lambda d: comment.find_elements(By.XPATH, './ancestor::ul[1]/li//h3/../span')
            )
            replies_text = [reply.text for reply in replies]
        except:
            replies_text = []    

        

    comments_data = []


    comments_data.append({
        "comentario": comment_text,
        #"respostas": replies_text
    })

    with open("comments_data.json", "w", encoding="utf-8") as f:
        json.dump(comments_data, f, ensure_ascii=False, indent=4)

    """
    try:
        next_post_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'svg[aria-label="Avançar"]' #encontra o filho do botão
        )))
        next_post_button = next_post_button.find_element(By.XPATH, '..') #sobe a hierarquia para encontrar o botão
        next_post_button.click()
        loading()
    except:
        print("fim dos posts")


print("raspagem terminada")
input()