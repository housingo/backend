import string
import pymongo
import os

client = pymongo.MongoClient(os.environ.get("DB_STRING"))
db = client["housingo"]
accounts = db["accounts"]
mails = db["mails"]


def queryByUser(_user: string):
    return accounts.find_one({"username": _user}, {"_id": 0})


def queryByEmail(_email: string):
    return accounts.find_one({"email": _email}, {"_id": 0})


def queryByEmailOrUsername(_email: string, _username: string):
    return accounts.find_one(
        {"$or": [{"username": _username}, {"email": _email}]}, {"_id": 0}
    )


def updatePassword(_email: string, _passwordHash: string):
    acc = accounts.find_one({"email": _email})
    if acc is not None:
        accounts.update_one(
            {"_id": acc["_id"]}, {"$set": {"password": _passwordHash}}, upsert=False
        )

        return f"Updated {_email} account!"
    else:
        return f"Acount with email {_email} doesn't exist!"


def updateEmail(_email: string, _newEmail: string):
    acc = accounts.find_one({"email": _email})
    if acc is not None:
        accounts.update_one(
            {"_id": acc["_id"]}, {"$set": {"email": _newEmail}}, upsert=False
        )

        return f"Updated {_email} account!"
    else:
        return f"Acount with email {_email} doesn't exist!"


def updateSubscription(
    _email: string, _stripe_id: string, _phone: string, _tier: string
):
    acc = accounts.find_one({"email": _email})
    if acc is not None:
        accounts.update_one(
            {"_id": acc["id"]},
            {"$set": {"stripe_id": _stripe_id, "phone": _phone, "tier": _tier}},
            upsert=False,
        )
        mails.insert_one({"email": _email, "cities": ["eindhoven"]})
        return f"Updated subscription status for user {_email}!"
    else:
        return f"Account with email {_email} doesn't exist!"


def endSubscription(_email: string):
    acc = accounts.find_one({"email": _email})
    if acc is not None:
        print(acc)
        accounts.update_one(
            {"_id": acc["_id"]},
            {"$set": {"tier": "free"}},
            upsert=False,
        )
        return f"Updated subscription status for user {_email}!"
    else:
        return f"Account with email {_email} doesn't exist!"


def addAccount(_accountDict):
    accounts.insert_one(_accountDict)
