#!/usr/bin/env python3.10
from bs2json import bs2json
import visited 
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
import visited_links.json



'Welcome to the club, ' + link + '!'


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
    if(link in visited_links):
        return None
    else:
        completed_links.append(link)
        return link
print(p)


file = open('staff_linksjson', 'rw')    
data = json.load(file)  

print(file)









