from asyncio.windows_events import NULL
from configparser import NoSectionError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from lxml import etree
from time import sleep

class WebDriver:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def go_to_url(self, url):
        self.driver.get(url)


    # Variável de classe para controlar tentativas de loading
    
    def wait_document_ready(self):
        """Espera o documento(página web) estar completamente carregado"""
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
        print("encontrando spinner")
        try:
            # Primeiro verifica se o spinner está presente (timeout curto)
            spinner_selector = 'article [aria-label*="Carregando"], article [data-visualcompletion="loading-state"], article [role="progressbar"]'
            spinner = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            print("Spinner encontrado, aguardando desaparecer...")
            
            # Tenta rolar até o spinner para garantir visibilidade
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", spinner)
            except:
                pass
            
            # Espera até que desapareça
            WebDriverWait(self.driver, 30).until(
                EC.staleness_of(spinner)
            )
            print("Spinner desapareceu")
            return True
        except TimeoutException as e:
            print("Spinner demorou demais")
            print("-ERRO-: "+ str(e))
            return None  # Retorna None para tratamento especial
        except NoSuchElementException:
            print("Nenhum spinner encontrado, continuando...")
            print("-ERRO-: "+ str(e))
            return True # Retorna True porque ausência de spinner também é válido
        except WebDriverException as e:
            print(f"Erro interno do WebDriver: {e}")
            return False
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return False

    def wait_reply_spinner(self, spinner_index):
        """Espera o spinner de "Ver respostas" específico desaparecer, se existir"""
        print("encontrando spinner de resposta"+ str(spinner_index))
        try:
            # Primeiro verifica se o spinner está presente (timeout curto)
            spinner_selector = 'article ul ul [aria-label*="Carregando"], article ul ul [data-visualcompletion="loading-state"], article ul ul [role="progressbar"]'
            spinners = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, spinner_selector))
            )
            print("Spinner de resposta "+ str(spinner_index)+" encontrado, aguardando desaparecer...")
            
            # Tenta rolar até o spinner para garantir visibilidade
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", spinners[spinner_index])
            except:
                pass
            
            # Espera até que desapareça
            WebDriverWait(self.driver, 30).until(
                EC.staleness_of(spinners[spinner_index])
            )
            print("Spinner de resposta"+ str(spinner_index)+"desapareceu")
            return True
        except TimeoutException as e:
            print("Spinner de resposta "+ str(spinner_index)+" demorou demais")
            print("-ERRO-: "+ str(e))
            return None  # Retorna None para tratamento especial
        except NoSuchElementException:
            print("Nenhum spinner de resposta "+ str(spinner_index)+" encontrado, continuando...")
            print("-ERRO-: "+ str(e))
            return True # Retorna True porque ausência de spinner também é válido
        except WebDriverException as e:
            print(f"Erro interno do WebDriver: {e}")
            return False
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return False

    def loading_2(self):
        """Função principal de espera de carregamento, com tentativas limitadas"""
        loading_attempts = 0
        max_loading_attempts = 3

        while loading_attempts < max_loading_attempts:
            loading_attempts += 1
            print(f"\nTentativa de carregamento #{loading_attempts}...")

            try:
                doc_ready = self.wait_document_ready()
                spinner_done = self.wait_spinner()

                if doc_ready and spinner_done:
                    print("\nCarregamento concluído com sucesso!")
                    return True
                elif doc_ready and spinner_done is None:
                    print("\nCarregamento demorou demais, prosseguindo")
                    return None

            except Exception as e:
                print(f"\nErro durante o carregamento: {str(e)}")
                return False

            print("\nTentativa de carregamento falhou, tentando novamente...")

        print("\nMáximo de tentativas de carregamento atingido. Desistindo.")
        return False

    def loading_reply(self, spinner_index):
        loading_attempts = 0
        max_loading_attempts = 3

        while loading_attempts < max_loading_attempts:
            loading_attempts += 1
            print(f"\nTentativa de carregamento #{loading_attempts}...")

            try:
                doc_ready = self.wait_document_ready()
                spinner_done = self.wait_reply_spinner(spinner_index)

                if doc_ready and spinner_done:
                    print("\nCarregamento concluído com sucesso!")
                    return True
                elif doc_ready and spinner_done is None:
                    print("\nCarregamento demorou demais, prosseguindo")
                    return None

            except Exception as e:
                print(f"\nErro durante o carregamento: {str(e)}")
                return False

            print("\nTentativa de carregamento falhou, tentando novamente...")

        print("\nMáximo de tentativas de carregamento atingido. Desistindo.")
        return False

    def wait_post_ready(self):
        self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'article div[role = "presentation"]'
        )))
        
    def loading(self):
        #espera o fim do carregamento, se algo estiver carregando
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
            ))        
            WebDriverWait(self.driver, 90).until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, '[aria-label*="Carregando"][data-visualcompletion="loading-state"][role="progressbar"]')
            ))
        except:
            print("Carregamento não finalizado, esperando 30 segundos")
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
            while not self.loading_2(): #apenas prossegue quando o carregamento finaliza corretamente(retorna True)
                pass
            login_error = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Sua senha está incorreta')] | //div[contains(text(), 'Houve um problema ao entrar no Instagram')]")
            if login_error:
                print("Falha no login. Automação detectada")
        except Exception as e:
            print("Falha no login. Erro: "+ str(e))


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
        self.wait_post_ready()
        

    def open_more_comments(self):
        while True:
                try:
                    more_comments_button = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, '[aria-label = "Carregar mais comentários"]'
                    )))
                    more_comments_button = more_comments_button.find_element(By.XPATH, './ancestor::button[1]')
                    more_comments_button.click()      
                    if self.loading_2() is None: #Carregamento demorou demais, desiste de tentar abrir mais comentários
                        return None #retorna None para não tentar abrir comentários ocultos
                except TimeoutException:
                    print("Não há mais comentários não ocultos")
                    return True
                except Exception as e:
                    print(f"Erro inesperado: {e}")
                    return False #retorna False para não tentar abrir comentários ocultos


    def open_hidden_comments(self):
        hidden_comments_button = self.driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span')
        
        if hidden_comments_button:
            try:
                hidden_comments_button = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 'svg[aria-label="Ver comentários ocultos"] + div span'
                    )))
                try:
                    hidden_comments_button.click() #tenta clicar normalmente
                    self.loading_2()
                except:
                    self.driver.execute_script("arguments[0].click();", hidden_comments_button) #clique com JavaScript(se o Selenium não conseguir sozinho)
                    self.loading_2()
            except:
                print("Não há comentários ocultos.")
        else:
            print("Não há comentários ocultos.")

    #TODO: abrir todas ao mesmo tempo
    def open_replies(self):
        try:
            see_replies_buttons = self.wait.until(EC.presence_of_all_elements_located((
                By.XPATH, '//button[span[contains(., "Ver respostas")]]'
            )))
            for button in see_replies_buttons: #clica em todos os botões de ver respostas
                button.click() 
            
            for num_buttons in range(len(see_replies_buttons)): #espera todas as respostas carregarem
                previous_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) 
                #número de respostas antes de abrir as respostas
                spinner_index = 0 
                #caso o spinner demore muito, é ignorado e apenas os próximos são esperados
                if self.loading_reply(spinner_index) is True:
                    self.wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) > previous_count) 
                    #espera até que o número de respostas aumente se o carregamento for bem-sucedido
                else:    
                    spinner_index += 1 #carregamento não deu certo, esse spinner será ignorado
                    #TODO: essa função supõe que o spinner nunca irá carregar, se ele carregar, spinners normais podem acabar sendo ignorados 
        except NoSuchElementException or TimeoutException:
            print("Não há respostas para os comentários.")
        except Exception as e:
            print("Erro inesperado: "+ str(e))

    def have_comments(self): #checa se há ao menos um comentário
        try:
            self.WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'h3 + div > span'
            )))
            return True
        except:
            return False


    def open_all_comments(self):
        if self.have_comments():
            if self.open_more_comments() is True:
                self.open_hidden_comments() #só é possível abrir comentários ocultos quando todos os não ocultos forem abertos
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
            self.loading_2()
            self.wait_post_ready()
            return True
        except Exception as e:
            print("fim dos posts. Erro: "+ str(e))
            return False
