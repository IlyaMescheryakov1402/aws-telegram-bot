import json
import os
from telegram_api import send_reply
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

def lambda_handler(event, context):
    body = json.loads(event['body'])

    print("*** Received event")

    chat_id = body['message']['chat']['id']
    user_name = body['message']['from']['username']
    message_text = body['message']['text']

    print(f"*** chat id: {chat_id}")
    print(f"*** user name: {user_name}")
    print(f"*** message text: {message_text}")
    print(json.dumps(body))

    reply_message = f"Reply to {message_text}"

    send_reply(BOT_TOKEN, chat_id, reply_message)

    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }
