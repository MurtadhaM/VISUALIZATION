#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: This is the main file for the program that will be used to scrape the website and save the data in a json file or csv





import json
import requests
from bs4 import BeautifulSoup
import re
import parse
import json
import bs4
import js2py
import pandas as pd


# TODO
# support sessions by checking for stored staff info and if they don't exist then get them from the website
# For each web request, save the outputed HTML file for future use and mining and to also reduce network traffic

# setting up the session (visited urls ) 

visited = open('log/visited_urls', 'r').read()


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
    
    write_file('log/javascript_script.js', script)
    
    
    write_file('log/staff_links.json', array)
    return links





# To retrieve the staff members's information from the website
def get_information(url):
    visited(url)
    response = requests.get(url)
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
    staff_member['academic_interests'] = academic_interests
    staff_member['bio'] = bio
    
    
    return staff_member



# to add the staff members to the an array to be written to a csv or a json file
def add_staff(url):
    try:
        print('Adding staff')
        new_staff = get_information(url)
        All_STAFF_INFOMATION.append(new_staff)
        write_file('log/staff_info.json', All_STAFF_INFOMATION)
        print('Staff added successfully')
    except:
        print('error adding a staff to csv') 

def write_file(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            print('File written successfully')
    except Exception as e:
        print('Error writing file')
        print(e)


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            print('File read successfully')
            return data
    except Exception as e:
        print('Error reading file')




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
        



# FOR TESTING PURPOSES
add_staff('https://pages.charlotte.edu/connections/people/aturovli')
add_staff('https://pages.charlotte.edu/connections/people/fmili')
print(All_STAFF_INFOMATION)


