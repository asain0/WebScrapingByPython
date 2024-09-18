import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import product

def get_page_content(url, headers, parameters):
  response = requests.get(url, headers = headers, params = parameters ).text
  soup = BeautifulSoup(response, 'html.parser')
  return soup

def parse_athletes(soup, kimono, category, gender, belt, division):
  table = soup.find('table')
  if not table:
    return None
  athletes =[]
  rows = table.find_all('tr')
  if not rows:
    return None
  for row in rows:
    photo_cell = row.find('td',class_= 'photo reduced')
    name_cell = row.find('td', class_ = 'name-academy')
    points_cell = row.find('td', class_='pontuation')
    rank_cell = row.find('td', class_='position')
    name_tag = name_cell.find('div', class_= "name").find('a')

    name = name_tag.get_text(strip=True)
    details = DOMAIN + name_tag['href']

    photo = photo_cell.find('img')['src'] if photo_cell and photo_cell.find('img') else 'Sem foto Disponível'
    points = points_cell.get_text(strip=True)
    rank =  rank_cell.get_text(strip=True)

    athlete = {
        'photo': photo,
        'name': name,
        'details': details,
        'points': points,
        'rank': rank,
        'kimono': kimono,
        'category': category,
        'gender': gender,
        'belt': belt,
        'division': division
    }
    athletes.append(athlete)
  return athletes

def list_filters(soup, filter_id):
  filters = soup.find(id=filter_id).find_all('option')
  return [item['value'] for item in filters[1:]]

DOMAIN = 'https://ibjjf.com'
URL = f'{DOMAIN}//2024-athletes-ranking'
HEADER = {'Uer-Agent':'Mozilla/5.0'}
PARAMETERS = {
    'utf8':'✓',
    'filters[s]':'ranking-geral-gi',
    'filters[ranking_category]':'adult',
    'filters[gender]':'male',
    'filters[belt]':'black',
    'filters[weight]': None,
    'page': 1
}

soup_filters = get_page_content(URL,HEADER,PARAMETERS)

kimono = list_filters(soup_filters, 'filters_s')
category = list_filters(soup_filters, 'filters_ranking_category')
gender = list_filters(soup_filters, 'filters_gender')
belt = list_filters(soup_filters, 'filters_belt')
division = list_filters(soup_filters, 'weight_filter')

all_athletes = []

for k, c, g,b,d in product(kimono, category, gender, belt, division):
  page = 1  
  while True:
    print(f'Scraping: {k}, {c}, {g}, {b}, {d} for page {page}')
    PARAMETERS['filters[s]'] = k
    PARAMETERS['filters[ranking_category]'] = c
    PARAMETERS['filters[gender]'] = g
    PARAMETERS['filters[belt]'] = b
    PARAMETERS['filters[weight]'] = d
    PARAMETERS['page']= page
    soup_athletes = get_page_content(URL,HEADER,PARAMETERS)
    athletes= parse_athletes(soup_athletes, k,c,g,b,d)
    if athletes is None :
      break
    all_athletes.extend(athletes)
    page +=1


df_athletes = pd.json_normalize(all_athletes)

excel_file = 'C:\\athletes.xlsx'

arquivo = open(excel_file,"w")
arquivo.write("Arquivo Criado")
arquivo.close()

df_athletes.to_excel(excel_file, index=False)
