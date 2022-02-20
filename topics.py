# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: This file contains the functions to fetch the topics from the website.

import json
import requests
from bs4 import BeautifulSoup
import re


# Preparing the dictionary
urls_arr = ['Belk College of Business ','https://pages.charlotte.edu/connections/group/cci/' ,'College of Arts + Architecture','https://pages.charlotte.edu/connections/group/chhs/' ,'College of Computing & Informatics','https://pages.charlotte.edu/connections/group/clas/' ,'College of Education ','https://pages.charlotte.edu/connections/group/coed/' ,'College of Health & Human Services','https://pages.charlotte.edu/connections/group/college-of-arts-and-architecture/' ,'College of Liberal Arts & Sciences','https://pages.charlotte.edu/connections/group/college-of-business/' ,'Lee College of Engineering','https://pages.charlotte.edu/connections/group/college-of-engineering/' ,'School of Data Science (SDS)','https://pages.charlotte.edu/connections/group/school-of-data-science-sds/']
departments =urls_arr[::2]
urls =urls_arr[1::2]
topics_group = {
    }

def topic_fetch(department , url):
    '''
    Fetches the topics from the given url and stores it in a dictionary.
    :param department: The department for which the topics are to be fetched.
    :param url: The url from which the topics are to be fetched.
    :return: A dictionary containing the topics and their respective counts.
    '''
    try:
            soup  = BeautifulSoup(requests.get(url).text, 'html.parser')         
            values = soup.find('input', attrs={'class', 'tags'})['value']
            topics = re.findall('"name":"(.*?)",', values)
            counts = re.findall('"count":(.*?),"', values)
            urls = re.findall('"url":"(.*?)"}', values)
            # populating the dictionary
            for i in range(len(topics)):
                topics_group[department][topics[i]] = {
                    'count': counts[i],
                    'url': urls[i].replace('\\/', '/')
                }
    except Exception as e:
            print(e.args)
    return topics_group       
for department, url in zip(departments, urls):
    topics_group[department] = {}
    topic_fetch(department, url)

# Writing the dictionary to a json file    
with open('logs/topics_group.json', 'w') as f:
        f.write(json.dumps(topics_group))    
print(json.dumps(topics_group, indent=4))
