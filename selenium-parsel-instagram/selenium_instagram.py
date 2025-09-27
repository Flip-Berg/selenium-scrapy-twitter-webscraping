from Facade import Facade
from Driver_initializer import Driver_initializer
from FileLogger import FileLogger


def main():
    logger = FileLogger("log.txt")
    driver = Driver_initializer.config_chrome_driver()
    # driver que permite que o Selenium tome açoes
    wait = Driver_initializer.config_wait(driver, 15)
    # tempo de espera máximo para encontrar elementos Web
    hashtags = ['#uece', '#uecevest'] + [f'#uece{year}' for year in range(2000, 2027)]
    accounts = ['@uece', '@uecedadepressao', '@uecealunos']
    # searches = ['uece']
    tag_inputs = []
    tag_inputs.append(hashtags)
    tag_inputs.append(accounts)
    # tag_inputs.append(searches)
    # tags para raspar
    # numero desejado de posts de cada tag a serem extraidos
    url = 'https://www.instagram.com/'
    # url para login

    instagram_text_scraper = Facade(driver, wait, tag_inputs)
    instagram_text_scraper.login(url)
    for tag_inputs_group in tag_inputs:
        for tag_input in tag_inputs_group:
            tag_index = 0
            while (tag_result := instagram_text_scraper.go_to_posts_by_tag(tag_input, tag_index)) is not False:
                tag_index += 1
                if tag_result == "Already saved":  # tag já foi raspada nessa run
                    continue
                tag = instagram_text_scraper.get_current_tag()
                #instagram_text_scraper.traverse_posts()
                if tag_input.startswith("#"):
                    num_posts = 500
                else: 
                    num_posts = 10000000
                instagram_text_scraper.scrape_posts_text_v3(tag, num_posts)
                #print(instagram_text_scraper.web_driver.tag_saver.get_saved_tags())

    instagram_text_scraper.merge_posts("merged_uece")
    logger.close()
    driver.quit()


main()
# a partir do ~=276 ou ~=185 post, começa a se repetir

