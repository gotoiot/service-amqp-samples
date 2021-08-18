import os
import sys
import json
import argparse

import pika


DEFAULT_RABBITMQ_HOSTNAME = os.getenv("RABBITMQ_HOSTNAME", "localhost")
DEFAULT_RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
DEFAULT_RABBITMQ_USER = os.getenv("RABBITMQ_USER", "gotoiot")
DEFAULT_RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "gotoiot")
DEFAULT_RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
DEFAULT_EXCHANGE = os.getenv("EXCHANGE", "")
DEFAULT_EXCHANGE_TYPE = os.getenv("EXCHANGE_TYPE", "")
DEFAULT_DURABLE = os.getenv("DURABLE", True)
DEFAULT_ROUTING_KEY = os.getenv("ROUTING_KEY", "")
DEFAULT_QUEUE = os.getenv("QUEUE", "")
DEFAULT_EXCLUSIVE = os.getenv("EXCLUSIVE", False)
DEFAULT_AUTO_ACK = os.getenv("AUTO_ACK", True)
DEFAULT_SIMPLE_DECLARATION = os.getenv("SIMPLE_DECLARATION", False)
# objects to establish connection to broker
connection = None
channel = None


def parse_cli_args():
    def _boolean_string(s):
        if s not in {'False', 'True'}:
            raise ValueError('Not a valid boolean string')
        return s == 'True'
    # Create the parset object
    parser = argparse.ArgumentParser(
        description='Help of usage for Goto IoT AMQP consumer client'
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
        type=_boolean_string,
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
        "-q", "--queue",
        dest='queue',
        type=str,
        help='The queue name to consume from',
        default=DEFAULT_QUEUE
        )
    parser.add_argument(
        "-x", "--exclusive",
        dest='exclusive',
        type=_boolean_string,
        help='The queue exclusive declaration flag',
        default=DEFAULT_EXCLUSIVE
        )
    parser.add_argument(
        "-a", "--auto_ack",
        dest='auto_ack',
        type=_boolean_string,
        help='The queue auto ACK enable flag config',
        default=DEFAULT_AUTO_ACK
        )
    parser.add_argument(
        "-s", "--simple_declaration",
        dest='simple_declaration',
        type=_boolean_string,
        help='Flag to declare simple exchange entities',
        default=DEFAULT_SIMPLE_DECLARATION
        )
    # Parse arguments and return them as dict
    args = parser.parse_args()
    return vars(args)


def connect_to_broker(**kwargs):
    global connection
    global channel
    credentials = pika.PlainCredentials(kwargs['rabbitmq_user'], kwargs['rabbitmq_pass'])
    parameters = pika.ConnectionParameters(
        kwargs['rabbitmq_hostname'], 
        kwargs['rabbitmq_port'], 
        kwargs['rabbitmq_vhost'], 
        credentials
        )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print(f"[INFO] Connected to broker: "
    f"host={kwargs['rabbitmq_hostname']}, "
    f"port={kwargs['rabbitmq_port']}, "
    f"user={kwargs['rabbitmq_user']}, "
    f"pass={kwargs['rabbitmq_pass']}, "
    f"vhost={kwargs['rabbitmq_vhost']}")


def _on_message_callback(ch, method, properties, body):
    print(f"[INFO] Received message: {body}")


def declare_broker_entities(**kwargs):
    if kwargs['simple_declaration']:
        channel.basic_consume(
            queue=kwargs['queue'], 
            on_message_callback=_on_message_callback, 
            auto_ack=kwargs['auto_ack']
        )
        print(f"[INFO] Done simple exchange declarations because already declared")
        return
    channel.exchange_declare(
        exchange=kwargs['exchange'], 
        exchange_type=kwargs['exchange_type'], 
        durable=kwargs['durable']
        )
    print(f"[INFO] Declared exchange: exchange='{kwargs['exchange']}', exchange_type='{kwargs['exchange_type']}', durable='{kwargs['durable']}'")
    queue = channel.queue_declare(
        queue=kwargs['queue'], 
        exclusive=kwargs['exclusive'],
        durable=kwargs['durable']
        )
    queue_name = queue.method.queue
    channel.queue_bind(
        exchange=kwargs['exchange'], 
        queue=queue_name, 
        routing_key=kwargs['routing_key']
        )
    print(f"[INFO] Binded exchange '{kwargs['exchange']}' to queue '{queue_name}' with routing key '{kwargs['routing_key']}'")
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=_on_message_callback, 
        auto_ack=kwargs['auto_ack']
        )


def disconnect_from_broker():
    connection.close()
    print(f"[INFO] Closed connection to broker")


def consume_queue(**kwargs):
    print(f"[INFO] Starting to consume from queue in blocking mode...To exit press CTRL+C")
    channel.start_consuming()


def main():
    cli_args = parse_cli_args()
    print(f"[DEBUG] CLI args: {cli_args}")
    connect_to_broker(**cli_args)
    declare_broker_entities(**cli_args)
    consume_queue(**cli_args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        disconnect_from_broker()
        print('[INFO] Exiting consumer by keyboard interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

