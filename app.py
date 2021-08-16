
def _show_welcome_message():
    welcome_message = """\n\n
          /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
         /$$__  $$          | $$                   |_  $$_/     |__  $$__/
        | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
        | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
        | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
        | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
        |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
         \______/ \______/   \___/  \______/       |______/\______/|__/   

                            SERVICE AMQP SAMPLES
                            --------------------
    \n"""
    print(welcome_message)
    print(f"\n{'#' * 80}\n")
    help_message = """
    In this repo there are many samples to connect to RabbitMQ broker.
    Each sample includes help message invoking it with -h flag.

    Default exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/default_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/default_exchange/consumer.py

    Direct exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/direct_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/direct_exchange/consumer.py

    Fanout exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/fanout_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/fanout_exchange/consumer.py

    Topic exchange:
        Producer: 
            - docker-compose run amqp-samples python samples/topic_exchange/producer.py
        Consumer:
            - docker-compose run amqp-samples python samples/topic_exchange/consumer.py

    HTTP integration:
        Entities declaration: 
            - docker-compose run amqp-samples python samples/http_integration/create_exchange.py
            - docker-compose run amqp-samples python samples/http_integration/create_queue.py
            - docker-compose run amqp-samples python samples/http_integration/create_binding.py
        Producer: 
            - docker-compose run amqp-samples python samples/http_integration/send_message.py
        Consumer:
            - docker-compose run amqp-samples python samples/http_integration/receive_messages.py
    """
    print(help_message)
    print(f"\n{'#' * 80}\n\n")


def _init_application():
    print("Starting to run Service AMQP Samples")
    _show_welcome_message()


if __name__ == "__main__":
    _init_application()
