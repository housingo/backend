import requests, time, json, pika, re
from bs4 import BeautifulSoup

BASE_URL = 'https://holland2stay.com/residences/'


def findBookDirectly(soup, list):
    element = soup.find_all('span', text=re.compile(".*BOOK DIRECTLY.*"))
    for item in element:
        address = item.parent.text.lower() \
            .replace('book directly', '') \
            .replace('parking included', '') \
            .replace('unfurnished', '') \
            .replace('semi-furnished', '') \
            .replace("premium inventory", "") \
            .replace("student only", "") \
            .strip().replace(' ', '-')
        list.append(BASE_URL + address + '.html')


city_ids = {
    29: "eindhoven",
    24: "amsterdam",
    6090: "maastricht",
    545: "groeningen",
    25: "rotterdam",
    27: "utrecht",
    90: "hague",
    6093: "tilburg",
    12345: "testing"
}

scraper_city_id = 29
search_url = "https://holland2stay.com/residences.html?available_to_book=179&city=" + str(scraper_city_id)
list = []


def scraper():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue="listings")

    except Exception:
        print("Could not connect to Rabbit MQ")

    for i in range(1, 3):

        html_content = ""

        print("Fetching urls from page: " + i.__str__())
        print(search_url)
        if i == 1:
            html_content = requests.get(search_url)

        if i > 1:
            html_content = requests.get(search_url + "?p=" + i.__str__())

        property_list = BeautifulSoup(html_content.content, "html.parser")
        findBookDirectly(property_list, list)

        for item in list:
            listing = {
                "url": item,
                "found_at": time.time(),
                "city": city_ids.get(scraper_city_id)
            }
            channel.basic_publish(
                exchange="",
                routing_key="listings",
                body=json.dumps(listing)
            )

        list.clear()

    connection.close()
