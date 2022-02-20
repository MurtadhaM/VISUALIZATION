#!/usr/bin/env python3.10
from bs2json import bs2json
import crawled 
import json
import json
import requests
from bs4 import BeautifulSoup
import re
import parse
import concurrent.futures
import json
import bs4
import cdata
import HTMLParser
import parser





filename = 'staff_links.json'
staff_links = []
# Get the text from a class name


def write_to_file(data, filename):
    with open(filename, 'w') as f:
        f.write(str(data))



response = requests.get(url)
soup = BeautifulSoup(response, 'lxml')
script = soup.html.find('script', type="CDATA").decode("utf-8")
write_to_file(script, filename)
def process_page(links):
    if(link in completed_links):
        return None
    else:
        'Welcome to the club, ' + link + '!'
p = BeautifulSoup(response, 'lxml').find_all('div', class_ = 'field-items')
for i in soup: staff_links.append(i.find('a') ['href'])
for i in staff_links: 
    response = requests.get(i) 
    soup = BeautifulSoup(response, 'lxml') 
    name = soup.find('h1', class_ = 'page-title').text 
    print(name) 
    soup = soup.find('div', class_ = 'field-items') 
    soup = soup.find_all('div', class_ = 'field-item') 
    for i in soup: 
        if i.text.strip() == 'Email Address': 
            email = i.find('a') ['href'] 
        elif i.text.strip() == 'Phone Number': phone = i.find('a') ['href'] 
        elif i.text.strip() == 'Website': website = i.find('a') ['href'] 
        print(email, phone, website) 
        data = f'{name}\n{email}\n{phone}\n{website}\n\n' 
        write_to_file(data, '[-LINKS_DATA.TXT') 
        name = soup.find('h1', class_ = 'page-title').text
        
        
        