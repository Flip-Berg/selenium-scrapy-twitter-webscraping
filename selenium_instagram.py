from Facade import Facade
from Driver_initializer import Driver_initializer

def main():
    driver = Driver_initializer.config_driver() 
    #driver que permite que o Selenium tome açoes
    wait = Driver_initializer.config_wait(driver, 15) 
    #tempo de espera máximo para encontrar elementos Web
    hashtags = ['#uece', '#uecevest', (f'#uece{year}' for year in range(2000, 2026))]
    accounts = ['@uece', '@uecedadepressao', '@uecealunos']
    tag_inputs = []
    tag_inputs.append(hashtags)
    tag_inputs.append(accounts)
    #tags para raspar
    num_posts = 1
    #numero desejado de posts de cada tag a serem extraidos
    url = 'https://www.instagram.com/' 
    #url para login

    instagram_text_scraper = Facade(driver, wait, tag_inputs)
    instagram_text_scraper.login(url)
    for tag_group in tag_inputs:
        for tag in tag_group:
            #TODO: consertar lógica para marcar as tags já raspadas
            #TODO: criar arquivos com nome da tag atual e não input da tag
            #TODO: salvar todas as tags corretamente
            tag_index=0
            while instagram_text_scraper.go_to_posts_by_tag(tag, tag_index) is not False:
                instagram_text_scraper.scrape_posts_text(num_posts, tag)
                tag_index += 1


main()