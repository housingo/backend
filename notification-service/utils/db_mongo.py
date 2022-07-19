import string
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.environ.get("DB_STRING"))
db = client["archive"]

city_ids = {
    29: "eindhoven",
    24: "amsterdam",
    6090: "maastricht",
    545: "groeningen",
    25: "rotterdam",
    27: "utrecht",
    90: "hague",
    6093: "tilburg",
    0: "testing",
}


def get_city_from_url(url: str):
    return city_ids.get(int(url[url.find("city=") + 5 : len(url)]))


def insert_listing_archive(listing: dict):
    collection_selected = db["listings_" + listing["website"]]
    collection_selected.insert_one(listing)


def check_in_archive(listing: dict):
    collection_selected = db["listings_" + listing["website"]]
    if collection_selected.find_one(listing) is None:
        return False

    return True
