import json

import urllib3


def send_reply(bot_token, chat_id, message):
    reply = {"chat_id": chat_id, "text": message}
    encoded_data = json.dumps(reply).encode("utf-8")
    urllib3.PoolManager().request(
        "POST",
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        body=encoded_data,
        headers={"Content-Type": "application/json"},
    )
    print(f"*** Reply : {encoded_data}")
