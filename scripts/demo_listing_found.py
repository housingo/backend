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


# channel.queue_declare(queue="listings")

channel.basic_publish(
    exchange="",
    routing_key="listings",
    body=json.dumps(list),
)
# cleanup connection
connection.close()
