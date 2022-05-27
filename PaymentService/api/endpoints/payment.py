from fastapi import APIRouter, Request
import stripe

from ..database.db_mongo import updateSubscription, endSubscription
from ..resources.mailer import mail_welcome

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):

    tier = {"1599": "basic", "2099": "premium"}
    info = await request.json()
    if info["type"] == "invoice.paid":
        try:
            customer_id = info["data"]["object"]["customer"]
            customer_object = stripe.Customer.retrieve(customer_id)

            customer_email = customer_object["email"]
            customer_phone = customer_object["phone"]
            amount_due = info["data"]["object"]["amount_due"]
            customer_tier = tier.get(amount_due.__str__())

            mail_welcome([customer_email])
            return updateSubscription(
                customer_email, customer_id, customer_phone, customer_tier
            )

        except Exception as e:
            print(e)
            pass

    if info["type"] == "customer.subscription.ends":
        try:
            customer_id = info["data"]["object"]["customer"]
            customer_object = stripe.Customer.retrieve(customer_id)

            customer_email = customer_object["email"]

            return endSubscription(customer_email)
        except Exception as e:
            print(e)
            pass

    return "Success!"
