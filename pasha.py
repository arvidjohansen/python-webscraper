import requests
from bs4 import BeautifulSoup

url = 'https://no.wikipedia.org/wiki/Liste_over_norske_videreg%C3%A5ende_skoler'

r = requests.get(url)

soup = BeautifulSoup(r.text)

element = input('Hvilket element ønsker du å vise?')

data = soup.find(element)

print(data.text)