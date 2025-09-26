from bs4 import BeautifulSoup
import json
import requests
import pandas as pd

url = 'https://www.imdb.com/pt/chart/moviemeter/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
data = json.loads(soup.find('script', type='application/ld+json').string)

tabelaTudo = []

for i in range(len(data['itemListElement'])):
    tabela = {}
    tabela['Título'] = data['itemListElement'][i].get('item').get('name')
    if data['itemListElement'][i].get('item').get('aggregateRating') == None:
        tabela['avaliação'] = "Sem avaliação"
        tabela['Quantidade de avaliação'] = "Sem avaliação"
    else:
        tabela['avaliação'] = data['itemListElement'][i].get('item').get('aggregateRating').get('ratingValue')
        tabela['Quantidade de avaliação'] = data['itemListElement'][i].get('item').get('aggregateRating').get('ratingCount')
    if data['itemListElement'][i].get('item').get('genre') == None:
        tabela['Gêneros'] = "Sem gêneros"
    else:
        tabela['Gêneros'] = data['itemListElement'][i].get('item').get('genre')
    if data['itemListElement'][i].get('item').get('contentRating') == None:
        tabela['Classificação Indicativa'] = "Sem classificação indicativa"
    else:
        tabela['Classificação Indicativa'] = data['itemListElement'][i].get('item').get('contentRating')
    if data['itemListElement'][i].get('item').get('duration') == None:
        tabela['Duração'] = "Sem duração"
    else:
        tabela['Duração'] = data['itemListElement'][i].get('item').get('duration').replace('PT', '')
    tabelaTudo.append(tabela)

df = pd.DataFrame(tabelaTudo)
df.to_csv("movies.cvs", index=False)