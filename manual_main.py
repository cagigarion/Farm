import docker
import pika, sys, os, datetime
import logging
import json
import base64
from procedure import public_message
from config import *
import threading
logging.basicConfig(filename='newlog.log', format='%(asctime)s %(message)s',level=logging.INFO)


client = docker.from_env()
#docker run --name etl-modules -v $(pwd)/dataconfig:/dataconfig etl-modules -c /dataconfig/pulsar_config_metadata.json
volumes = "/home/conf:/dataconfig"
log_config = docker.types.LogConfig(
    type='fluentd'
)
container = client.containers.run(image="etl-modules:latest", 
                                volumes=[volumes],
                                log_config=log_config,
                                command=f"-c /dataconfig/test.json",
                                detach=True)

            
print(container)

