import requests
from bs4 import BeautifulSoup
url = 'https://no.wikipedia.org/wiki/Liste_over_norske_videreg%C3%A5ende_skoler'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table', class_='wikitable sortable')
tbody = table.find('tbody')

rows = tbody.find_all('tr')
rows = rows[1:]

for row in rows:
    row = row.find_all('td')
    navn = row[0].text.strip()
    sted = row[1].text.strip()
    fylke = row[2].text.strip()
    studieplasser = row[4].text.strip()
    vigo_kode = row[6].text.strip()
    print(f'Navn: {navn} sted: {sted} studieplasser: {studieplasser} vigo: {vigo_kode}')