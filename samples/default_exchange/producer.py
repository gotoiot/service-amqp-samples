import os
import pika
import sys

# check if user request help
if len(sys.argv) > 0 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(f"Usage default exchange producer: python producer.py [routing_key] [message]")
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
routing_key = sys.argv[1] if len(sys.argv) > 1 else "gotoiot.default"
message = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Hello Goto IoT!"
# send message to queue
channel.basic_publish(exchange='', routing_key=routing_key, body=message)
print(f"Sent to default exchange routing_key='{routing_key}', message='{message}'")
connection.close()
