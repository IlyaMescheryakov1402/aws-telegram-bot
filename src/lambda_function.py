import json
import logging
import os

from dotenv import load_dotenv

from amazon_api import add_recipe_to_db
from logger_utils import base_config
from openai_api import openai_chat_completion, postproc_llm_answer
from reply_phrases import ReplyPhrases
from telegram_api import send_reply

logger = logging.getLogger(__name__)
base_config()
logger.setLevel("INFO")

load_dotenv()
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_TOKEN = os.environ["OPENAI_API_KEY"]


def lambda_handler(event, context):
    body = json.loads(event["body"])

    logger.info("*** Received event")

    chat_id = body["message"]["chat"]["id"]
    user_name = body["message"]["from"]["username"]
    message_text = body["message"]["text"]

    logger.info(f"*** chat id: {chat_id}")
    logger.info(f"*** user name: {user_name}")
    logger.info(f"*** message text: {message_text}")
    # logger.info(json.dumps(body))

    if message_text.startswith("Ping"):
        reply_message = ReplyPhrases.ping_pong
    elif message_text.startswith("Recipe"):
        titles = ["Название", "Ингредиенты", "Метод приготовления"]
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = ReplyPhrases.wrong_ingredients
        else:
            ingredients = message_list[1]
            llm_answer = openai_chat_completion(
                openai_api_key=OPENAI_API_TOKEN,
                ingredient=ingredients,
                model="gpt-4o-mini",
                titles=titles,
            )
            full_recipe = postproc_llm_answer(llm_answer, titles)
            if full_recipe:
                add_recipe_to_db(
                    title=full_recipe.title,
                    ingredients=full_recipe.ingredients,
                    recipe=full_recipe.recipe,
                )
                reply_message = f"{full_recipe.title}\n \
                    {full_recipe.ingredients}\n {full_recipe.recipe}"
            else:
                reply_message = ReplyPhrases.wrong_postprocessing
    elif message_text.startswith("Search"):
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = ReplyPhrases.wrong_ingredients
        else:
            ingredients = message_list[1]
            # TODO: вывести из базы данных все рецепты,
            # которые содержат указанные ингредиенты
            reply_message = ReplyPhrases.future_feature
    else:
        reply_message = ReplyPhrases.wrong_command

    send_reply(BOT_TOKEN, chat_id, reply_message)

    return {
        "statusCode": 200,
        "body": json.dumps("Message processed successfully"),
    }
