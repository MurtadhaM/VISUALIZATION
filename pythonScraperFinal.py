
import re
import requests
from bs4 import BeautifulSoup as bs

import csv

print("=================== Belk College of Business ===================")
URL = 'https://pages.charlotte.edu/connections/group/college-of-business/'

req = requests.get(URL)

soup  = bs(req.text, 'html.parser')
values = soup.find('input', attrs={'class', 'tags'})['value']

topics = re.findall('"name":"(.*?)",', values)
# print(names)

counts = re.findall('"count":(.*?),"', values)
# print(count)

urls = re.findall('"url":"(.*?)"}', values)
# print(url)

# print(len(topics))

# print(len(counts))

# print(len(urls))

totalRowCount = 0

header = ['College', 'Topic', 'Count', 'URL']

with open('data.csv', 'w', encoding='UTF8', newline = '') as f:

    writer = csv.writer(f)

    writer.writerow(header)

    for i in range(len(topics)):

        infoForRows = []

        infoForRows.append('Belk College of Business')
        infoForRows.append(topics[i])
        infoForRows.append(counts[i])
        infoForRows.append(urls[i])

        writer.writerow(infoForRows)
        totalRowCount += 1
