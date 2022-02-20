# -*- coding: utf-8 -*-
# Author: Murtadha Marzouq
# Description: This is the Person Class File

import json
import requests
from bs4 import BeautifulSoup
from pandasql import sqldf 
import pandas as pd




# TODO
# support sessions by checking for stored staff info and if they don't exist then get them from the website --Completed
# For each web request, save the outputed HTML file for future use and mining and to also reduce network traffic
# Tor connection option for the program to anonymize the traffic and avoid detection -- Completed
# setting up the session (visited urls )  -- Completed

# visited_urls = open('log/visited_urls', 'r').read().split('\n')


# a master array to store all the staff members
All_STAFF_INFOMATION = []
TOR_FLAG = False

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






# setting i[ the people's array]
people = []

urls = pd.read_csv('links_data_filtered.csv')['links'].dropna().tolist()
UNCC = {'Belk College of Business': {}, 'College of Arts + Architecture': {}, 'College of Computing & Informatics': {}, 'College of Education': {}, 'College of Health & Human Services': {}, 'College of Liberal Arts & Sciences': {}, 'Lee College of Engineering': {}}
UNCC['Belk College of Business'] = {'Business Info Systems/Operations': {}, 'Economics': {}, 'Finance': {}, 'Management': {}, 'Marketing': {}, 'Turner School of Accountancy':{}}
UNCC['College of Arts + Architecture'] = {'Art & Art History': {}, 'Dance': {}, 'Music': {}, 'Performing Arts Services': {}, 'School of Architecture': {}, 'TheatreBrook Muller':{}}
UNCC['College of Computing & Informatics'] = {'Bioinformatics and Genomics' : {}, 'Bioinformatics Research Center': {}, 'Computer Science': {}, 'Software & Information Systems':{}, 'School of Data Science (SDS)': {}}
UNCC['College of Education'] = {'Counseling': {}, 'Ctr For STEM Education': {}, 'Educational Leadership': {}, 'Middle Grades Secondary & K-12': {}, 'Reading & Elementary ED': {}, 'School & Community Partnerships': {}, 'Special Ed & Child Dev':{}}
UNCC['College of Health & Human Services'] = {'Kinesiology': {}, 'Public Health Sciences': {}, 'School of Nursing': {}, 'School of Social Work':{}}
UNCC['College of Liberal Arts & Sciences'] = {'Africana Studies': {}, 'Anthropology': {}, 'Biological Sciences': {}, 'Chemistry': {}, 'Communication Studies': {}, 'Criminal Justice and Criminology': {}, 'English': {}, 'Geography and Earth Sciences': {}, 'Global Studies': {}, 'History': {}, 'Languages and Culture Studies': {}, 'Mathematics and Statistics': {}, 'Philosophy': {}, 'Physics and Optical Science': {}, 'Political Science and Public Administration': {}, 'Psychological Science': {}, 'Religious Studies': {}, 'Sociology': {}, 'Writing, Rhetoric, and Digital Studies':{}}
UNCC['Lee College of Engineering'] = {'Civil and Environmental Engr': {}, 'Electrical & Computer Engineering': {}, 'Engineering Tech & Constr Mgmt': {}, 'EPIC': {}, 'Mech Engineering & Engineering Sci': {}, 'Student Dev & Success': {}, 'Systems Engin & Engin Management':{}}

#UNCC['School of Data Science (SDS)'] = {}
# # Setting up the user fields
# for colleges in UNCC.keys():
#     for departments in UNCC[colleges]:
#         UNCC[colleges][departments] = []
        
def get_college(department):
        try:
            if department in UNCC.keys():
                return department
            for key in UNCC.keys():
                for subkey in UNCC[key].keys():
                    if department in subkey:
                        return key
                
                
            return " "
        except Exception as e:
            print(e)       
class Person :

    def __init__(self, link):
        self.name = " "
        self.academic_interests = ""
        self.department = " "
        self.bio = " "
        self.link = link
        self.college = " "
        
        # fetching the information from the website
        self.get_info()
        #self.college = get_college(self.department) 

        
    
    def __str__(self):
        try:
            return json.dumps(self.__dict__)
        except Exception as e:
            print(e)
    
    # @param: the department of the staff member
    # @return: the college of the staff member
    # @param: the department of the staff member
    # @return: the college of the staff member
    def get_college(self,department):
        try:
            if department in UNCC.keys():
                return department
            for key in UNCC.keys():
                for subkey in UNCC[key].keys():
                    if department == subkey:
                        return key
                
                
            return " "
        except Exception as e:
            print(e)
            
            
    def get_info(self):
        url = self.link
        # making a request to the website
        response = requests.get(url)
        # saving the log file
        soup = BeautifulSoup(response.text , 'html.parser')
        department = soup.find('div', class_='connection-groups').text.strip().split('\n')[0]
        academic_interests = soup.find('div', class_='connection-links columns-2')
        name = soup.find('div', class_='page-title').text.strip()
        bio = soup.find('div', class_='post-contents').text
        link = url
        
        # assigning the values to the class variables
        self.name = name
        self.department = department
        self.academic_interests = academic_interests.text.split('\n')
        self.college = self.get_college(department)
        self.link = link
        # CASTING THE BIO TO STRING
        self.bio = bio.replace('\n', ' ').replace('\u00a0', '').replace('\u201c', '')
        
def query_csv(csv_file, query):
    pysqldf = lambda q: sqldf(q, globals())
    output = pysqldf(query)
    return output

def visited_update(url): 
    # remove the url from the file
     
    for link in  pd.read_csv('links_data_filtered.csv')['links'].dropna().tolist():
        if link == url:
            # print(link)
            urls.pop(urls.index(link))
    
    return urls
    
def get_json():
    # json.dumps([UNCC])
    return json.dumps([UNCC])  # json.dumps([person.__dict__ for person in people])



def get_all_links(links , limit):
           #for debugging
    #links = ['https://pages.charlotte.edu/connections/people/cwaites/', 'https://pages.charlotte.edu/connections/people/ewahler1/','https://pages.charlotte.edu/connections/people/jean-claude-thill/', 'https://pages.charlotte.edu/connections/people/bmuller7/' ,'https://pages.charlotte.edu/connections/people/astefan1/']
    try:
        for i in range(limit) :
            print(links[i])
            visited_update(links[i])
            person_added = Person(links[i]) 
            print(person_added)   
            people.append(person_added)   
            log_data()
    except Exception as e:
        print(e)
    # removing the entries that are already added    
    pd.DataFrame(urls , columns=['links'], index=None).to_csv('links_data_filtered.csv', index=None)
    
# reads the data to a json file    
def read_UNCC():
    # Reads the data to a json file
    json_file = open('staff_data.json', 'r').readline(
)
    return json.loads(json_file)
       
def log_data():    
    with open('log.json', 'w') as f:
        print('writing to log.json')
        add_to_UNCC()
        f.write(json.dumps([UNCC]))
# save the data to a json file    
def save_UNCC():
    # Save the data to a json file
    with open('staff_data.json', 'w') as f:
        f.write(json.dumps([UNCC]))
        
# Adds the data to the master json file


def add_to_UNCC():
    try:
        for p in people:
            if len(p.college) > 2 and len(p.department) > 2 and p.department  != p.college and p.college != " ":
                #print('the person is : ' + p.name + ' and the department is : ' + p.department + ' and the college is : ' + p.college)
                UNCC[p.college][p.department][p.name] = ({ 'link' : p.link, 'bio' : p.bio, 'academic_interests': p.academic_interests  , 'college' : p.college, 'department' : p.department})
            elif  p.college  in UNCC.keys() :
                UNCC[p.college][p.name] = ({ 'link' : p.link, 'bio' : p.bio, 'academic_interests': p.academic_interests  , 'college' : p.college, 'department' : p.department})
        return json.dumps([UNCC])        
    except Exception as e:
        print(e.with_traceback) 
        print('error adding to UNCC')
        exit()

# I will do 50 at a time to avoid overloading UNCC Servers
staff_links = pd.read_csv('links.csv').drop_duplicates()['links'].dropna().tolist()


def start():
    # Starting the application
    # get staff information
    get_all_links(staff_links, len(staff_links))
    # update file
    add_to_UNCC()
    # save file
    save_UNCC()
# startin the application    
    
# startin the application
start()
save_UNCC()

#print([UNCC])