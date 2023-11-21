import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep

service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=service)


browser.get('https://www.reclameaqui.com.br')

sleep(2)

browser.find_element('xpath','//*[@id="homeRankings"]/div/div[2]/nav/div[2]/button[2]').click()

sleep(2)


browser.find_element('xpath', '//*[@id="homeRankings"]/div/div[2]/div[3]/div/div[1]/a[1]').click()

sleep(4)

page_content = browser.page_source

site = BeautifulSoup(page_content, 'html.parser')

detalhes = site.find('div', attrs={'id': 'reputation'})

print(detalhes.prettify())

score_element = detalhes.find('span', class_='score')
score = score_element.get_text(strip=True)

print("Score:", score)

percentuais = {}

for p in detalhes.find_all('p'):
    label = p.text.strip()
    bar_container = p.find_next('div', class_='sc-9xbj9-0 eOujtY bar-container', title=True)
    percentual = bar_container.find('span', class_='label').text.strip()
    percentuais[label] = percentual

print("Reclamações Respondidas:", percentuais.get('Reclamações respondidas'))
print("Voltariam a fazer negócio:", percentuais.get('Voltariam a fazer negócio'))
print("Índice de Solução:", percentuais.get('Índice de solução'))
print("Nota do Consumidor:", percentuais.get('Nota do consumidor'))

browser.back()
sleep(2)