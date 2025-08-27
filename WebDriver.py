from configparser import NoSectionError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep

class WebDriver:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self._loading_attempts = 0
        self._max_loading_attempts = 3

    def go_to_url(self, url):
        self.driver.get(url)


    # Variável de classe para controlar tentativas de loading
    
    #TODO: fix loading
    def wait_document_ready(self):
        """Espera o documento estar completamente carregado"""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("Documento carregado")
            return True
        except TimeoutException:
            print("Aviso: Documento não carregou no tempo limite")
            return False
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return False

    def wait_spinner(self):
        """Espera o spinner desaparecer, se existir"""
        try:
            # Primeiro verifica se o spinner está presente (timeout curto)
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.spinner_selector))
            )
            print("spinner encontrado, aguardando desaparecer...")
            # Espera até que desapareça por 2 minutos
            WebDriverWait(self.driver, 120).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, self.spinner_selector))
            )
            print("Carregamento concluído")
            return True
        except TimeoutException:
            print("Spinner não encontrado ou não desapareceu a tempo")
            return True  # Retorna True porque ausência de spinner também é válido
        except NoSuchElementException:
            print("Nenhum elemento de carregamento encontrado, continuando...")
            return True
        except WebDriverException as e:
            print(f"Erro interno do WebDriver: {e}")
            return False
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return False

    def loading_2(self):
        """Função principal de espera de carregamento, com tentativas limitadas"""
        while self._loading_attempts < self._max_loading_attempts:
            self._loading_attempts += 1
            print(f"Tentativa de carregamento #{self._loading_attempts}...")

            doc_ready = self.wait_document_ready()
            spinner_done = self.wait_spinner()

            if doc_ready and spinner_done:
                # Reset contador e encerra
                self._loading_attempts = 0
                return

            print("Tentativa falhou, aguardando 2s antes da próxima tentativa...")
            time.sleep(2)

        # Se atingir o máximo de tentativas
        print("Número máximo de tentativas de carregamento atingido. Desistindo.")
        self._loading_attempts = 0
    
    def loading(self):
        #espera o fim do carregamento, se algo estiver carregando
        try:
            WebDriverWait(self.driver, 90).until(EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
            ))        
            WebDriverWait(self.driver, 90).until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
            ))
        except:
            print("Carregamento não finalizado")
            sleep(30)
                

    def login(self, email,senha):
        email_input = self.wait.until(EC.element_to_be_clickable((
            By.NAME, "username"
        )))
        email_input.send_keys(email) #preenche email

        senha_input = self.wait.until(EC.element_to_be_clickable((
            By.NAME, "password"
        )))
        senha_input.send_keys(senha) #preenche senha

        try:
            login_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[text()='Entrar']"
            )))
            login_button.click() #clica em entrar
            self.loading()
            login_error = self.driver.find_elements(By.XPATH, "//[text()='Sua senha está incorreta. Confira-a.'] or //[text()='Houve um problema ao entrar no Instagram. Tente novamente em breve']")
            if login_error:
                print("Falha no login")
        except:
            print("Falha no login")


    def not_now(self):
        not_now_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[text()="Agora não"]'
        )))
        not_now_button.click()

        self.wait.until(EC.url_to_be('https://www.instagram.com/')) 


    def search_tag(self, tag):
        #Pesquisa manual(caso url direto não funcione)
        self.driver.fullscreen_window()

        search_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'a svg[aria-label="Pesquisa"]'
        )))
        search_button.click() #clica no botao de pesquisa

        search_input = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'input[aria-label="Entrada da pesquisa"]'
        )))
        search_input.send_keys(tag)

        tag = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, f'a[href="/explore/tags/{tag}/"]'
        )))
        tag.click()
        #só funciona se a tag existir exatamente como digitado


    def click_on_first_post(self):
        #clica no primeiro post encontrado
        first_post = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'div[style="--x-width: 100%;"] > a'
        )))
        first_post.click()


    def open_more_comments(self):
        while True:
                try:
                    more_comments_button = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, '[aria-label = "Carregar mais comentários"]'
                    )))
                    more_comments_button = more_comments_button.find_element(By.XPATH, './ancestor::button[1]')
                    more_comments_button.click()      
                    self.loading()
                except:
                    print("Não há mais comentários não ocultos")
                    break


    def open_hidden_comments(self):
        hidden_comments_button = self.driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span')
        
        if hidden_comments_button:
            try:
                hidden_comments_button = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span'
                    )))
                try:
                    hidden_comments_button.click() #tenta clicar normalmente
                    self.loading()
                except:
                    self.driver.execute_script("arguments[0].click();", hidden_comments_button) #clique com JavaScript(se o Selenium não conseguir sozinho)
                    self.loading()
            except:
                print("Não há comentários ocultos.")
        else:
            print("Não há comentários ocultos.")


    def open_replies(self):
        try:
            see_replies_buttons = self.wait.until(EC.presence_of_all_elements_located((
                By.XPATH, '//button[span[contains(., "Ver respostas")]]'
            )))
            for button in see_replies_buttons:
                previous_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) #número de respostas antes de abrir as respostas
                button.click()
                self.loading()
                self.wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) > previous_count) #espera até que o número de respostas aumente
        except:
            print("Não há respostas para os comentários.")


    def open_all_comments(self):
        self.open_more_comments()
        self.open_hidden_comments()
        self.open_replies()    


    def get_post_html(self):
        #pega o html da parte textual do post
        post_html = self.wait.until(EC.presence_of_element_located((
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
        
    def go_to_next_post(self):
        try:
            next_post_button = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'svg[aria-label="Avançar"]' #encontra o filho do botão
            )))
            next_post_button = next_post_button.find_element(By.XPATH, '..') #sobe a hierarquia para encontrar o botão
            next_post_button.click()
            self.loading()
        except:
            print("fim dos posts")
