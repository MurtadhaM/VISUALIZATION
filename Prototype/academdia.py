#!/usr/bin/env python3.10
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import time
# getting articles and scholarily links from the website
# all of RESEARCH OF UNCC https://ninercommons.charlotte.edu/islandora/search/?type=dismax


def write_file(filename, data):
    try:
        with open(filename, 'a') as file:
            file.write(str(data))
            print(filename + ' written successfully')
    except Exception as e:
        print('Error writing ' + filename)
        print(e)
        
def scholars_fetch():
    print('Setting up initial links')
    url = 'https://ninercommons.charlotte.edu/islandora/object/ir:scholars'
        # fetching the html file
    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'lxml')
    print('parsing elements to extract links')

    scholars  =  soup.find_all('dt',  {'class' : 'islandora-object-thumb'} )


    scholars_links = {
        
        
        'scholar' : "https://ninercommons.charlotte.edu/islandora/object/",
    }

    for scholar in scholars:
        scholars_links[scholar.find('a').get('title')] =  'https://ninercommons.charlotte.edu' + scholar.find('a').get('href').replace('%3A', ':') 

    scholar_pd = pd.DataFrame(columns=['scholar_name', 'scholar_link'], data=scholars_links.items())
    scholar_pd.to_csv('log/scholars_links.csv', index=False)
    write_file('log/http_log_scholars.txt' ,scholar_pd)



def departments_fetch():
    print('Setting up links links')
    url = 'https://pages.charlotte.edu/connections/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'lxml')
    print('parsing elements to extract links')
    colleges  =  soup.find_all('div',  {'id' : 'collapscat-2'} )
    links = {
        
    }
    for value in colleges:
        for tag in value.find_all('a'):   
             if 'group' in tag.get('href'):
                 links[tag.text] =  tag.get('href')
        
        
    group_pd = pd.DataFrame(columns=['group', 'link'], data=links.items())
    group_pd.to_csv('log/group_links.csv', index=False)

    print(links)
    return links

#links_fetch()


def topic_fetch():
    departments = departments_fetch()
    group_links = departments.values()
    names = departments.keys()
    
    
    for  names ,url  in departments.items():
        try:
            print('fetching topics for group' + names)
            print(url)
            soup  = BeautifulSoup(requests.get(url).text, 'html.parser')
            
            values = soup.find('input', attrs={'class', 'tags'})['value']

            topics = re.findall('"name":"(.*?)",', values)

            counts = re.findall('"count":(.*?),"', values)

            urls = re.findall('"url":"(.*?)"}', values)
            header = ['College', 'Topic', 'Count', 'URL']
            print(str(counts) + "\n" + str(topics) + "\n" + str(urls))             

            with open('log/topics.csv', 'a+', encoding='UTF8', newline = '') as f:

                writer = csv.writer(f)

                for i in range(len(topics)):

                    infoForRows = []

                    infoForRows.append(names  )
                    infoForRows.append(topics[i])
                    infoForRows.append(counts[i])
                    infoForRows.append(urls[i])

                    writer.writerow(infoForRows)
        except Exception as e:
            print(e)

topic_fetch()