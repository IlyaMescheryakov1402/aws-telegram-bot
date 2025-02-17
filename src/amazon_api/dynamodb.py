import logging
from typing import Optional

import boto3

from logger_utils import base_config
from openai_api import AIRecipe

logger = logging.getLogger(__name__)
base_config()
logger.setLevel("INFO")


def add_recipe_to_db(recipe_dict: dict, table_name: str) -> None:
    dynamodb = boto3.client("dynamodb")
    items = dynamodb.scan(TableName=table_name, Limit=100).get("Items")
    RecipeID = max([int(item["RecipeID"]["N"]) for item in items]) + 1
    item_dict = {k: {"S": v} for k, v in recipe_dict.items()}
    item_dict.update({"RecipeID": {"N": str(RecipeID)}})
    dynamodb.put_item(TableName=table_name, Item=item_dict)
    logger.info(f"Recipe {item_dict['Title']['S']} was submitted successfully")
    return None


def get_recipe_by_id(recipe_id: str, table_name: str) -> Optional[AIRecipe]:
    dynamodb = boto3.client("dynamodb")
    item = dynamodb.get_item(
        TableName=table_name, Key={"RecipeID": {"N": recipe_id}}
    ).get("Item")
    logger.info(f"Get recipe {recipe_id}: {item}")
    if item:
        updated_item = {
            k: v["S"]
            for k, v in item.items()
            if type(v) == dict and v.get("S") is not None
        }
        # updated_item = {k: v["S"] for k, v in item.items()}
        ai_recipe = AIRecipe.from_dict(updated_item)
        return ai_recipe
    else:
        return None


def search_recipe(ingredient: str, table_name: str) -> Optional[str]:
    dynamodb = boto3.client("dynamodb")
    items = dynamodb.scan(
        TableName=table_name,
        FilterExpression="contains(Ingredients, :word)",
        ExpressionAttributeValues={":word": {"S": ingredient}},
    )["Items"]
    logger.info(f"Search items: {items}")
    reply_message = ""
    if items:
        for item in items:
            recipe_id = item["RecipeID"]["N"]
            recipe_title = item["Title"]["S"]
            reply_message += f"{recipe_id} - {recipe_title}\n"
        return reply_message
    else:
        return None
