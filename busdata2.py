from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time


client = KafkaClient(hosts="localhost:9092")

topic = client.topics['busdata_seoul']

# producer 생성
producer = topic.get_sync_producer()


# read Coordinates from geojason
input_file = open('./data/7611.json')
json_array = json.load(input_file) # json 형식의 데이터 로드

# 가져온 json format data에서 coordinates 부분만 뽑기
coordinates = json_array['features'][0]['geometry']['coordinates'] 

# generate uuid
def generate_uuid():
    return uuid.uuid4()

data = {}
data['busline'] = '00002'

#construct message and send it to kafka
def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.now())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('utf8'))
        i += 1
        time.sleep(1)



generate_checkpoint(coordinates)