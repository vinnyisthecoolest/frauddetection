import csv
import json
from kafka import KafkaProducer
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

topic = 'fraud-topic'

labels = 'step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,' \
    'nameDest,oldbalanceDest,newbalanceDest,isFraud,isFlaggedFraud' \
    .split(',')

# Simulate Stream
# return streamData
# stream = simulate.getStream()

def emitter():
    print('Emitting...')

    # producer.send(stream)

    with open('../data/data.csv') as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            producer.send(topic, dict(zip(labels, row)))
            print(dict(zip(labels, row)))
            sleep(1)

    print('Done emitting!')

if __name__ == '__main__':
    emitter()
