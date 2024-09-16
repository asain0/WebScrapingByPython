import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import product

def get_page_content(url, headers, parameters):
  response = requests.get(url, headers = headers, params = parameters ).text
  soup = BeautifulSoup(response, 'html.parser')
  return soup

def parse_athletes(soup):
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
    photo =photo_cell.find('img')['src']
    points = points_cell.get_text(strip=True)
    rank =  rank_cell.get_text(strip=True)

    athlete = {
        'photo': photo,
        'name': name,
        'details': details,
        'points': points,
        'rank': rank
    }
    athletes.append(athlete)
  return athletes

DOMAIN = 'https://ibjjf.com'
URL = f'{DOMAIN}//2024-athletes-ranking'
HEADER = {'USER-AGENT':'Mozilla/5.0'}
PARAMETERS = {
    'utf8':'✓',
    'filters[s]':'ranking-geral-gi',
    'filters[ranking_category]':'adult',
    'filters[gender]':'male',
    'filters[belt]':'black',
    'filters[weight]': None,
    'page': 2
}

page = 140
all_athletes = []
while True:
  PARAMETERS['page']= page

  soup_athletes = get_page_content(URL,HEADER,PARAMETERS)
  athletes= parse_athletes(soup_athletes)
  if athletes is None :
    break
  print(page)
  all_athletes.extend(athletes)
  page +=1

df_athletes = pd.json_normalize(all_athletes)

excel_file = 'C:\\asain\\EstudosDev\\Python\\webscraping\\athletes.xlsx'

arquivo = open(excel_file,"w")
arquivo.write("Arquivo Criado")
arquivo.close()

df_athletes.to_excel(excel_file, index=False)