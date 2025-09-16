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
        # self.web_driver.load_all_posts()
        self.web_driver.click_on_first_post()
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
        post_description.replace('\n', '')
        print("Descrição do post(facade):")
        print(repr(post_description))
        saved_post = self.json_manager.check_if_post_is_saved(
            tag, post_description, True)
        if saved_post:
            print(
                "Post já salvo anteriormente, escaneando para checar se há mais comentários que antes")
            print(saved_post)
        self.web_driver.open_all_comments()
        post_html = self.web_driver.get_post_html()
        if post_html:
            self.scraper.scrape_post_text(
                post_html, tag, self.json_manager, saved_post)
        have_next_post = self.web_driver.go_to_next_post()
        if have_next_post is None:
            # fim dos posts
            return None
        elif have_next_post is False:
            # erro inesperado
            return False
        return True

    def scrape_posts_text(self, num_posts, tag):
        for post in range(num_posts):
            print(f"raspando o post nº {post+1}")
            result = self.scrape_post_text(tag)
            if result is None:
                # fim dos posts
                print(f"fim dos posts com a tag {tag}")
                break
            elif result is False:
                # erro inesperado
                print(
                    "erro inesperado em scrape_post_text ao avançar para o próximo post")
                break
        print(f"raspagem da tag {tag} terminada")
        print(f"foram raspados {post+1} posts")

    def get_saved_tags(self):
        return self.web_driver.tag_saver.get_saved_tags()

    def merge_posts(self, tags, output_filename="merged_posts_data.json"):
        self.json_manager.merge_jsons(tags, output_filename)

    def traverse_posts(self):
        while self.web_driver.go_to_next_post():
            pass
