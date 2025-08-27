from JsonManager import JsonManager
from Scraper import Scraper
from WebDriver import WebDriver

class Facade:
    def __init__(self, driver, wait, tag):
        self.web_driver = WebDriver(driver, wait)
        self.scraper = Scraper()
        self.json_manager = JsonManager()
        self.tag = tag

    

    def login(self):
        self.web_driver.go_to_url('https://www.instagram.com/')
        self.json_manager.delete_previous_json(self.tag)
        credentials = self.scraper.get_credentials()
        self.web_driver.login(*credentials)
        self.web_driver.not_now()

    
    def go_to_posts(self):
        #self.web_driver.search_tag(tag)
        self.web_driver.driver.get('https://www.instagram.com/explore/search/keyword/?q=%23uece') #tag uece
        self.web_driver.click_on_first_post()

    def scrape_post_text(self):
        self.web_driver.driver.fullscreen_window()
        self.web_driver.open_all_comments()
        post_html = self.web_driver.get_post_html()
        self.scraper.scrape_post_text(post_html)
        self.web_driver.go_to_next_post()
    
    def scrape_posts_text(self, num_posts):
        post_counter = 0
        for post in range(num_posts):
            post_counter += 1
            print(f"raspando o post nº {post_counter}")
            self.scrape_post_text()
        print("raspagem terminada")

    
    """driver.get('https://www.instagram.com/')
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
    input()"""
