import pika, json
from utils.discord_webhooks import alert_customers
from utils.db_mongo import insert_listing_archive
from datetime import datetime


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="listings")


def notify(listing: str):
    alert_customers(listing, "test")


def on_request(ch, method, props, body):
    listing_dict = body

    now = datetime.timestamp(datetime.now())
    found_at = json.loads(listing_dict)["found_at"]
    print("Found apartment at: " + str(found_at) + " now: " + str(now))

    listing_url = json.loads(listing_dict)["listing_url"]
    insert_listing_archive(listing_url, int(found_at))

    if int(now) - int(found_at) < 100:
        notify(listing_url)

    ch.basic_publish(
        exchange="",
        routing_key=str(props.reply_to),
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str("success"),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="listings", on_message_callback=on_request)

print("Notification Service Status: started")
channel.start_consuming()
