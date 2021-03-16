import os
import datetime
import re
import requests
import time

from collections import namedtuple
from bs4 import BeautifulSoup

#static variables
SLEEP_INTERVAL = 10

Site = namedtuple('Site', ['name','url','filename','function_name'])

SITES = [
    Site('VG','https://www.vg.no','vg.txt', 'get_headlines_vg'),
    Site('NRK','https://www.nrk.no','nrk.txt', 'get_headlines_nrk'),
    Site('DB','https://www.db.no','db.txt', 'get_headlines_nrk'),
    Site('ITAV','https://itavisen.no','itavisen.txt', 'get_headlines_nrk'),
]

class SiteParser():
    @staticmethod
    def write_headline_to_file(overskrift, filename):
        with open(filename,'a') as log_file:
            log_file.write(overskrift.strip()+'\n')

    @staticmethod
    def process_headlines(headlines, sitename, filename):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
        
        #create the file if it dont exist
        try: open(filename) 
        except FileNotFoundError: open(filename,'w').close()

        #load all existing headlines
        existing_headlines = []
        with open(filename) as log_file:
            for headline in log_file.readlines():
                existing_headlines.append(headline.strip())
        
        #loop over current headlines and write new ones to file
        for o in headlines:
            o = o.strip()
            if o in existing_headlines:
                #headline exists, skip
                continue
            #new headline; alert and write to file
            print(f'{timestamp} ({sitename}): {o}')
            SiteParser.write_headline_to_file(o, filename)
                
    @staticmethod
    def _get_soup(url):
        r = requests.get(url)
        if r.encoding == 'ISO-8859-1':
            r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')
        return soup

    @staticmethod
    def get_headlines_vg(url):
        soup = SiteParser._get_soup(url)
        overskrifter = soup.find_all('h3',class_='headline')
        processed_headlines = [] #gather new headlines here
        for o in overskrifter:
            processed_headlines.append(o.text.replace('\n',' '))
        return processed_headlines
    
    @staticmethod
    def get_headlines_nrk(url):
        soup = SiteParser._get_soup(url)
        headlines_h3 = soup.find_all('h3') #remove new line
        processed_headlines = [] #gather new headlines here

        for o in headlines_h3:
            o = o.text.strip().replace('\n',' ').strip()
            o = re.sub(r'\s+', ' ',o) #remove multiple spaces
            processed_headlines.append(o)
            
        headlines_h2 = soup.find_all('h2')
        for o in headlines_h2:
            o = o.text.strip().replace('\n',' ').strip() #remove new line
            o = re.sub(r'\s+', ' ',o) #remove multiple spaces
            processed_headlines.append(o)
           
        return processed_headlines

KEEP_GOING=True
if __name__ == '__main__':
    os.system('cls') #clear screen
    
    print(f'Checking for new articles at {SLEEP_INTERVAL} second intervals...')

    while KEEP_GOING:
        for site in SITES:
            #call the designated function to fetch the headlines
            site_headlines = getattr(SiteParser, site.function_name)(site.url)
            #process headlines and write to file
            SiteParser.process_headlines(site_headlines, site.name, site.filename) 
        #sleep when sites have been updated    
        time.sleep(SLEEP_INTERVAL)
        