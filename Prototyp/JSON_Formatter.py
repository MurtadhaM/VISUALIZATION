import json 
import csv
import requests
import BeautifulSoup as BeautifulSoup
colleges_dict = {'William States Lee College of Engineering', 'Belk College of Business', 'College of Computing & Informatics','William States Lee College of Engineering', 'Cato College of Education','College of Health and Human Services', 'College of Arts + Architecture', 'College of Liberal Arts and Sciences'}



json_template = {
  "UNCC": {
    "Total Publications": 11324,
    "Colleges": [
      {
        "College Name": "Belk College of Business",
        "Faculty": 163,
        "College Publications": 192,
        "Department": [
          {
            "Name": "Accounting",
            "Department Publications": 58,
            "Faculty": [
              {
                "Name": "Bojan Cukic",
                "Link": "http://test.uncc.edu",
                "Publications": 29
              },
              {
                "Name": "Test Name",
                "Link": "http://test.uncc.edu",
                "Publications": 12
              }
            ],
            "Keywords": [
              {
                "Keyword": "Diversity",
                "Publications": 21
              },
              {
                "Keyword": "Test",
                "Publications": 21
              }
            ]
          }
        ]
      },
      {
        "Name": "College of Computing & Informatics",
        "Faculty": 163,
        "Total Publications": 192,
        "Department": [
          {
            "Name": "Business",
            "Keywords": [
              {
                "Keyword": "Test",
                "publications": 21
              },
              {
                "Keyword": "Test",
                "Publications": 21
              }
            ]
          }
        ]
      }
    ]
  }
}
def make_json(name, jsonData):
    json_object = json.dumps(jsonData, indent=4)
    with open('%s.json' % name, 'w') as outfile:
        outfile.write(json_object)


    
    



print(colleges_dict)
def read_file(filename):
    try:
        data = open(filename, 'r').read() 
        print('File read successfully')
        
        return data
    except Exception as e:
        print('Error reading file')
        print(e)
json_template = read_file('JSON_Template.json')
print(json_template)


# To retrieve the staff members's information from the website
def get_information(url):
    # making a request to the website
    response = requests.get(url)
    # saving the log file
    write_file('log/http_log.txt', response.text)
    soup = BeautifulSoup(response.text , 'lxml')
    department = soup.find('div', class_='connection-groups').text.strip()
    academic_interests = soup.find('div', class_='connection-links columns-2').text.strip()
    name = soup.find('div', class_='page-title').text.strip()

    link = url
    staff_member = {}
    staff_member['name'] = name
    staff_member['department'] = department
    print(department)
    staff_member['academic_interests'] = academic_interests
    
    
    return staff_member

def add_college_name(json_obj, college_name):
    # add college name to json object
    json_obj['College Name'] = college_name
    # add Faculty total  to json template
    json_obj['Faculty'] = 200
    # adding Public total to json template
    json_obj['College Publications'] = 200
    
    
    
def load_staff_info_output(json_file):
    
        
    json_new = json.load(json_file)
    
    name = json_obj
    print(name)
    college = json_new['UNCC']
    department = get_information('https://pages.uncc.edu/faculty/' + name.replace(' ', '-') )
    url = json_new['UNCC']['url']
    print(url)
    with open(json_file, 'w') as newOUTPUT:
        newOUTPUT(json.dumps('test.json', indent=4))
    
    

    # alling all departments to the colleges
    for college in json_obj[college_name]:
        json_obj[college_name][college]['Department'] = college 
    return json_obj

json_obj = read_file('all_staff.json')


print(json_obj)

colleges_dict = dict.fromkeys(colleges_dict)


# To retrieve the staff members's information from the website
def get_information(url):
    # making a request to the website
    response = requests.get(url)
    # saving the log file
    write_file('log/http_log.txt', response.text)
    soup = BeautifulSoup(response.text , 'lxml')
    department = soup.find('div', class_='connection-groups').text.strip()
    academic_interests = soup.find('div', class_='connection-links columns-2').text.strip()
    name = soup.find('div', class_='page-title').text.strip()

    link = url
    staff_member = {}
    staff_member['link'] = link
    staff_member['name'] = name
    staff_member['department'] = department
    staff_member['academic_interests'] = academic_interests
    
    
    return staff_member


# for college_abbr in json_obj['UNCC']:
#     if college_abbr['college_name'] not in college_abbr:
#        colleges_dict['College'] = college_abbr['college_name']
load_staff_info_output('all_staff.json')
#print(make_json('sample', colleges_dict ))
#print(colleges_dict)
