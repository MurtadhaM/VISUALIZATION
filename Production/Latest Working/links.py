#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: Collect all staff links




# This is an interesting function because I discovered that I can save SOOOO much time by parsing the javascript code
# of the website because it contains the links to the staff members
import json
import pandas as pd
import requests as request
from bs4 import BeautifulSoup

def setup_initial_links():
    print('Setting up initial links')
    # getting the initial links from the website
    url = 'https://pages.charlotte.edu/connections/'
    # fetching the html file
    response = request.get(url)
    soup = BeautifulSoup(response.text , 'lxml')
    script = soup.html.find_all('script')
    html_links = ''
    print('parsing elements to extract links')
    for elem in script:
        if elem.text.find('collapsing categories item') != -1:
            for line in elem.text.split('\n'):
                if line.find('href') != -1:
                    html_links += line.split(' = ')[1].replace('\\\'', '\"' ).replace(';', '').replace('\'', '')                
    s = BeautifulSoup(html_links, 'html.parser')
    links = {
        
   
     }
    
    anchor = s.find_all('a')
    for  tag in anchor:
        if 'people' in tag.get('href'):
            links[tag.text] = tag.get('href')

    print('converting to json the json file\n')
    array = [ {'name' : i, 'link' : links[i]} for i in links]
    # print(array)
    # print(json.dumps(array))
    
    #printing the links for debugging
    print('links set up successfully')
    print('\n')
    
    
    with open('links.json', 'w') as file:
        file.write(json.dumps(array))       
    links_df = pd.DataFrame(columns=["name", "link"], data=links.items() , index=None)
    links_df.to_csv('links_data.csv', index=False)   
    pd.DataFrame(data=links.values(), index=None, columns=['links']).to_csv('links.csv', index=False)
    return links_df




setup_initial_links()
