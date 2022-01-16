from kafka import KafkaConsumer
from hdfs import InsecureClient
import pandas as pd
import csv
import json
import os

from pandas.core.indexes.base import Index
my_consumer = KafkaConsumer(  
    'de-capstone3',  
    bootstrap_servers = ['ip : port'],  
    auto_offset_reset = 'earliest',  
    enable_auto_commit = True,   
    value_deserializer = lambda x : (x.decode('utf-8'))  
    )

data=[]

for i in my_consumer:   
    if i.value != 'some_message_bytes':
        data.append(json.loads(i.value))
    else:
        break

df = pd.DataFrame(data)
client_hdfs = InsecureClient('http://localhost:9870')

df['timestamp\n'].replace('\n','',regex=True , inplace=True)

with client_hdfs.write('/yoc_project/clickstream/clickstream.csv', encoding = 'utf-8') as writer:
    df.to_csv(writer,header=False,index=False)
