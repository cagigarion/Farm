import pika


def public_message(queue_name: str, message: str):
    public_message('', queue_name, message)

def public_message(exchange_name: str,queue_name: str, message: str):    
    connection_parameters = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=message)

    connection.close()