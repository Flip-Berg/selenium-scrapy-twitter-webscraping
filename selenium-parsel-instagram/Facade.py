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
        # self.json_manager.delete_previous_jsons(self.tags)
        credentials = self.scraper.get_credentials()
        self.web_driver.login(*credentials)
        self.web_driver.not_now()

    def go_to_posts_by_tag(self, tag, tag_index=0):
        search_result = self.web_driver.search_tag(tag, tag_index)
        if search_result == "Already saved":
            return "Already saved"
        if search_result is None:
            return None
        if search_result is False:
            print(f"Erro ao buscar tag input {tag}, prosseguindo")
            return False
        tag_text = search_result[1]
        while self.web_driver.loading() is not True:  # espera até que a página carregue
            self.web_driver.driver.refresh()
            pass
        #self.web_driver.load_all_posts()
        #self.web_driver.click_on_first_post()
        return tag_text

    def get_current_tag(self):
        return self.web_driver.tag_saver.get_current_tag()

    def go_to_posts_direct_link(self):
        # tag #uece
        self.web_driver.driver.get(
            'https://www.instagram.com/explore/search/keyword/?q=%23uece')
        while not self.web_driver.loading():  # espera até que a página carregue
            pass
        # self.web_driver.load_all_posts()
        self.web_driver.click_on_first_post()
        self.web_driver.driver.fullscreen_window()

    def scrape_post_text(self, tag):
        post_description = self.web_driver.get_post_description()
        # print("Descrição do post(facade):")
        # print(repr(post_description))
        saved_post = self.json_manager.check_if_post_is_saved(
            tag, post_description, True)
        if saved_post:
            print(
                "Post já salvo anteriormente, escaneando para checar se há mais comentários que antes")
            # print(saved_post)
        self.web_driver.open_all_comments()
        post_html = self.web_driver.get_post_html()
        if post_html:
            scraping_result =self.scraper.scrape_post_text(
                post_html, tag, self.json_manager, saved_post)
            if scraping_result is False:
                return False
        """have_next_post = self.web_driver.go_to_next_post()
        if have_next_post is None:
            # fim dos posts
            return None
        elif have_next_post is False:
            # erro inesperado
            return False"""
        return True

    def scrape_posts_text_v1(self, tag, num_posts=10000000000):
        still_posts = True
        current_post_number = 0
        while still_posts == True and current_post_number < num_posts:
            if current_post_number == 0:
                posts_range = 72
            else:
                self.web_driver.close_post()
                self.web_driver.load_next_posts()  # carrega mais posts
                self.web_driver.go_to_nth_post(current_post_number)
                posts_range = 96
            for _ in range(posts_range):
                current_post_number += 1
                print(f"raspando o post nº {current_post_number}")
                result = self.scrape_post_text(tag)
                if result is None:
                    # fim dos posts
                    print(f"fim dos posts com a tag {tag}")
                    still_posts = False
                    break
                elif result is False:
                    # erro inesperado
                    print(
                        "erro inesperado em scrape_post_text ao avançar para o próximo post")
                    still_posts = False
                    break
            
        print(f"raspagem da tag {tag} terminada")
        print(f"foram raspados {current_post_number} posts")

    def scrape_posts_text_v2(self, tag, num_posts=10000000000):
        #vai post por post, foca no post, salva seu html, entra nele, extrai os dados, sai do post e vai pro próximo
        current_post_number = 0
        current_post_href = self.web_driver.focus_first_post()
        self.web_driver.click_on_first_post()
        self.scrape_post_text(tag)
        self.web_driver.close_post()
        while current_post_number < num_posts:
            current_post_href = self.web_driver.focus_on_next_post(current_post_href, tag)
            if current_post_href is None or current_post_href is False or current_post_href == "":
                break
            self.web_driver.click_on_next_post(current_post_href)
            print(f"raspando o post nº {current_post_number + 2}")
            self.scrape_post_text(tag)
            self.web_driver.close_post()
            current_post_number += 1
        print(f"raspagem da tag {tag} terminada")

    def scrape_posts_text_v3(self, tag, num_posts=10000000000):
        #vai post por post, foca no post, salva seu html, entra nele, extrai os dados, sai do post e vai pro próximo
        current_post_number = 0
        self.web_driver.click_on_first_post()
        self.scrape_post_text(tag)
        while current_post_number < num_posts:
            print(f"raspando o post nº {current_post_number + 1}")
            scraping_result = self.scrape_post_text(tag)
            if scraping_result is None or scraping_result is False:
                break
            current_post_number += 1
            still_have_posts = self.web_driver.go_to_next_post()
            if still_have_posts is None or still_have_posts is False:
                break
        print(f"raspagem da tag {tag} terminada")

    def get_saved_tags(self):
        return self.web_driver.tag_saver.get_saved_tags()

    def merge_posts(self, output_filename="merged_posts_data.json"):
        self.json_manager.merge_jsons(output_filename)

    def traverse_posts(self):
        self.web_driver.click_on_first_post()
        while self.web_driver.go_to_next_post():
            pass

    def normalize_jsons(self):
        self.json_manager.normalize_jsons()
