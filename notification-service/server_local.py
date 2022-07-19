import pika, json, pprint
from utils.discord_webhooks import alert_customers
from utils.db_mongo import insert_listing_archive, check_in_archive
from datetime import datetime


def notify(listing_url: str, city: str):
    alert_customers(listing_url, "test")


def on_request(ch, method, props, body):
    listing_dict_list = json.loads(body)
    pprint.pprint(listing_dict_list)
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

    ch.basic_publish(
        exchange="",
        routing_key=str(props.reply_to),
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str("success"),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    try:
        print("Connecting to RabbitMQ")
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.exchange_declare(exchange="listings", exchange_type="fanout")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange="listings", queue=queue_name)
        print("Notification Service Status: started")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_request)

        channel.start_consuming()
    except Exception as e:
        print(e)
