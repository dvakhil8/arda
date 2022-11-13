from time import sleep
from json import dumps,loads
from kafka import KafkaProducer
import pandas as pd
from common.config_support import ConfigSupport
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    stream=sys.stdout)

class EventProducer:
    def __int__(self):

        self.kafka_config = ConfigSupport().get_config('Kafka')
        self.producer = self.getEventProducer()
        # self.topic = self.kafka_config['topic']

    def readEvents(self, file_path):
        return pd.read_csv(file_path)

    def getTopicName(self, file_path):
        head, tail = os.path.split(file_path)
        return tail.replace('.csv', '')

    def getEventProducer(self):
        logging.info(self.kafka_config['bootstrap_servers'])
        return KafkaProducer(bootstrap_servers='127.0.0.1:9092', api_version=(0, 1, 0),
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    def publish(self):
        files = ['blocks.csv', 'transactions.csv']
        # files = ['transactions.csv']
        # files = ['blocks.csv']
        for file in files:
            topicName = self.getTopicName(file)
            eventsDf = self.readEvents(file)
            # print(eventsDf)
            events_list = loads(eventsDf.to_json(orient='records'))
            count=0
            try:
                for event in events_list:
                    try:
                        self.producer.send(topic=topicName, value=event)



                    except Exception as e:
                        logging.error(e)
                self.producer.flush()
            except Exception as e:
                logging.error(e)





if __name__ == "__main__":
    event = EventProducer()
    event.__int__()
    event.publish()
