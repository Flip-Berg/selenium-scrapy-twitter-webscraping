from JsonManager import JsonManager
from Scraper import Scraper
from WebDriver import WebDriver

class Facade:
    def __init__(self, driver, wait, tags):
        self.web_driver = WebDriver(driver, wait)
        self.scraper = Scraper()
        self.json_manager = JsonManager()
        self.tags = tags

    

    def login(self, url):
        self.web_driver.go_to_url(url)
        self.web_driver.driver.fullscreen_window()
        self.json_manager.delete_previous_jsons(self.tags)
        credentials = self.scraper.get_credentials()
        self.web_driver.login(*credentials)
        self.web_driver.not_now()

    
    def go_to_posts_by_tag(self, tag):
        if self.web_driver.search_tag(tag) is False:
            print(f"Erro ao buscar tag {tag}")
            return False
        while self.web_driver.loading() is not True: #espera até que a página carregue
            self.web_driver.driver.refresh()
            pass
        self.web_driver.click_on_first_post()

    def go_to_posts_direct_link(self):
        #tag #uece
        self.web_driver.driver.get('https://www.instagram.com/explore/search/keyword/?q=%23uece')
        while not self.web_driver.loading(): #espera até que a página carregue
            pass
        self.web_driver.click_on_first_post()
        self.web_driver.driver.fullscreen_window()

    def scrape_post_text(self, tag):
        
        self.web_driver.open_all_comments()
        post_html = self.web_driver.get_post_html()
        self.scraper.scrape_post_text(post_html, tag, self.json_manager)
        if self.web_driver.go_to_next_post() is None:
            #fim dos posts
            return None
        elif self.web_driver.go_to_next_post() is False:
            #erro inesperado
            return False
    
    def scrape_posts_text(self, num_posts, tag):
        for post in range(num_posts+1):
            print(f"raspando o post nº {post+1}")
            result = self.scrape_post_text(tag)
            if result is None:
                #fim dos posts
                print(f"fim dos posts com a tag {tag}")
                break
            elif result is False:
                #erro inesperado
                print("erro inesperado em scrape_post_text ao avançar para o próximo post")
                break
        print(f"raspagem da tag {tag} terminada")
        print(f"foram raspados {post+1} posts")

    def traverse_posts(self):
        while self.web_driver.go_to_next_post():
            pass
