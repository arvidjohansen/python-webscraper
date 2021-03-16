import os
import datetime
import re
import requests
import time

from collections import namedtuple
from bs4 import BeautifulSoup

Site = namedtuple('Site', ['name','url','filename','function_name'])

SITES = [
    #Site('VG','https://www.vg.no','vg.txt', 'fetch_headlines_vg'),
    #Site('NRK','https://www.nrk.no','nrk.txt', 'fetch_headlines_nrk'),
    Site('DB','https://www.db.no','db.txt', 'get_headlines_db'),
]

class SiteParser():

    @staticmethod
    def _fetch_soup(url):
        r = requests.get(url)
        print(r.encoding)
        if r.encoding == 'ISO-8859-1':
            r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')
        return soup

    @staticmethod
    def fetch_headlines_nrk(url):
        soup = SiteParser._fetch_soup(url)
        headlines_h3 = soup.find_all('h3')
        processed_headlines = [] #gather new headlines here

        for o in headlines_h3:
            o = o.text.strip().replace('\n',' ').strip()
            o = re.sub(r'\s+', ' ',o)
            processed_headlines.append(o)
            print(o)

        headlines_h2 = soup.find_all('h2')
        for o in headlines_h2:
            o = o.text.strip().replace('\n',' ').strip()
            o = re.sub(r'\s+', ' ',o)
            processed_headlines.append(o)
            print(o)

        
        return processed_headlines

keep_going=True
if __name__ == '__main__':
    #os.system('cls') #clear screen
 
    for site in SITES:
        url = site.url
        site_headlines = SiteParser.fetch_headlines_nrk(url)
        #print(site_headlines)
        #SiteParser.process_headlines(site_headlines, site.name, site.filename) #fix
    
        