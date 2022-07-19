import pika, json, pprint
from utils.discord_webhooks import alert_customers
from utils.db_mongo import insert_listing_archive, check_in_archive
from datetime import datetime


def notify(listing_url: str, city: str):
    alert_customers(listing_url, city)


def on_request(ch, method, props, body):
    listing_dict_list = json.loads(body)
    for item in listing_dict_list:
        if not check_in_archive(item):
            insert_listing_archive(item)

            now = datetime.timestamp(datetime.now())
            listing_found_at = item["found_at"]
            listing_url = item["url"]
            listing_city = item["city"]

            print(
                "Found apartment at: " + str(listing_found_at) + " now: " + str(now),
                listing_city,
                listing_url,
            )

            if int(now) - int(listing_found_at) < 300:
                notify(listing_url, listing_city)

    ch.basic_publish(
        exchange="",
        routing_key=str(props.reply_to),
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str("success"),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    print("Connecting to RabbitMQ")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="listings", exchange_type="fanout")
    channel.queue_declare(queue="listings")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="listings", on_message_callback=on_request)

    print("Notification Service Status: started")
    channel.start_consuming()
except Exception as e:
    print(e)
