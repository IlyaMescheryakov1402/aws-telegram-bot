import json
import logging
import os

from dotenv import load_dotenv

from amazon_api import add_recipe_to_db, get_recipe_by_id, search_recipe
from logger_utils import base_config
from openai_api import AIRecipe, openai_chat_completion, postproc_llm_answer
from reply_phrases import ReplyPhrases
from telegram_api import send_reply

logger = logging.getLogger(__name__)
base_config()
logger.setLevel("INFO")

load_dotenv()
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_TOKEN = os.environ["OPENAI_API_KEY"]
AWS_DYNAMODB_TABLE = os.environ["AWS_DYNAMODB_TABLE"]


def lambda_handler(event, context):
    body = json.loads(event["body"])

    logger.info("*** Received event")

    chat_id = body["message"]["chat"]["id"]
    user_name = body["message"]["from"]["username"]
    message_text = body["message"]["text"]

    logger.info(f"*** chat id: {chat_id}")
    logger.info(f"*** user name: {user_name}")
    logger.info(f"*** message text: {message_text}")

    if message_text.startswith("PING"):
        reply_message = ReplyPhrases.ping_pong
    elif message_text.startswith("RECIPE"):
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = ReplyPhrases.wrong_ingredients
        else:
            ingredients = message_list[1]
            llm_answer = openai_chat_completion(
                openai_api_key=OPENAI_API_TOKEN,
                ingredient=ingredients,
                model="gpt-4o-mini",
                titles=AIRecipe.prompt_articles,
            )
            full_recipe = postproc_llm_answer(llm_answer)
            if full_recipe:
                add_recipe_to_db(full_recipe.to_dict(), AWS_DYNAMODB_TABLE)
                reply_message = "\n\n".join(full_recipe.to_tuple())
            else:
                reply_message = ReplyPhrases.wrong_postprocessing
    elif message_text.startswith("SEARCH"):
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = ReplyPhrases.wrong_ingredients
        else:
            ingredient = message_list[1]
            reply = search_recipe(ingredient, AWS_DYNAMODB_TABLE)
            if reply:
                reply_message = reply
            else:
                reply_message = ReplyPhrases.empty_search
    elif message_text.startswith("GET"):
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = ReplyPhrases.wrong_id
        else:
            recipe_id = message_list[1]
            full_recipe = get_recipe_by_id(recipe_id, AWS_DYNAMODB_TABLE)
            if full_recipe:
                reply_message = "\n\n".join(full_recipe.to_tuple())
            else:
                reply_message = ReplyPhrases.wrong_id
    else:
        reply_message = ReplyPhrases.wrong_command

    send_reply(BOT_TOKEN, chat_id, reply_message)

    return {
        "statusCode": 200,
        "body": json.dumps("Message processed successfully"),
    }
