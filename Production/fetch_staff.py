#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: This is the main file for the program that will be used to scrape the website and save the data in a json file or csv

import json
import requests
from bs4 import BeautifulSoup
import re
import json

# FLAGS:

# Tor Setup
TOR_FLAG = False

# TODO
# support sessions by checking for stored staff info and if they don't exist then get them from the website --Completed
# For each web request, save the outputed HTML file for future use and mining and to also reduce network traffic
# Tor connection option for the program to anonymize the traffic and avoid detection -- Completed
# setting up the session (visited urls )  -- Completed

# visited_urls = open('log/visited_urls', 'r').read().split('\n')


# first start tor service on port 9050 by running the command:
# tor SocksPort 9050
def get_tor_session():
    import requests
    if TOR_FLAG:
        
        print('enabling tor')
        # check if tor is running
        try:
            
            session = requests.session()
            
            # Tor uses the 9050 port as the default socks port
            session.proxies = {'http':  'socks5://127.0.0.1:9050',
                            'https': 'socks5://127.0.0.1:9050'}
            
            current_ip = session.request('GET', 'http://httpbin.org/ip').text
            print('tor session established with IP ' + current_ip.split('origin')[1])
            
            return session 
        except Exception as e:
            print(e)
            print('Error getting tor session')
            print('Please make sure tor is running or disable the TOR_FLAG')
            print('Exiting program')
            exit()   
        return session
    else:
        print('tor not enabled')
        return requests


departments = {'Belk College of Business': {}, 'College of Arts & Architecture': {}, 'College of Computing & Informatics': {}, 'College of Education': {}, 'College of Health & Human Services': {}, 'College of Liberal Arts & Sciences': {}, 'Lee College of Engineering': {}, 'School of Data Science (SDS)':{}}
# = ['Belk College of Business','College of Arts & Architecture','College of Computing & Informatics','College of Education','College of Health & Human Services','College of Liberal Arts & Sciences','Lee College of Engineering','School of Data Science (SDS)']
departments['Belk College of Business'] = {'Business Info Systems/Operations': {}, 'Economics ': {}, 'Finance ': {}, 'Management ': {}, 'Marketing ': {}, 'Turner School of Accountancy':{}}
departments['College of Arts & Architecture'] = {'Art & Art History': {}, 'Dance': {}, 'Music': {}, 'Performing Arts Services': {}, 'School of Architecture': {}, 'TheatreBrook Muller':{}}
departments['College of Computing & Informatics'] = {'Bioinformatics and Genomics' : {}, 'Bioinformatics Research Center ': {}, 'Computer Science ': {}, 'Software & Information Systems':{}}
departments['College of Education'] = {'Counseling': {}, 'Ctr For STEM Education': {}, 'Educational Leadership': {}, 'Middle Grades Secondary & K-12': {}, 'Reading & Elementary ED': {}, 'School & Community Partnerships': {}, 'Special Ed & Child Dev':{}}
departments['College of Health & Human Services'] = {'Kinesiology': {}, 'Public Health Sciences': {}, 'School of Nursing': {}, 'School of Social Work':{}}
departments['College of Liberal Arts & Sciences'] = {'Africana Studies': {}, 'Anthropology': {}, 'Biological Sciences': {}, 'Chemistry': {}, 'Communication Studies': {}, 'Criminal Justice and Criminology': {}, 'English': {}, 'Geography and Earth Sciences': {}, 'Global Studies': {}, 'History': {}, 'Languages and Culture Studies': {}, 'Mathematics and Statistics': {}, 'Philosophy': {}, 'Physics and Optical Science': {}, 'Political Science and Public Administration': {}, 'Psychological Science': {}, 'Religious Studies': {}, 'Sociology': {}, 'Writing, Rhetoric, and Digital Studies':{}}
departments['Lee College of Engineering'] = {'Civil and Environmental Engr': {}, 'Electrical & Computer Engineering': {}, 'Engineering Tech & Constr Mgmt': {}, 'EPIC': {}, 'Mech Engineering & Engineering Sci': {}, 'Student Dev & Success': {}, 'Systems Engin & Engin Management':{}}
departments['School of Data Science (SDS)'] = {}


def departments_fetch():
    print('Setting up links links')
    url = 'https://pages.charlotte.edu/connections/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'lxml')
    print('parsing elements to extract links')
    colleges = soup.find_all('div', {'id' : 'collapscat-2'})
    links = {
        
    }
    
    for value in departments:
        for tag in value.g('a'):   
            # print(value.find_all('a')[0].text)
            if 'group' in tag.get('href'):
                links[tag.text] = tag.get('href')
                # Appending the links to the dictionary
                for t in ['Belk College of Business', 'College of Arts & Architecture', 'College of Computing & Informatics', 'College of Education', 'College of Health & Human Services', 'College of Liberal Arts & Sciences', 'Lee College of Engineering', 'School of Data Science (SDS)']:
                    for p in departments[t].keys():
                        if str(p).strip() in tag.text:
                            departments[t][p]['links'] = tag.get('href')
    return departments                        
    
    
# Checking for tor connection 
requests = get_tor_session()



# departments = departments_fetch()    

# setup_initial_links()
# to print the links in the json file
# print(json.dumps(departments))
    
    





# To retrieve the staff members's information from the website
def get_information(url):
    # making a request to the website
    response = requests.get(url)
    # saving the log file
    soup = BeautifulSoup(response.text , 'lxml')
    department = soup.find('div', class_='connection-groups').text.strip()
    academic_interests = soup.find('div', class_='connection-links columns-2').text.strip()
    name = soup.find('div', class_='page-title').text.strip()
    bio = soup.find('div', class_='post-contents').text.strip()
    link = url
    staff_member = {}
    staff_member['link'] = link
    staff_member['name'] = name
    staff_member['department'] = department
    staff_member['academic_interests'] = academic_interests.replace('\n', ' ')
    staff_member['bio'] = bio.replace('\n', ' ')
    
    
    return staff_member

    
def setup_crawing():
    
    response = requests.get('https://pages.charlotte.edu/connections/group')
    soap = BeautifulSoup(response.content, 'lxml')
    for value in departments:
        for tag in value.g('a'):   
            if 'group' in tag.get('href'):
                
                # Appending the links to the dictionary
                for t in ['Belk College of Business', 'College of Arts & Architecture', 'College of Computing & Informatics', 'College of Education', 'College of Health & Human Services', 'College of Liberal Arts & Sciences', 'Lee College of Engineering', 'School of Data Science (SDS)']:
                    for p in departments[t].keys():
                        if str(p).strip() in tag.text:
                            departments[t][p]['links'] = tag.get('href')
    return departments                        





            
setup_crawing()
    
#print(anchor)
# To get the links for stafff:
# DATA SCIENCE:

# collapsItems['collapsCat-5698:2']

# Lee College of Engineering
# collapsItems['collapsCat-2104:2']

# College of Liberal Arts & Sciences
# collapsItems['collapsCat-1846:2']

# College of Health & Human Services
# collapsItems['collapsCat-13:2']

# College of Education
# collapsItems['collapsCat-4271:2']
# College of Computing & Informatics
# collapsItems['collapsCat-1914:2']

# College of Arts + Architecture

# collapsItems['collapsCat-2097:2']

# Belk College of Business

# collapsItems['collapsCat-48:2']

