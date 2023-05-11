import docker
import pika
import sys
import os
import logging
import json
import time
from config import *
import threading
from setup_coinfig import SetupConfig
import configparser
from report import report_check_worker

logging.getLogger("pika").propagate = False


def get_setup_configs_raw() -> list:
    path = get_path_config() + ".config"
    with open(path) as flog:
        return json.loads(flog.read())


def write_setup_configs(setup_configs: list[dict]) -> list:
    path = get_path_config() + ".config"
    if setup_configs is None:
        return
    with open(path, "w") as config_file:
        config_file.write(json.dumps(setup_configs))


def get_setup_configs() -> list[SetupConfig]:
    raw_data = get_setup_configs_raw()
    return SetupConfig.from_dict(raw_data)


class Threaded_worker(threading.Thread):
    def make_folder(self, path):
        exists_folder = os.path.exists(path)
        if not exists_folder:
            # Create a new directory because it does not exist
            os.makedirs(path)

    def callback_databiz(self, ch, method, properties, body):
        try:
            # send message to identify service
            # public_message("", queue_name=DATABIZ_QUEUE_IDENTIFY, message="Received Message")
            # need to receive authentication
            # save file to folder config

            client = docker.from_env()
            data_config = json.loads(body.decode())
            container_name_unique = data_config["name"] + \
                "_" + data_config["id"]
            try:
                container = client.containers.get(container_name_unique)
                if container != None:
                    if (data_config["is_enabled"] == False):
                        container.stop()
                        container.remove()
                        return
                    if (data_config["is_enabled"] == True):
                        return
            except Exception as ex:
                logging.error(f'No thing to do here {ex}')

            # print(type(data_config))

            # print(data_config)
            folder_name = data_config["name"] + "_" + data_config["id"]
            file_job_name = data_config["jobTaskId"]
            # path file json pipeline
            path = get_path_config()
            etl_mount_folder = get_path_config()
            # self.make_folder(path)
            pipeline_name_location = f'{path}{folder_name}'
            self.make_folder(pipeline_name_location)

            dic = {
                "type": "logfile",
                "name": "Logfile",
                "schema": {
                    "filename": f"{file_job_name}.log",
                    "logpath": f"{etl_mount_folder}/{folder_name}"
                }
            }

            data_config["destinations"].append(dic)

            # path file .config support read line log
            log_fname = f"{pipeline_name_location}/{file_job_name}.log"
            setup_configs = get_setup_configs_raw()
            setup_configs.append(SetupConfig(
                0, file_job_name, log_fname).__dict__)
            print("start container:")
            print(setup_configs)
            write_setup_configs(setup_configs)

            print("file meta save is",
                  f"{pipeline_name_location}/{file_job_name}.json")
            f = open(f"{pipeline_name_location}/{file_job_name}.json", "w")
            f.write(json.dumps(data_config, indent=4))
            f.close()

            '''
            config logs path file
            '''
            create_log_conf_file(
                f"{PATH_MAP}/{folder_name}/{file_job_name}.log", pipeline_name_location)

            # docker run --name etl-modules -v $(pwd)/dataconfig:/dataconfig etl-modules -c /dataconfig/pulsar_config_metadata.json
            # volumes = f"{path}:{etl_mount_folder}"
            volumes = f"{path}:{PATH_MAP}"
            # log_config = docker.types.LogConfig(
            #     type='fluentd'
            # )

            container = client.containers.run(image="etl-modules:latest",
                                              volumes=[volumes],
                                              name=container_name_unique,
                                              command=f"-c {PATH_MAP}/{folder_name}/{file_job_name}.json -l {PATH_MAP}/{folder_name}/etl_log.ini -i {PATH_MAP}/{folder_name}/interval.config",
                                              detach=True)

            # print(container.id, container.image, container.name, container.status)
            '''
            save log file 
            '''
            print("pass container")
            logging.basicConfig(
                filename=log_fname, format='%(asctime)s %(message)s', level=logging.INFO, force=True)
            logging.info(
                f"the container {container.short_id}  has been crated with module {container.image} and name is {container.name}")

        except Exception as ex:
            logging.error(ex)
            print(ex)

    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=get_databiz_queue())
        self.channel.basic_consume(
            queue=get_databiz_queue(), on_message_callback=self.callback_databiz, auto_ack=True)

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


def make_folder(path):
    exists_folder = os.path.exists(path)
    if not exists_folder:
        # Create a new directory because it does not exist
        os.makedirs(path)


def create_log_conf_file(log_file_name, log_config_path):
    # creating object of configparser
    config = configparser.ConfigParser()

    config.add_section("loggers")
    config.set("loggers", "keys", "root")

    config.add_section("handlers")
    config.set("handlers", "keys", "myhandler")

    config.add_section("formatters")
    config.set("formatters", "keys", "sampleFormatter")

    config.add_section("logger_root")
    config.set("logger_root", "level", "DEBUG")
    config.set("logger_root", "handlers", "myhandler")

    config.add_section("handler_myhandler")
    config.set("handler_myhandler", "class", "FileHandler")
    config.set("handler_myhandler", "level", "DEBUG")
    config.set("handler_myhandler", "formatter", "sampleFormatter")
    config.set("handler_myhandler", "args", f"('{log_file_name}', 'a')")

    config.add_section("formatter_sampleFormatter")
    config.set("formatter_sampleFormatter", "format",
               "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    with open(f"{log_config_path}/etl_log.ini", 'w') as example:
        config.write(example)


if __name__ == '__main__':
    # authentication

    '''
    we have a log filw with field "id"

    '''

    make_folder(get_path_config())
    write_setup_configs([])

    try:
        json_farm= get_farm_file_bytes()
        
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(
            exchange='farm.fanout', exchange_type='fanout')
        channel.queue_declare(queue='databiz-agent-check', durable=True)
        channel.basic_publish(exchange='farm.fanout',
                                routing_key='databiz-agent-check',
                                body=json_farm,
                                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        connection.close()

        td = Threaded_worker()
        td.start()

        farm_check = report_check_worker()
        farm_check.start()

        while (True):
            time.sleep(10)
            '''
            read log and send content to rabbitmq
            '''
            setup_configs = get_setup_configs()

            for setup_config in setup_configs:
                print("current_log_line ", setup_config.current_log_line)
                count_total_line = setup_config.current_log_line
                str_logs = []

                log_fname = setup_config.log_file_name
                print("setup_config.current_task", setup_config.current_task)
                if log_fname is not None and log_fname != "":
                    with open(log_fname) as f:
                        for _ in range(setup_config.current_log_line):
                            next(f)
                        for line in f:
                            count_total_line += 1
                            str_logs.append(line)
                    logs_message = "".join(str_logs)
                    time.sleep(5)

                    setup_config.current_log_line = count_total_line

                # '''

                # Agent sends logs data to rabbitmq through Exchange name 'logs.fanout' type 'fanout' and queue 'databiz-log'
                # '''
                # print("setup_config.current_task", setup_config.current_task)

                print("str_logs", str_logs)
                if (len(str_logs) > 0):
                    dis_message = {
                        "current_task": setup_config.current_task,
                        "message": logs_message
                    }
                    print(logs_message)
                    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=RABBITMQ_HOST))
                    channel = connection.channel()
                    channel.exchange_declare(
                        exchange='logs.fanout', exchange_type='fanout')
                    channel.queue_declare(queue='databiz-log', durable=True)
                    channel.basic_publish(exchange='logs.fanout',
                                          routing_key='databiz-log',
                                          body=json.dumps(dis_message),
                                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

                    connection.close()

                '''
                end send log
                '''

            setup_configs_raw = get_setup_configs_raw()
            setup_configs_updated = [
                setup_config.__dict__ for setup_config in setup_configs]
            len_setup_configs_raw = setup_configs_raw.__len__()
            if setup_configs_updated.__len__() < setup_configs_raw.__len__():
                i = setup_configs_updated.__len__()
                while (i < setup_configs_raw.__len__()):
                    setup_configs_updated.append(setup_configs_raw[i])
                    i = i+1
            print("sysnc log end process")
            print(setup_configs_updated)
            write_setup_configs(setup_configs_updated)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
