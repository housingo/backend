import requests

token = "5129684742:AAH1HOBwCrjMZGg83r1HTr2Ag8CT7sIg0P4"
chat = "-699731868"


def sendTelegramMsg(msg):
    url = (
        "https://api.telegram.org/bot"
        + token
        + "/"
        + "sendMessage?chat_id="
        + chat
        + "&text="
        + msg
    )
    requests.get(url)
