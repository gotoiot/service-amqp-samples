import os
import pika
import sys
import json

# check if user request help
if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(f"Usage topic exchange producer: python producer.py [exchange_name] [routing_key] [message]")
    sys.exit(0)
# connection settings
rabbitmq_hostname = os.getenv("RABBITMQ_HOSTNAME", "rabbitmq")
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "gotoiot")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "gotoiot")
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")
# establish connection to broker
print(f"Connecting to RabbitMQ: amqp://{rabbitmq_user}:{rabbitmq_user}@{rabbitmq_hostname}:{rabbitmq_port}")
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(rabbitmq_hostname, rabbitmq_port, rabbitmq_vhost, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# application settings
exchange_name = sys.argv[1] if len(sys.argv) > 1 else "gotoiot.topic"
routing_key = sys.argv[2] if len(sys.argv) > 2 else "event.status"
message = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else json.dumps({'type': 'REGISTRATION_DONE', 'user_id': 1})
durable_flag = True if exchange_name == "amq.topic" else False
# send message to queue
channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=durable_flag)
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
print(f"Sent to exchange='{exchange_name}', routing_key='{routing_key}', message='{message}'")
connection.close()
