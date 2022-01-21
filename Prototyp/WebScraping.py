
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json

import visited_links.json


COLLEGE_ABBRS = ['college-of-business', 'college-of-arts-and-architecture', 'cci', 'coed', 'chhs', 'clas', 'college-of-engineering', 'school-of-data-science-sds']

filename = 'links.json'
staff_links = []
def get_faculty_names_dict(link):
    group = {'tag':'div', 'class_':'connection-links-container'}
    interests = {'tag':'div', 'class_':'connection-groups'}
    name = {'tag':'div', 'class_':'connection-groups'}
    outer_container = {'tag':'div', 'class_':'post connection'}
    params = {
        'key_container': name,
        'key_container': name,
        'val_containers': [group, interests],
        'vals_are_link_text': True,
        'outer_container': outer_container
        }
    
    
    return outputDict, total_pages

def get_soup(link):
    html_response = requests.get(link)
    html_text = html_response.content
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

def get_all_pages(link, pageScrapeConfig):
    '''
    :param str link:
    :param PageScrapeConfig pageScrapeConfig:
    '''
    page_exists = True
    page_num = 1
    allPagesDict = dict()
    while page_exists:
        link_to_page = '%s%d/' % (link, page_num)
        try:
            get_soup(link_to_page)
            page_results_dict = get_page_dict_outer(soup, pageScrapeConfig)
            if len(page_results_dict) < 1:
                page_exists = False
                continue
            else:
                allPagesDict.update(page_results_dict)
            page_num += 1
        except Exception as e:
            print('pages found %d' % (page_num-1))
            print(e)
            page_exists = False
    return allPagesDict, page_num-1 # total pages

def make_json(name, jsonData):
    json_object = json.dumps(jsonData, indent=4)
    with open('%s.json' % name, 'w') as outfile:
        outfile.write(json_object)

