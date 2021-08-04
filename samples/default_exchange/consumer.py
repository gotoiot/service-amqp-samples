import os
import pika
import sys

# check if user request help
if len(sys.argv) > 0 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(f"Usage default exchange consumer: python consumer.py [routing_key]")
    sys.exit(0)


# connection settings
rabbitmq_hostname = os.getenv("RABBITMQ_HOSTNAME", "rabbitmq")
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "gotoiot")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "gotoiot")
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")


def callback(ch, method, properties, body):
    print(f"Received message: {body}")


def main():
    # establish connection to broker
    print(f"Connecting to RabbitMQ: amqp://{rabbitmq_user}:{rabbitmq_user}@{rabbitmq_hostname}:{rabbitmq_port}")
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    parameters = pika.ConnectionParameters(rabbitmq_hostname, rabbitmq_port, rabbitmq_vhost, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # application settings
    queue_name = sys.argv[1] if len(sys.argv) > 1 else "gotoiot.default"
    # starting to consume from queue
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Starting to consume from queue '{queue_name}'. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)