import pika
import json
from datetime import datetime

list = []
test_listing = {
    "url": "https://holland2stay.com/residences/victoriapark-828.html",
    "found_at": int(datetime.timestamp(datetime.now())),
    "city": "test",
    "website": "test",
}

list.append(test_listing)
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

channel = connection.channel()


def populate_messaging_queue():

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="listings", exchange_type="fanout")
    channel.basic_publish(
        exchange="listings",
        routing_key="",
        body=json.dumps(list),
    )
    # messages.clear()

    connection.close()


# channel.queue_declare(queue="listings")
# channel.exchange_declare(exchange="listings", exchange_type="fanout")
# channel.basic_publish(
#     exchange="listings",
#     routing_key="",
#     body=json.dumps(list),
# )
if __name__ == "__main__":

    populate_messaging_queue()

# cleanup connection
# connection.close()
