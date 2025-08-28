from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import json
from lxml import etree
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from Facade import Facade
#TODO: abrir respostas, abrir novos posts ao chegar ao final
#atributos globais
driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = Options()
)
wait = WebDriverWait(driver, 30)
tag = "#uece"
num_posts = 5000 #numero desejado de posts a serem extraidos
url = 'https://www.instagram.com/'


def main():
    instagram_text_scraper = Facade(driver, wait, tag)
    instagram_text_scraper.login()
    instagram_text_scraper.go_to_posts()
    instagram_text_scraper.scrape_posts_text(num_posts)
    input()

def main_2():
    instagram_text_scraper = Facade(driver, wait, tag)
    instagram_text_scraper.login()
    instagram_text_scraper.go_to_posts()
    instagram_text_scraper.traverse_posts()

main_2()