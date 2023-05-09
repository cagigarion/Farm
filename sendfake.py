import pika
import json
import logging
from config import *
# Create and configure logger
logging.basicConfig(format='%(asctime)s %(message)s',
                    filemode='w')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=DATABIZ_QUEUE)

dt_conf_file = 'conf/receive.json'
try:
    with open(dt_conf_file,"r") as conf_file:
        dt_config =json.load(conf_file)
        print(dt_config)
    
except:
    logging.error(f'Problem when handling the input file {dt_conf_file}')
    exit(0)


json_string = json.dumps(dt_config)

channel.basic_publish(exchange='', routing_key=DATABIZ_QUEUE, body=json_string)
print(" [x] Sent '" , json_string)
connection.close()