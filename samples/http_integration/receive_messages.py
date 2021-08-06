# importing the requests library
import requests
import json
import sys
import os
 
# check if user request help
if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(f"Usage HTTP API consumer: python receive_messages.py [queue_name]")
    sys.exit(0)
# connection settings
rabbitmq_hostname = os.getenv("RABBITMQ_HOSTNAME", "rabbitmq")
rabbitmq_http_port = int(os.getenv('RABBITMQ_HTTP_PORT', 15672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "gotoiot")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "gotoiot")
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")
print(f"Connecting to RabbitMQ: http://{rabbitmq_user}:{rabbitmq_user}@{rabbitmq_hostname}:{rabbitmq_http_port}")
# application settings
queue_name = sys.argv[1] if len(sys.argv) > 1 else "http.queue"
count = 10
requeue = True
encoding = "auto"
truncate = 50000
ackmode = "ack_requeue_false"
# execute request
headers = {'content-type': 'application/json'}
api_endpoint = f"http://{rabbitmq_hostname}:{rabbitmq_http_port}/api/queues/%2f/{queue_name}/get"
receive_settings = {"count": count, "requeue": requeue, "encoding": encoding, "truncate": truncate, "ackmode": ackmode}
response = requests.post(
    url=api_endpoint, 
    auth=(rabbitmq_user, rabbitmq_pass), 
    json=receive_settings, 
    headers=headers
)
print(f"Sent request to '{api_endpoint}' -> '{receive_settings}'")
print(f"The server code is '{response.status_code}' and content is '{response.text}'")
