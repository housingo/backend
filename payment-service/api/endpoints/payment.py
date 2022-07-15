from fastapi import APIRouter, Request
import stripe, os, pprint

from ..database.db_mongo import updateSubscription, endSubscription
from ..resources.mailer import mail_welcome

router = APIRouter()
stripe.api_key = os.environ.get("STRIPE_KEY_TEST")
# stripe.api_key = os.environ.get("STRIPE_KEY_LIVE")
@router.post("/webhook")
async def webhook(request: Request):

    tier = {"1599": "basic", "2099": "premium", "3000": "testing"}
    info = await request.json()

    print(info["type"])

    if info["type"] == "checkout.session.completed":
            try:
                customer_id = info["data"]["object"]["customer"]

                customer_email = info["data"]["object"]["customer_details"]["email"]
                customer_phone = info["data"]["object"]["customer_details"]["phone"]
                amount_due = info["data"]["object"]["amount_total"]
                customer_tier = tier.get(amount_due.__str__())

                mail_welcome([customer_email])
                updateSubscription(customer_email, customer_id, customer_phone, customer_tier)
                return ''
            except Exception as e:
                print(e)
                pass

    if info["type"] == "customer.subscription.deleted":
        try:
            customer_id = info["data"]["object"]["customer"]
            customer_object = stripe.Customer.retrieve(customer_id)

            pprint.pprint(customer_object)

            customer_email = customer_object["email"]

            return endSubscription(customer_email)
        except Exception as e:
            print(e)
            pass

    return "Success!"
