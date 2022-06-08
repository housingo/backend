import pika
import json
from datetime import datetime

test_listing = {
    "listing_url": "https://holland2stay.com/residences.html?available_to_book=179,336&city=12345",
    "found_at": int(datetime.timestamp(datetime.now())),
}

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="listings")

channel.basic_publish(
    exchange="",
    routing_key="listings",
    body=json.dumps(test_listing),
)
# cleanup connection
connection.close()
