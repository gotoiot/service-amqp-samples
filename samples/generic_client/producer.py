import os
import pika
import sys
import json
import argparse


DEFAULT_RABBITMQ_HOSTNAME = os.getenv("RABBITMQ_HOSTNAME", "localhost")
DEFAULT_RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
DEFAULT_RABBITMQ_USER = os.getenv("RABBITMQ_USER", "gotoiot")
DEFAULT_RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "gotoiot")
DEFAULT_RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
DEFAULT_EXCHANGE = os.getenv("EXCHANGE", "")
DEFAULT_EXCHANGE_TYPE = os.getenv("EXCHANGE_TYPE", "")
DEFAULT_DURABLE = os.getenv("DURABLE", True)
DEFAULT_ROUTING_KEY = os.getenv("ROUTING_KEY", "")
DEFAULT_BODY = os.getenv("BODY", "")


def parse_cli_args():
        # Create the parset object
        parser = argparse.ArgumentParser(
            description='Help of usage for Goto IoT AMQP producer client'
            )
        # Add the cli arguments supported
        parser.add_argument(
            "-H", "--hostname",
            dest='rabbitmq_hostname',
            type=str,
            help='The RabbitMQ hostname',
            default=DEFAULT_RABBITMQ_HOSTNAME
            )
        parser.add_argument(
            "-p", "--port",
            dest='rabbitmq_port',
            type=int,
            help='The RabbitMQ port',
            default=DEFAULT_RABBITMQ_PORT
            )
        parser.add_argument(
            "-u", "--user",
            dest='rabbitmq_user',
            type=str,
            help='The RabbitMQ user',
            default=DEFAULT_RABBITMQ_USER
            )
        parser.add_argument(
            "-P", "--pass",
            dest='rabbitmq_pass',
            type=str,
            help='The RabbitMQ pass',
            default=DEFAULT_RABBITMQ_PASS
            )
        parser.add_argument(
            "-v", "--vhost",
            dest='rabbitmq_vhost',
            type=str,
            help='The RabbitMQ virtual host',
            default=DEFAULT_RABBITMQ_VHOST
            )
        parser.add_argument(
            "-e", "--exchange",
            dest='exchange',
            type=str,
            help='The exchange name to publish',
            default=DEFAULT_EXCHANGE
            )
        parser.add_argument(
            "-t", "--type",
            dest='exchange_type',
            type=str,
            help='The exchange type to declare',
            default=DEFAULT_EXCHANGE_TYPE
            )
        parser.add_argument(
            "-d", "--durable",
            dest='durable',
            type=bool,
            help='The exchange durable config',
            default=DEFAULT_DURABLE
            )
        parser.add_argument(
            "-r", "--routing_key",
            dest='routing_key',
            type=str,
            help='The routing key to publish message',
            default=DEFAULT_ROUTING_KEY
            )
        parser.add_argument(
            "-m", "--message",
            dest='body',
            type=str,
            help='The message to send',
            default=DEFAULT_BODY
            )
        
        # Execute the parse_args() method
        args = parser.parse_args()
        # return the arguments obtained as dict
        return vars(args)

def connect_to_broker(**kwargs):
    credentials = pika.PlainCredentials(kwargs['rabbitmq_user'], kwargs['rabbitmq_pass'])
    parameters = pika.ConnectionParameters(kwargs['rabbitmq_hostname'], kwargs['rabbitmq_port'], kwargs['rabbitmq_vhost'], credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print(f"[INFO] Connected to broker: "
    f"host={kwargs['rabbitmq_hostname']}, "
    f"port={kwargs['rabbitmq_port']}, "
    f"user={kwargs['rabbitmq_user']}, "
    f"pass={kwargs['rabbitmq_pass']}, "
    f"vhost={kwargs['rabbitmq_vhost']}")
    return connection, channel


cli_args = parse_cli_args()
connection, channel = connect_to_broker(**cli_args)
channel.exchange_declare(exchange=cli_args['exchange'], exchange_type=cli_args['exchange_type'], durable=cli_args['durable'])
print(f"[INFO] Declared exchange: exchange='{cli_args['exchange']}', exchange_type='{cli_args['exchange_type']}', durable='{cli_args['durable']}'")
channel.basic_publish(exchange=cli_args['exchange'], routing_key=cli_args['routing_key'], body=cli_args['body'])
print(f"[INFO] Sent message: exchange='{cli_args['exchange']}', routing_key='{cli_args['routing_key']}', body='{cli_args['body']}'")
connection.close()
