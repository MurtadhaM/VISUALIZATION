
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json

COLLEGE_ABBRS = ['college-of-business', 'college-of-arts-and-architecture', 'cci', 'coed', 'chhs', 'clas', 'college-of-engineering', 'school-of-data-science-sds']

class ContainerDict:
    def __init__(self, containerParams):
        self.tag = containerParams['tag']
        self.class_ = containerParams['class_']

class PageScrapeConfig:
    def __init__(self, containerParams):
        ''' 
        :param str key_container: key html 'tag' type and 'class_' 
        :param dict val_containers: list of dicts with 'tag' and 'class_' converted to ContainerDict object
        :param bool vals_are_link_text: true if vals are hyperlink text within container
        :param bool vals_are_links: true if getting the link itself
        :param bool outer_container: if there is an outer container for keys and vals this is that container's html 'tag' type and 'class_'
        '''
        self.key_container = ContainerDict(containerParams['key_container'])
        self.val_containers = [ContainerDict(val_params) for val_params in containerParams['val_containers']]
        self.vals_are_link_text = False if not 'vals_are_link_text' in containerParams else containerParams['vals_are_link_text']
        self.vals_are_links = False if not 'vals_are_links' in containerParams else containerParams['vals_are_links']
        self.outer_container = False if not 'outer_container' in containerParams else ContainerDict(containerParams['outer_container'])

def get_key(soup, tag, class_):
    key = soup.find(tag, class_)
    if key:
        return key.text
    elif soup and soup.text:
        return soup.text
    else:
        print('no key found')
        return None

def get_elements(soup, pageScrapeConfig):
    try:
        key = get_key(soup, pageScrapeConfig.key_container.tag, class_ = pageScrapeConfig.key_container.class_)
        vals = []
        if pageScrapeConfig.vals_are_link_text:
            for val_container in pageScrapeConfig.val_containers:
                val_soup = soup.find(val_container.tag, class_=val_container.class_)
                for val in val_soup.find_all('a'):
                    if val.text:
                        vals.append(val.text)
        elif pageScrapeConfig.vals_are_links:
            vals = [a['href'] for a in soup.select('a', href=True) if not a['href'].startswith('mailto')]
            if len(vals) == 0 and soup.has_attr('href'):
                vals = soup['href']
        else:
            for val_container in pageScrapeConfig.val_containers:
                for val in soup.find_all(val_container.tag, class_=val_container.class_):
                    print(val)
                    if val.text:
                        vals.append(val.text)
        return key, vals
    except Exception as e:
        print('get_elements exception')
        print(e)
        return False, False

def get_page_dict_outer(soup, pageScrapeConfig):
    '''
    :param BeautifulSoup soup:
    :param PageScrapeConfig pageScrapeConfig:
    '''
    pageDict = dict()
    if pageScrapeConfig.outer_container:
        outer_containers = soup.find_all(pageScrapeConfig.outer_container.tag, class_ = pageScrapeConfig.outer_container.class_)
        for div in outer_containers:
            key, vals = get_elements(div, pageScrapeConfig)
            if key and vals:
                pageDict[key] = vals
    else:
        key, vals = get_elements(soup, pageScrapeConfig)
        if key and vals:
            pageDict[key] = vals
    return pageDict

def createCollegeDict(college_abbr):
    link_to_pages = 'https://pages.charlotte.edu/connections/group/%s/page/' % college_abbr
    return get_faculty_names_dict(link_to_pages)

def get_faculty_names_dict(link):
    group = {'tag':'div', 'class_':'connection-links-container'}
    interests = {'tag':'div', 'class_':'connection-groups'}
    name = {'tag':'div', 'class_':'connection-groups'}
    outer_container = {'tag':'div', 'class_':'post connection'}
    params = {
        'key_container': name,
        'val_containers': [group, interests],
        'vals_are_link_text': True,
        'outer_container': outer_container
        }
    containerParams = PageScrapeConfig(params)
    outputDict, total_pages = get_all_pages(link, containerParams)
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

def main():
    colleges_dict = dict.fromkeys(COLLEGE_ABBRS)
    for college_abbr in COLLEGE_ABBRS:
        colleges_dict[college_abbr], total_pages = createCollegeDict(college_abbr)
        print(' college:\t%s\n total pages:\t%d' % (college_abbr, total_pages))
    make_json('sample', colleges_dict)

if __name__ == '__main__':
    main()