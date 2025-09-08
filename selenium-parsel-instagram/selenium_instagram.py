from Facade import Facade
from Driver_initializer import Driver_initializer

def main():
    driver = Driver_initializer.config_chrome_driver() 
    #driver que permite que o Selenium tome açoes
    wait = Driver_initializer.config_wait(driver, 15) 
    #tempo de espera máximo para encontrar elementos Web
    hashtags = ['#uece', '#uecevest'] + [f'#uece{year}' for year in range(2000, 2027)]
    accounts = ['@uece', '@uecedadepressao', '@uecealunos']
    #searches = ['uece']
    tag_inputs = ["#hollowknight"]
    #tag_inputs.append(hashtags)
    #tag_inputs.append(accounts)
    #tag_inputs.append(searches)
    #tags para raspar
    num_posts = 2
    #numero desejado de posts de cada tag a serem extraidos
    url = 'https://www.instagram.com/' 
    #url para login

    instagram_text_scraper = Facade(driver, wait, tag_inputs)
    instagram_text_scraper.login(url)
    for tag_inputs_group in tag_inputs:
        for tag_input in tag_inputs_group:
            #TODO: identificar se o post já foi raspado
            tag_index=0
            while (tag_result := instagram_text_scraper.go_to_posts_by_tag(tag_input, tag_index)) is not False:
                tag_index += 1
                if tag_result == "Already saved": #tag já foi raspada
                    continue
                tag = instagram_text_scraper.get_current_tag()
                instagram_text_scraper.scrape_posts_text(num_posts, tag)
                print(instagram_text_scraper.web_driver.tag_saver.get_saved_tags())

    tags = instagram_text_scraper.get_saved_tags()
    instagram_text_scraper.merge_posts(tags)

main()