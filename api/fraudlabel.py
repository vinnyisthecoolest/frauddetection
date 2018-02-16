from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import requests

client = MongoClient('localhost', 27017)
# client.drop_database('test_database')

db = client.test_database
tests = db.tests

topic = 'fraud-topic'
url='http://vps152755.vps.ovh.ca:5000/predict'

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['0.0.0.0:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def main():
    for msg in consumer:
        prob = requests.post(url, json=msg.value)
        tests.insert_one({**msg.value, 'prob': float(prob.text)})
        print(prob.text)

if __name__ == "__main__":
    main()
