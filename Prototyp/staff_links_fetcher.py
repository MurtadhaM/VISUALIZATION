#!/usr/bin/env python3.10
#import visited 
import json
import requests
from bs4 import BeautifulSoup
import re
import parse
import json
import bs4
import js2py
import pandas as pd


# getting the initial links from the website
url = 'https://pages.charlotte.edu/connections/'
# fetching the html file
response = requests.get(url)
soup = BeautifulSoup(response.text , 'lxml')
script = soup.html.find_all('script')
html_links = ''
for elem in script:
    if elem.text.find('collapsing categories item') != -1:
        for line in elem.text.split('\n'):
            if line.find('href') != -1:
                html_links += line.split(' = ')[1].replace('\\\'', '\"' ).replace(';', '').replace('\'', '')                
s = BeautifulSoup(html_links, 'html.parser')
for attr in s:
        print(attr.find('a').get('href'))
        print(attr.find('a').get('title'))
# defining the information for each staff member
staff_member = dict(
     name = '',
     department = '',
     bio = '',
     link = '',
     academic_interests = ''
     
)

# adding the links to the list
# adding the name of the staff to the list
STAFF = pd.DataFrame( data=staff_member, columns=['name', 'link', 'interests', 'department', 'bio'] , index=[1,2,3,4,5,6,7])  



staff_member['name'] = 'name'
staff_member['department'] = 'department'
staff_member['bio'] = 'bio'


def get_information(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text , 'lxml')
    department = soup.find('div', class_='connection-groups').text
    academic_interests = soup.find('div', class_='connection-links columns-2').text
    bio = soup.find('div', class_='post-contents').text
    
    print(department, academic_interests, bio)
    staff_member['department'] = department
    staff_member['academic_interests'] = academic_interests
    staff_member['bio'] = bio
    return staff_member



print(STAFF)
get_information('https://pages.charlotte.edu/connections/people/bjnoble/')



def add_staff(staff):
    try:
     
        STAFF.append(staff.name . staff. staff.link . staff.interests . staff.department . staff.bio)
        print('Staff added successfully')
    except:
        print('error adding a staff to csv') 
add_staff(staff_member)
     
print(STAFF)  
     
     
     
    
    
