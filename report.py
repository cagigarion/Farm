import os, threading, time, pika
from config import *

class report_check_worker(threading.Thread):
   
    def __init__(self):
        threading.Thread.__init__(self)
        
        queue_name = get_databiz_queue()
        self.agent_id = queue_name["databiz_".__len__():]  

    def run(self):
        while(True):
            connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.exchange_declare(exchange='farm.fanout', exchange_type='fanout')
            channel.queue_declare(queue='databiz-agent-check', durable=True)
            channel.basic_publish(exchange='farm.fanout',
                                    routing_key='databiz-agent-check',
                                    body=get_farm_file_bytes(),
                                    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

            connection.close()
            time.sleep(10)