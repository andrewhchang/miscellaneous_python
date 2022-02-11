import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.coronavirus.vic.gov.au/victorian-coronavirus-covid-19-data')
soup = BeautifulSoup(page.content, 'html.parser')

stat_items = soup.find_all(class_='ch-daily-update__statistics-item')

for item in stat_items:
    stat_title = item.find(class_='ch-daily-update__statistics-item-text').string
    stat_desc = item.find(class_='ch-daily-update__statistics-item-description').string
    joined_str = stat_title + ' ' + stat_desc
    print (joined_str)
    
