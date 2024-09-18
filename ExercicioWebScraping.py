import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import product
import time

MAX_RETRIES = 10
WAIT_TIME = 30  # segundos
FILE_PATH = 'C:'

def get_page_content(url, headers, parameters):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, headers=headers, params=parameters)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            else:
                print(f'Erro na requisição({retries + 1}). Código de status: {response.status_code}')
                print(f'URL: {response.url}')
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
        
        retries += 1
        time.sleep(WAIT_TIME)

    print("Número máximo de tentativas alcançado.")
    return None

def extract_news_data(row):
    photo_cell = row.find('div', class_='widget--info__media-container')
    info_cell = row.find('div', class_='widget--info__text-container')

    if info_cell is None:
        return None

    news_title = info_cell.find('div', class_='widget--info__title').get_text(strip=True)
    news_link = info_cell.find('a')['href']
    news_summary = info_cell.find('p', class_='widget--info__description').get_text(strip=True, default='Sem resumo')
    news_photo = photo_cell.find('img')['src'] if photo_cell and photo_cell.find('img') else 'Sem foto disponível'

    return {
        'titulo': news_title,
        'link': news_link,
        'resumo': news_summary,
        'foto': news_photo
    }

def get_news(url, header, parameters, keywords):
    news = []
    for keyword in keywords:
        page = 1
        while True:
            print(f'Consulta termo "{keyword}", página {page}')
            parameters['page'] = page
            parameters['q'] = keyword

            soup_news = get_page_content(url, header, parameters)

            if not soup_news:
                break  

            empty_row = soup_news.find('ul', class_='results__list').find_all('li', class_='widget widget--no-results')
            if empty_row:
                print('Nenhuma notícia encontrada!')
                break

            rows = soup_news.find('ul', class_='results__list').find_all('li')

            for row in rows:
                news_item = extract_news_data(row)
                if news_item:
                    news_item['termo'] = keyword 
                    news.append(news_item)

            page += 1

    return news

# Configurações gerais
DOMAIN = 'https://site.desejado.com.br'
URL = f'{DOMAIN}/busca/'
HEADER = {'User-Agent': 'Mozilla/5.0'}
PARAMETERS = {
    'q': '',
    'order': 'recent',
    'from': '2024-01-01T00:00:00-0300',
    'to': '2024-12-31T23:59:59-0300',
    'page': 1
}
keywords = ['lista_de_termos']

news_list = get_news(URL, HEADER, PARAMETERS, keywords)

if news_list:
    print(f'{len(news_list)} notícias encontradas!')
    df_noticias = pd.json_normalize(news_list)

    excel_file = f'{FILE_PATH}\\dados.xlsx'
    df_noticias.to_excel(excel_file, index=False)
    print('Consulta finalizada e dados salvos!')
else:
    print('Nenhuma notícia foi encontrada.')
