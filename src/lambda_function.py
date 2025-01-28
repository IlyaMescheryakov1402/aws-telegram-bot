import json
import os

from dotenv import load_dotenv

from openai_api import openai_chat_completion, postproc_llm_answer
from telegram_api import send_reply

load_dotenv()
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_TOKEN = os.environ["OPENAI_API_KEY"]


def lambda_handler(event, context):
    body = json.loads(event["body"])

    print("*** Received event")

    chat_id = body["message"]["chat"]["id"]
    user_name = body["message"]["from"]["username"]
    message_text = body["message"]["text"]

    print(f"*** chat id: {chat_id}")
    print(f"*** user name: {user_name}")
    print(f"*** message text: {message_text}")
    print(json.dumps(body))

    reply_message = f"Reply to {message_text}"
    if message_text.startwith("!Cлышь"):
        reply_message = "За углом поссышь!"
    elif message_text.startwith("!Рецепт"):
        titles = ["Название", "Ингредиенты", "Метод приготовления"]
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = "Неверно указаны ингредиенты"
        else:
            ingredients = message_list[1]
            llm_answer = openai_chat_completion(
                openai_api_key=OPENAI_API_TOKEN,
                ingredient=ingredients,
                model="gpt-4o-mini",
                titles=titles,
            )
            title, all_ingredients, recipe = postproc_llm_answer(llm_answer)
            # TODO: Занести это в базу данных, выводить через команду поиск
            reply_message = f"{title}\n {all_ingredients}\n {recipe}"
    elif message_text.startwith("!Поиск"):
        message_list = message_text.split(maxsplit=1)
        if len(message_list) == 1:
            reply_message = "Неверно указаны ингредиенты"
        else:
            ingredients = message_list[1]
            # TODO: вывести из базы данных все рецепты,
            # которые содержат указанные ингредиенты
            reply_message = "Этот функционал пока не разработан!"
    else:
        reply_message = "Не знаю такой команды, попробуй еще!"

    send_reply(BOT_TOKEN, chat_id, reply_message)

    return {
        "statusCode": 200,
        "body": json.dumps("Message processed successfully"),
    }
