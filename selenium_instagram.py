from Facade import Facade
from Driver_initializer import Driver_initializer

def main():
    driver = Driver_initializer.config_driver() 
    #driver que permite que o Selenium tome açoes
    wait = Driver_initializer.config_wait(driver, 15) 
    #tempo de espera máximo para encontrar elementos Web
    tags = ["#uece", "@uece"] 
    #tags para raspar
    num_posts = 2 
    #numero desejado de posts de cada tag a serem extraidos
    url = 'https://www.instagram.com/' 
    #url para login

    instagram_text_scraper = Facade(driver, wait, tags)
    instagram_text_scraper.login(url)
    for tag in tags:
        if instagram_text_scraper.go_to_posts_by_tag(tag) is False:
            continue
        instagram_text_scraper.scrape_posts_text(num_posts, tag)

main()