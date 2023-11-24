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

# Instancia a classe.
class ReclameAquiScraper:
    def __init__(self, browser):
        self.browser = browser

# Extrai os dados da categoria Moda.
    def extract_data(self, categoria_xpath, empresa_xpath):
        # Espera até que o botão seja clicável.
        moda_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, categoria_xpath)))
        moda_button.click()

        empresa = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, empresa_xpath)))
        empresa.click()
        sleep(2)

# Utiliza o Beautiful Soup para análisar o código e extrair os dados.
        detalhes = BeautifulSoup(self.browser.page_source, 'html.parser').find(
            'div', attrs={'id': 'reputation'})
        
        #Extrai o Score.
        score_element = detalhes.find('span', class_='score')
        score = score_element.get_text(strip=True)

# Cria um dicionário para armazenar os percentuais.
        percentuais = {}
        for p in detalhes.find_all('p'):
            label = p.text.strip()
            bar_container = p.find_next(
                'div', class_='sc-9xbj9-0 eOujtY bar-container', title=True)
            percentual = bar_container.find('span', class_='label').text.strip()
            percentuais[label] = percentual

# Extrai o nome da empresa.
        nome_empresa_xpath = '/html/body/div[4]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]/h1'
        nome_empresa = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, nome_empresa_xpath))).text

# Compila os dados extraídos em um dicionário.
        dados_empresa = {
            "Empresa": nome_empresa,
            "Score": score,
            "Reclamações Respondidas": percentuais.get('Reclamações respondidas'),
            "Voltariam a fazer negócio": percentuais.get('Voltariam a fazer negócio'),
            "Índice de Solução": percentuais.get('Índice de solução'),
            "Nota do Consumidor": percentuais.get('Nota do consumidor')
        }

        self.browser.back()
        sleep(2)

        return dados_empresa
    
# Executa o método de scraping.
    def run_scraper(self):
        dados_empresas = []

# Loop para extrair dados das Melhores Empresas.
        for i in range(1, 4):
            categoria_xpath = '/html/body/astro-island[6]/section[1]/div[1]/div[2]/nav[1]/div[2]/button[2]'
            empresa_xpath = f'(/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[1]//a)[{i}]'
            dados_empresa = self.extract_data(categoria_xpath, empresa_xpath)
            dados_empresas.append(dados_empresa)

# Loop para extrair dados das Piores Empresas.
        for i in range(1, 4):
            categoria_xpath = '/html/body/astro-island[6]/section[1]/div[1]/div[2]/nav[1]/div[2]/button[2]'
            empresa_xpath = f'(/html/body/astro-island[6]/section/div/div[2]/div[3]/div/div[2]//a)[{i}]'
            dados_empresa = self.extract_data(categoria_xpath, empresa_xpath)
            dados_empresas.append(dados_empresa)

        # Cria um DataFrame no Pandas.
        df = pd.DataFrame(dados_empresas)

        # Salva o DataFrame em um arquivo Excel.
        df.to_excel("dados_empresas_reclameaqui.xlsx", index=False)

        # Exibe o DataFrame.
        print(df)

# Instancia a classe ReclameAquiScraper e executa o scraper.
scraper = ReclameAquiScraper(browser)
scraper.run_scraper()

# Fecha o navegador.
browser.quit()
