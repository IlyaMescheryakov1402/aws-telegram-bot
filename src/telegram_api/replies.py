import json
import logging

import urllib3

from logger_utils import base_config

logger = logging.getLogger(__name__)
base_config()


def send_reply(bot_token, chat_id, message) -> None:
    reply = {"chat_id": chat_id, "text": message}
    encoded_data = json.dumps(reply).encode("utf-8")
    urllib3.PoolManager().request(
        "POST",
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        body=encoded_data,
        headers={"Content-Type": "application/json"},
    )
    logger.info(f"*** Reply : {encoded_data}")
    return None
