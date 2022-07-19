import schedule, requests, time, json, pika, threading, datetime
from pprint import pprint

# messages = []
# mutex = Lock()

# Push all new listings to the RabbitMQ queue
def populate_messaging_queue(messages):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.exchange_declare(exchange="listings", exchange_type="fanout")
        channel.basic_publish(
            exchange="listings",
            routing_key="",
            body=json.dumps(messages),
        )
        messages.clear()
        connection.close()

    except Exception as e:
        print("Error: " + str(e))


# Report downtime in uptime channel in Discord
def report_crash():
    requests.post(
        "https://discordapp.com/api/webhooks/997554015783100476/nltop35cmxVMDKKMtLC8kYz_AOKZdAa4VvGgQkM-Msjbm14X2DewK971BJF54y8arLZ6",
        data={"content": "Scrapers are down!"},
    )


def run_threaded(job_func, *args):
    job_thread = threading.Thread(target=job_func, args=args)
    job_thread.start()


# Shared resource safe thread implementation
def job_h2s(city_id):
    print("I'm running on thread %s" % threading.current_thread())

    pprint("Sending results to RabbitMQ Queue...")
    populate_messaging_queue(
        [
            {
                "url": "https://holland2stay.com/residences/victoriapark-828.html"
                + str(threading.current_thread()),
                "found_at": time.time(),
                "city": "test",
                "website": "test",
            }
        ]
    )

    pprint("Done")


def run_scrapers():
    try:
        run_threaded(job_h2s, 12345)
        run_threaded(job_h2s, 12345)
        run_threaded(job_h2s, 12345)
        run_threaded(job_h2s, 12345)
        run_threaded(job_h2s, 12345)
    except Exception as e:
        print("Error:" + str(e))
        report_crash()


if __name__ == "__main__":
    run_scrapers()
