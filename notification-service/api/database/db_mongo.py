import pymongo
import os

client = pymongo.MongoClient(os.environ.get("DB_STRING"))
db = client["housingo"]
mails = db["mails"]


def get_emails(_city: str):
    emails = []
    for x in mails.find({}):
        if _city in x["cities"] or "all" in x["cities"]:
            emails.append(x["mail"])
    return emails


def insert_email(mail, cities):
    new_document = {"mail": mail, "cities": cities}
    mails.insert_one(new_document)
