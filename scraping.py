from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd


# Configuração do serviço do WebDriver
service = Service(ChromeDriverManager().install())

# Inicializa o navegador automatizado.
browser = webdriver.Chrome(service=service)
browser.maximize_window()

browser.get('https://www.reclameaqui.com.br')

# Rola a página 600 pixels para baixo.
browser.execute_script("window.scrollBy(0, 1250);")
sleep(2)

# Clica na categoria "Moda" no ranking.
moda_button_xpath = '/html/body/astro-island[6]/section[1]/div[1]/div[2]/nav[1]/div[2]/button[2]'
moda_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, moda_button_xpath)))
moda_button.click()
sleep(2)

# Lista para armazenar os dados.
dados_empresas = []

# Busca e itera os 3 primeiros resultados em "Melhores Empresas.
for i in range(1, 4):
    moda_button_xpath = '/html/body/astro-island[6]/section[1]/div[1]/div[2]/nav[1]/div[2]/button[2]'
    moda_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, moda_button_xpath)))
    moda_button.click()
    
    empresa_xpath = f'(/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[1]//a)[{i}]'
    empresa = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, empresa_xpath)))
    empresa.click()
    sleep(2)

    # Extrai os dados e percentuais.
    detalhes = BeautifulSoup(browser.page_source, 'html.parser').find(
        'div', attrs={'id': 'reputation'})
    score_element = detalhes.find('span', class_='score')
    score = score_element.get_text(strip=True)

    percentuais = {}
    for p in detalhes.find_all('p'):
        label = p.text.strip()
        bar_container = p.find_next(
            'div', class_='sc-9xbj9-0 eOujtY bar-container', title=True)
        percentual = bar_container.find('span', class_='label').text.strip()
        percentuais[label] = percentual

    # Imprime os dados coletados.
    print("Score:", score)
    print("Reclamações Respondidas:", percentuais.get('Reclamações respondidas'))
    print("Voltariam a fazer negócio:",
          percentuais.get('Voltariam a fazer negócio'))
    print("Índice de Solução:", percentuais.get('Índice de solução'))
    print("Nota do Consumidor:", percentuais.get('Nota do consumidor'))

     
    nome_empresa_xpath = '/html/body/div[4]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]/h1'
    nome_empresa = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, nome_empresa_xpath))).text

    # Armazena os dados em um dicionário.
    dados_empresa = {
        "Empresa": nome_empresa,
        "Score": score,
        "Reclamações Respondidas": percentuais.get('Reclamações respondidas'),
        "Voltariam a fazer negócio": percentuais.get('Voltariam a fazer negócio'),
        "Índice de Solução": percentuais.get('Índice de solução'),
        "Nota do Consumidor": percentuais.get('Nota do consumidor')
    }

    # Adiciona o dicionário à lista.
    dados_empresas.append(dados_empresa)

    # Volta para a página anterior.
    browser.back()
    sleep(2)


# Lista e itera os 3 primeiros resultados em "Piores Empresas".
for i in range(1, 4):
    moda_button_xpath = '/html/body/astro-island[6]/section[1]/div[1]/div[2]/nav[1]/div[2]/button[2]'
    moda_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, moda_button_xpath)))
    moda_button.click()
    
    empresa_xpath = f'(/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[2]//a)[{i}]'
    empresa = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, empresa_xpath)))
    empresa.click()
    sleep(2)

    # Extrai os dados e percentuais.
    detalhes = BeautifulSoup(browser.page_source, 'html.parser').find(
        'div', attrs={'id': 'reputation'})
    score_element = detalhes.find('span', class_='score')
    score = score_element.get_text(strip=True)

    percentuais = {}
    for p in detalhes.find_all('p'):
        label = p.text.strip()
        bar_container = p.find_next(
            'div', class_='sc-9xbj9-0 eOujtY bar-container', title=True)
        percentual = bar_container.find('span', class_='label').text.strip()
        percentuais[label] = percentual

    # Imprime os dados coletados.
    print("Score:", score)
    print("Reclamações Respondidas:", percentuais.get('Reclamações respondidas'))
    print("Voltariam a fazer negócio:",
          percentuais.get('Voltariam a fazer negócio'))
    print("Índice de Solução:", percentuais.get('Índice de solução'))
    print("Nota do Consumidor:", percentuais.get('Nota do consumidor'))

    
    nome_empresa_xpath = '/html/body/div[4]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]/h1'
    nome_empresa = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, nome_empresa_xpath))).text

    # Armazena os dados em um dicionário.
    dados_empresa = {
        "Empresa": nome_empresa,
        "Score": score,
        "Reclamações Respondidas": percentuais.get('Reclamações respondidas'),
        "Voltariam a fazer negócio": percentuais.get('Voltariam a fazer negócio'),
        "Índice de Solução": percentuais.get('Índice de solução'),
        "Nota do Consumidor": percentuais.get('Nota do consumidor')
    }

    # Adiciona o dicionário à lista
    dados_empresas.append(dados_empresa)

    # Voltar para a página anterior.
    browser.back()
    sleep(2)

# Criar um DataFrame no Pandas.
df = pd.DataFrame(dados_empresas)

# Salva o DataFrame em um arquivo CSV e Excel.
df.to_excel("dados_empresas_reclameaqui.xlsx", index=False)

# Exibe o DataFrame.
print(df)

# Fecha o navegador.
browser.quit()
