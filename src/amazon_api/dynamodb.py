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
    RecipeID = (
        int(
            dynamodb.scan(TableName=table_name, Limit=1)["Items"][0][
                "RecipeID"
            ]["N"]
        )
        + 1
    )
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
    if item:
        # updated_item = {
        #     k: v["S"]
        #     for k, v in item.items()
        #     if type(v) == dict and v.get("S") is not None
        # }
        updated_item = {k: v["S"] for k, v in item.items()}
        ai_recipe = AIRecipe.from_dict(updated_item)
        return ai_recipe
    else:
        return None
