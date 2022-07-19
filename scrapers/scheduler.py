import schedule, requests, time, json, pika, threading
from threading import Lock
from pprint import pprint
from h2s.scraper import scraper as scraper_h2s

messages = []
mutex = Lock()

# Push all new listings to the RabbitMQ queue
def populate_messaging_queue():

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # channel.queue_declare(queue="listings_test")
    channel.basic_publish(
        exchange="",
        routing_key="listings",
        body=json.dumps(messages),
    )
    messages.clear()

    connection.close()


# except Exception as e:
#     print("Error: " + str(e))
#     print("Could not connect to Rabbit MQ")


# Report downtime in uptime channel in Discord
def report_crash():
    requests.post(
        "https://discordapp.com/api/webhooks/997554015783100476/nltop35cmxVMDKKMtLC8kYz_AOKZdAa4VvGgQkM-Msjbm14X2DewK971BJF54y8arLZ6",
        data={"content": "Scrapers are down!"},
    )


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# Shared resource safe thread implementation
def job_h2s():
    print("I'm running on thread %s" % threading.current_thread())

    mutex.acquire()
    for item in scraper_h2s():
        messages.append(item)

    messages.append(
        {
            "url": "testing",
            "found_at": 100,
            "city": "test",
            "website": "test",
        }
    )
    pprint("Sending results to RabbitMQ Queue...")
    populate_messaging_queue()

    pprint("Done")
    mutex.release()


# Scheduler code
# def run_scrapers():
#     # run the h2s thread every 30s
#     schedule.every(30).seconds.do(run_threaded, job_h2s)
#     while True:
#         try:
#             schedule.run_pending()
#             time.sleep(1)
#         except Exception:
#             connection.close()
#             report_crash()
def run_scrapers():
    try:
        run_threaded(job_h2s)
    except Exception:
        report_crash()


if __name__ == "__main__":
    messages.append(
        {
            "url": "testing",
            "found_at": 100,
            "city": "test",
            "website": "test",
        }
    )
    populate_messaging_queue()
    # run_scrapers()
