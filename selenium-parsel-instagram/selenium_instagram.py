from Facade import Facade
from Driver_initializer import Driver_initializer
from FileLogger import FileLogger


def main():
    logger = FileLogger("log.txt")
    driver = Driver_initializer.config_chrome_driver()
    # driver que permite que o Selenium tome açoes
    wait = Driver_initializer.config_wait(driver, 15)
    # tempo de espera máximo para encontrar elementos Web
    # hashtags = ['#uece', '#uecevest'] + \[f'#uece{year}' for year in range(2000, 2027)]
    accounts = ['@uece', '@uecedadepressao', '@uecealunos']
    # searches = ['uece']
    tag_inputs = []
    # tag_inputs.append(hashtags)
    tag_inputs.append(accounts)
    # tag_inputs.append(searches)
    # tags para raspar
    num_posts = 5000
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
                if tag_result == "Already saved":  # tag já foi raspada
                    continue
                tag = instagram_text_scraper.get_current_tag()
                instagram_text_scraper.scrape_posts_text(num_posts, tag)
                print(instagram_text_scraper.web_driver.tag_saver.get_saved_tags())

    tags = instagram_text_scraper.get_saved_tags()
    instagram_text_scraper.merge_posts(tags)
    logger.close()
    driver.quit()

desc_facade = '*Último dia para inscrição no Vestibular 2026.1 da Uece*\n\nA Uece recebe somente até esta sexta-feira, 12 de setembro, as inscrições para o Vestibular 2026.1, exclusivamente pelo site da CEV/Uece.\n\nPara efetivar a inscrição, é necessário anexar, em formato PDF, um documento oficial de identidade com foto, o histórico escolar do Ensino Médio e, para os candidatos que concorrerem pelo sistema de cotas sociais, o comprovante de renda.\n\nAqueles que optarem por vagas reservadas às cotas PPIQ (pretos, pardos, indígenas e quilombolas) também devem enviar o termo de autodeclaração devidamente preenchido. Todos os detalhes sobre documentação, regras, cronograma e programas de provas estão disponíveis no Edital Nº 04/2025-CEV/UECE, publicado no site da CEV, em https://www.cev.uece.br/vestibular20261/\n\n*Datas das provas*\n\nA primeira fase do Vestibular 2026.1 será realizada no dia 12 de outubro de 2025, em um domingo, com prova de conhecimentos gerais.\n\nJá a segunda fase do vestibular ocorrerá em dois dias, com aplicação da prova de redação e das provas específicas: o primeiro dia será 30 de novembro e o segundo dia, 1º de dezembro de 2025.\n\n#uece'
desc_scraper = '*Último dia para inscrição no Vestibular 2026.1 da Uece*A Uece recebe somente até esta sexta-feira, 12 de setembro, as inscrições para o Vestibular 2026.1, exclusivamente pelo site da CEV/Uece.Para efetivar a inscrição, é necessário anexar, em formato PDF, um documento oficial de identidade com foto, o histórico escolar do Ensino Médio e, para os candidatos que concorrerem pelo sistema de cotas sociais, o comprovante de renda. Aqueles que optarem por vagas reservadas às cotas PPIQ (pretos, pardos, indígenas e quilombolas) também devem enviar o termo de autodeclaração devidamente preenchido. Todos os detalhes sobre documentação, regras, cronograma e programas de provas estão disponíveis no Edital Nº 04/2025-CEV/UECE, publicado no site da CEV, em https://www.cev.uece.br/vestibular20261/*Datas das provas*A primeira fase do Vestibular 2026.1 será realizada no dia 12 de outubro de 2025, em um domingo, com prova de conhecimentos gerais.Já a segunda fase do vestibular ocorrerá em dois dias, com aplicação da prova de redação e das provas específicas: o primeiro dia será 30 de novembro e o segundo dia, 1º de dezembro de 2025.#uece'
print()
main()

# a partir do ~=276 post, começa a se repetir
