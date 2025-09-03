from asyncio.windows_events import NULL
from configparser import NoSectionError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementClickInterceptedException
from lxml import etree
from time import sleep
from TagSaver import TagSaver

class WebDriver:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.tag_saver = TagSaver()

    def go_to_url(self, url):
        self.driver.get(url)


    # Variável de classe para controlar tentativas de loading
    
    def wait_document_ready(self):
        """Espera o documento(página web) estar completamente carregado"""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            #print("Documento carregado")
            return True
        except TimeoutException:
            print("Aviso: Documento não carregou no tempo limite")
            return False
        except Exception as e:
            print(f"Erro inesperado em wait_document_ready: \n{e}")
            return False

    def wait_spinner(self):
        """Espera o spinner desaparecer, se existir"""
        #print("encontrando spinner")
        try:
            # Primeiro verifica se o spinner está presente (timeout curto)
            try:
                spinner_selector = 'article [data-visualcompletion="loading-state"], article [role="progressbar"]'
                spinner = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
                )
            except TimeoutException:
                return True
            except Exception as e:
                print(f"Erro inesperado em wait_spinner ao tentar encontrar o spinner: \n{e}")
                return False
            #print("Spinner encontrado, aguardando desaparecer...")
            
            # Tenta rolar até o spinner para garantir visibilidade
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", spinner)
            except:
                pass
            
            # Espera até que desapareça
            self.wait.until(
                EC.staleness_of(spinner)
            )
            #print("Spinner desapareceu")
            return True
        except TimeoutException as e:
            #print("Spinner demorou demais")
            #print("-ERRO-: "+ str(e))
            return None  # Retorna None para tratamento especial
        except NoSuchElementException:
            #print("Nenhum spinner encontrado, continuando...")
            #print("-ERRO-: "+ str(e))
            return True # Retorna True porque ausência de spinner também é válido
        except WebDriverException as e:
            print(f"Erro interno do WebDriver: \n{e}")
            return False
        except Exception as e:
            print(f"Erro inesperado em wait_spinner: \n{e}")
            return False

    def wait_reply_spinner(self, spinner_index):
        """Espera o spinner de "Ver respostas" específico desaparecer, se existir"""
        #print("encontrando spinner de resposta "+ spinner_index+1)
        try:
            # Primeiro verifica se o spinner está presente (timeout curto)
            spinner_selector = 'article ul ul [data-visualcompletion="loading-state"], article ul ul [role="progressbar"]'
            spinners = WebDriverWait(self.driver, 1, 0.2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, spinner_selector))
            )
            if spinner_index == -1: #espera rapidamente cada spinner
                for spinner in spinners:
                    try:
                        WebDriverWait(self.driver, 2).until(
                            EC.staleness_of(spinner)
                        )
                    except:
                        continue
                return True

            elif spinner_index < len(spinners):
                #print("Spinner de resposta "+ str(spinner_index)+" encontrado, aguardando desaparecer...")
            
                # Tenta rolar até o spinner para garantir visibilidade
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", spinners[spinner_index])
                except:
                    pass
                
                # Espera até que desapareça
                WebDriverWait(self.driver, 5).until(
                    EC.staleness_of(spinners[spinner_index])
                )
                #print("Spinner de resposta"+ str(spinner_index)+"desapareceu")
                return True
            else:
                #print("Spinner de resposta "+ str(spinner_index)+" não encontrado")
                return True
        except TimeoutException as e:
            #print("Spinner de resposta "+ str(spinner_index)+" demorou demais")
            #print("-ERRO-: "+ str(e))
            return None  # Retorna None para tratamento especial
        except NoSuchElementException:
            #print("Nenhum spinner de resposta "+ str(spinner_index)+" encontrado, continuando...")
            #print("-ERRO-: "+ str(e))
            return True # Retorna True porque ausência de spinner também é válido
        except WebDriverException as e:
            print(f"Erro interno do WebDriver: \n{e}")
            return False
        except Exception as e:
            print(f"Erro inesperado em wait_reply_spinner: \n{e}")
            return False

    def loading(self):
        """Função principal de espera de carregamento, com tentativas limitadas"""
        loading_attempts = 0
        max_loading_attempts = 3

        while loading_attempts < max_loading_attempts:
            loading_attempts += 1
            #print(f"\nTentativa de carregamento #{loading_attempts}...")

            try:
                doc_ready = self.wait_document_ready()
                spinner_done = self.wait_spinner()

                if doc_ready and spinner_done:
                    #print("\nCarregamento concluído com sucesso!")
                    return True
                elif doc_ready and spinner_done is None:
                    #print("\nCarregamento demorou demais, prosseguindo")
                    return None

            except Exception as e:
                print(f"\nErro inesperado em loading: \n{e}")
                return False

            #print("\nTentativa de carregamento falhou, tentando novamente...")

        #print("\nMáximo de tentativas de carregamento atingido. Desistindo.")
        return False

    def loading_reply(self, spinner_index):
        loading_attempts = 0
        max_loading_attempts = 2

        while loading_attempts < max_loading_attempts:
            loading_attempts += 1
            #print(f"\nTentativa de carregamento de resposta {spinner_index} #{loading_attempts}...")

            try:
                doc_ready = self.wait_document_ready()
                spinner_done = self.wait_reply_spinner(spinner_index)

                if doc_ready and spinner_done:
                    #print("\nCarregamento de resposta "+ str(spinner_index)+" concluído com sucesso!")
                    return True
                elif doc_ready and spinner_done is None:
                    #print("\nCarregamento de resposta "+ str(spinner_index)+" demorou demais, prosseguindo")
                    return None

            except Exception as e:
                print(f"\nErro durante o carregamento de resposta {spinner_index}: {str(e)}")
                return False

            #print("\nTentativa de carregamento de resposta "+ str(spinner_index)+" falhou, tentando novamente...")

        #print("\nMáximo de tentativas de carregamento de resposta "+ str(spinner_index)+" atingido. Desistindo.")
        return False

    def wait_post_ready(self):
        try:
            self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'article div[role = "presentation"]'
            )))
        except:
            print("falha no carregamento")
                

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
            while not self.loading(): #apenas prossegue quando o carregamento finaliza corretamente(retorna True)
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


    def capture_tags(self, tag):
        try:
            tags = self.wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, f'a[href^="/"][href$="/"]:not([href^="/p"]):not(footer a):not(span > div > a):not(main a)'
            )))
            return tags
        except TimeoutException:
            print(f"nenhuma tag {tag} encontrada")
            return None


    def search_tag(self, tag, tag_index=0):
        #Pesquisa manual de tag
        #vai no primeiro resultado por padrão
        #volta à página inicial
        self.driver.get('https://www.instagram.com/')
        self.driver.fullscreen_window()
        try:
            search_button = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'a svg[aria-label="Pesquisa"]'
            )))
            search_button.click() #clica no botao de pesquisa

            search_input = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//input[@aria-label="Entrada da pesquisa" and not(ancestor::main)]'
            )))
            search_input.send_keys(tag)
            self.loading()
            tag_elements = self.capture_tags(tag)

            if tag_elements is None:
                print(f"nenhuma tag {tag} encontrada")
                return None
            
            num_tags = len(tag_elements)

            if tag_index >= num_tags:
                print(f"não há °{tag_index+1} tag em {tag}")
                return None
    
            tag_element = tag_elements[tag_index]
            if self.tag_saver.is_tag_saved(tag_element):
                print(f"Tag {tag_element.text} já foi raspada.")
                return None
            #espera estar clicavel
            self.wait.until(EC.element_to_be_clickable(tag_element))
            tag_element.click() #clica na tag
            self.tag_saver.save_tag(tag_element)
            return True
        except TimeoutException:
            print("Elemento de busca(Lupa) não encontrado")
            return False
        except Exception as e:
            print(f"Erro inesperado em search_tag: \n{e}")
            return False


    

    def click_on_first_post(self):
        #clica no primeiro post encontrado
        try:
            first_post = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'div[style="--x-width: 100%;"] > a, header + div + div a'
            )))
            first_post.click()
        except ElementClickInterceptedException:
            # Tenta fechar modal genérico se estiver visível
            try:
                modal = self.driver.find_element(By.CSS_SELECTOR, 'div.generic_dialog.pop_dialog.generic_dialog_modal')
                close_btn = modal.find_elements(By.CSS_SELECTOR, 'button, [role="button"], .x1i10hfl')
                for btn in close_btn:
                    try:
                        btn.click()
                        break
                    except:
                        continue
                # Aguarda o modal sumir
                WebDriverWait(self.driver, 5).until(EC.staleness_of(modal))
            except Exception:
                pass
            # Tenta novamente
            self.click_on_first_post()

    def open_more_comments(self):
        while True:
                try:
                    more_comments_button = self.wait.until(EC.presence_of_element_located((
                        By.XPATH, '//button[.//*[name()="svg"][@aria-label="Carregar mais comentários"]]'
                    )))
                    #more_comments_button = more_comments_button.find_element(By.XPATH, './ancestor::button[1]')
                    more_comments_button.click()      
                    if self.loading() is None: #Carregamento demorou demais, desiste de tentar abrir mais comentários
                        return None #retorna None para não tentar abrir comentários ocultos
                except (NoSuchElementException, TimeoutException):
                    print("Não há mais comentários não ocultos")
                    return True
                except Exception as e:
                    print(f"Erro inesperado em open_more_comments: \n{e}")
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
            try:
                see_replies_buttons = self.wait.until(EC.presence_of_all_elements_located((
                    By.XPATH, '//button[span[contains(., "Ver respostas")]]'
                )))
            except TimeoutException:
                print("Não há respostas para os comentários.")
                return
            except Exception as e:
                print(f"Erro inesperado em open_replies ao coletar botões de ver respostas: \n{e}")
                return

            for button in see_replies_buttons: #clica em todos os botões de ver respostas
                button.click() 
            
            spinner_index = 0 
            #caso o spinner demore muito, é ignorado e apenas os próximos são esperados
            for num_buttons in range(len(see_replies_buttons)): #espera todas as respostas carregarem
                
                previous_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) 
                #número de respostas antes de abrir as respostas
                
                loading_result = self.loading_reply(spinner_index)
                if loading_result is True:
                    try:
                        self.wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ul li h3 + div > span')) > previous_count) 
                    #espera até que o número de respostas aumente se o carregamento for bem-sucedido
                    except:
                        print("spinner sumiu, mas comentários não apareceram a tempo")
                        continue
                elif loading_result is None:    
                    spinner_index += 1 #carregamento não deu certo, esse spinner será ignorado
                else:
                    #algum erro no carregamento, cessar abertura de respostas
                    print("erro ao abrir respostas, desistindo dessa atividade")
                    break
            
            #verifica todos os spinners abandonados e espera rapidamente cada um
            self.loading_reply(-1) 

        except Exception as e:
            print(f"Erro inesperado em open_replies: \n{e}")

    def have_comments(self): #checa se há ao menos um comentário
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'h3 + div > span'
            )))
            print("post tem comentários")
            return True
        except TimeoutException:
            print("post sem comentários")
            return False
        except Exception as e:
            print(f"Erro inesperado em have_comments \n{e}")
            return False


    def open_all_comments(self):
        print("esperando post carregar")
        self.wait_post_ready()
        print("checando se há comentários")
        if self.have_comments():
            print("abrindo mais comentários, se houverem")
            if self.open_more_comments() is True:
                print("abrindo comentários ocultos")
                self.open_hidden_comments() #só é possível abrir comentários ocultos quando todos os não ocultos forem abertos
            print("abrindo respostas, se houverem")
            self.open_replies()


    def get_post_html(self):
        #pega o html da parte textual do post
        post_html = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'article div[role = "presentation"]:has(*)'
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
                By.XPATH, '//button[.//*[name()="svg"][@aria-label="Avançar"]]' #encontra o filho do botão
            )))
            #next_post_button = next_post_button.find_element(By.XPATH, '..') #sobe a hierarquia para encontrar o botão
            next_post_button.click()
            self.loading()
            self.wait_post_ready()
            return True
        except (NoSuchElementException, TimeoutException):
            print("fim dos posts")
            return None
        except Exception as e:
            print(f"Erro inesperado em go_to_next_post: \n{e}")
            return False
