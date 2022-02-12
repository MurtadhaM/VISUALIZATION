#!/usr/bin/env python3.10 


import pandas as pd
import json
import csv




file_data = pd.read_csv('log/topics.csv'  , encoding='utf-8'   )
d = pd.DataFrame(columns=['department', 'topic', 'count' , 'url'] ,   data=file_data.values.tolist() )
print(d.head() )


topics = {
    
}



for row in d.to_dict('records'):
    if row['department'] not in topics.keys():
        topics[row['department']] = {
            
            "topic": []
        }
    else:    
        topics[row['department']]["topic"].append([row['topic'], row['count']])
    
        


print(json.dumps(topics))
json.dump((topics), open('log/topics.json', 'w'))