#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: This is the main file for the program that will be used to scrape the website and save the data in a json file or csv





import json
import requests
from bs4 import BeautifulSoup
import re
import json
import bs4
import pandas as pd


# FLAGS:

# Tor Setup
TOR_FLAG = False





# TODO
# support sessions by checking for stored staff info and if they don't exist then get them from the website --Completed
# For each web request, save the outputed HTML file for future use and mining and to also reduce network traffic
# Tor connection option for the program to anonymize the traffic and avoid detection -- Completed
# setting up the session (visited urls )  -- Completed



visited_urls = open('log/visited_urls', 'r').read().split('\n')




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
    
    
    
# Checking for tor connection 
requests = get_tor_session()




# TESTS

def test_tor():
    import requests
    print('Original IP ADDRESS')
    print(requests.get("http://httpbin.org/ip").text)
    requests = get_tor_session()
    print('Hidden IP ADDRESS')
    print(requests.get("http://httpbin.org/ip").text)
 
# testing tor connection 
#test_tor()

# HOW TO:
# 
# 1. run setup_initial_links() to get the links to the staff members
# 2. for each link in the outputed json file run add_staff(link)
# 3. Add an exit condition to the loop to stop the program when you have added all the staff members
# 4. 



# a master array to store all the staff members
All_STAFF_INFOMATION = []




def visited(url):

        with open('log/visited_urls', 'a') as file:
            file.write(url + '\n')


# This is an interesting function because I discovered that I can save SOOOO much time by parsing the javascript code
# of the website because it contains the links to the staff members
def setup_initial_links():
    print('Setting up initial links')
    # getting the initial links from the website
    url = 'https://pages.charlotte.edu/connections/'
    visited(url)
    # fetching the html file
    response = requests.get(url)
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
        links[tag.text] = tag.get('href')

    print('converting to json the json file\n')
    array = [ {'name' : i, 'link' : links[i]} for i in links]
    # print(array)
    # print(json.dumps(array))
    
    #printing the links for debugging
    print('links set up successfully')
    print('\n')
    
    
    
    
    write_file('log/staff_links.json', array)
    links_df = pd.DataFrame(columns=["name", "link"], data=links.items() , index=None)
    links_df.to_csv('log/staff_links.csv', index=False)
    
    return links_df





# To retrieve the staff members's information from the website
def get_information(url):
    visited(url)
    # making a request to the website
    response = requests.get(url)
    # saving the log file
    write_file('log/http_log.txt', response.text)
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



# to add the staff members to the an array to be written to a csv or a json file
def add_staff(url):
    try:
        print('Adding staff')
        new_staff = get_information(url)
        All_STAFF_INFOMATION.append(new_staff)
        print(new_staff['name'] +  ' added successfully')
        
        
    except Exception as e:
        print('error adding staff')
        print(e)
    
def write_file(filename, data):
    try:
        with open(filename, 'a') as file:
            json.dump(data, file, indent=4  )
#            file.write(data)
            print(filename + ' written successfully')
    except Exception as e:
        print('Error writing ' + filename)
        print(e)


def read_file(filename):
    try:
        data = open(filename, 'r').readlines()
        print('File read successfully')
        return data
    except Exception as e:
        print('Error reading file')
        print(e)




# to get the links from the json file (DEPRECATED)
def convert_to_json(collection):
    try:
        array = []
        for i in collection:
            value = {i : collection[i]}
            array.append(value)
        print('Converted to json')
        
        return array
    except Exception as e:
        print('Error converting to json')
        print(e) 
        

def get_all_links(links, limit):
    original_df = pd.read_csv('log/staff_info.csv')
    for i in range(0, limit):
        url = links[i]
        visited(url)    
        add_staff(url)
        write_file('log/outputlog.txt', All_STAFF_INFOMATION)     
        write_file('log/staff_info.json', All_STAFF_INFOMATION)
        staff = {
            
        }

            
            
        staff_info_df = pd.DataFrame(All_STAFF_INFOMATION)    
        staff_info_df =staff_info_df.append(original_df)
        staff_info_df.to_csv('log/staff_info.csv', index=False)

        print(str(All_STAFF_INFOMATION.__len__() )+ ' staff members added for a total of ' + str(len(staff_info_df) ))



# Filter the links to remove the ones that have already been visited

def filter_visited():
    links = pd.read_csv('log/staff_links.csv').get('link').astype(str).tolist()
    print(links)
    filtered_links = []
    for link in links:
        if   link not in visited_urls:
            filtered_links.append(link)   
    return filtered_links



setup_initial_links()

# removing the visited links from the links
filtered_links = filter_visited()
# to query information from the website with a stop condition
get_all_links(filtered_links, 500)

# This is the main function that will be called to get the links to the staff members


# testing the convert_to_json function
original_df = pd.read_csv('log/staff_info.csv')
original_df.to_json('log/staff_info.json'  , orient='records')

