from fastapi import APIRouter
from ..utils.discord_webhooks import alert_customers
from ..utils.telegram import sendTelegramMsg
from ..utils.mailer import mail_listing
from ..database.db_mongo import get_emails
from ..utils import *
from pydantic import BaseModel

router = APIRouter()


class URL(BaseModel):
    housing_url: str


city_ids = {
    29: "eindhoven",
    24: "amsterdam",
    6090: "maastricht",
    545: "groeningen",
    25: "rotterdam",
    27: "utrecht",
    90: "hague",
    6093: "tilburg",
}


def get_city_from_url(url: str):
    return city_ids.get(int(url[url.find("city=") + 5 : len(url)]))


@router.post("/discord")
async def discord(body: URL):
    housing_url = body.housing_url
    return alert_customers(housing_url, get_city_from_url(housing_url))


@router.post("/telegram")
def telegram(body: URL):
    housing_url = body.housing_url
    return sendTelegramMsg(f"⚠⚠⚠ NEW APARTMENT FOUND ⚠⚠⚠ : {housing_url}")


@router.post("/mail")
def mail(body: URL):
    housing_url = body.housing_url
    found_city = get_city_from_url(housing_url)

    email_list = get_emails(found_city)
    return mail_listing(housing_url, email_list)
