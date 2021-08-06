# importing the requests library
import requests
import json
import sys
import os
 
# check if user request help
if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(f"Usage HTTP API create binding: python create_binding.py [exchange_name] [queue_name] [routing_key]")
    sys.exit(0)
# connection settings
rabbitmq_hostname = os.getenv("RABBITMQ_HOSTNAME", "rabbitmq")
rabbitmq_http_port = int(os.getenv('RABBITMQ_HTTP_PORT', 15672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "gotoiot")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "gotoiot")
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")
print(f"Connecting to RabbitMQ: http://{rabbitmq_user}:{rabbitmq_user}@{rabbitmq_hostname}:{rabbitmq_http_port}")
# application settings
exchange_name = sys.argv[1] if len(sys.argv) > 1 else "gotoiot.http"
queue_name = sys.argv[2] if len(sys.argv) > 2 else "http.queue"
routing_key = sys.argv[3] if len(sys.argv) > 3 else "event"
arguments = {}
# execute request
headers = {'content-type': 'application/json'}
api_endpoint = f"http://{rabbitmq_hostname}:{rabbitmq_http_port}/api/bindings/%2f/e/{exchange_name}/q/{queue_name}"
binding_settings = {"routing_key": routing_key, "arguments": arguments}
response = requests.post(
    url=api_endpoint, 
    auth=(rabbitmq_user, rabbitmq_pass), 
    json=binding_settings, 
    headers=headers
)
print(f"Sent request to '{api_endpoint}' -> '{binding_settings}'")
print(f"The server code is '{response.status_code}' and content is '{response.text}'")

