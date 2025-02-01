import logging

import boto3

from logger_utils import base_config

logger = logging.getLogger(__name__)
base_config()


def add_recipe_to_db(title: str, ingredients: str, recipe: str) -> None:
    dynamodb = boto3.client("dynamodb")

    dynamodb.put_item(
        TableName="aws-telegram-bot",
        Item={
            "RecipeID": {"N": "0"},
            "Title": {"S": title},
            "Ingredients": {"S": ingredients},
            "Recipe": {"S": recipe},
        },
    )
    logger.info(f"Recipe {title} was submitted successfully")
    return None
