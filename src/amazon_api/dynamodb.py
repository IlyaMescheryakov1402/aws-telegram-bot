import logging

import boto3

from logger_utils import base_config

logger = logging.getLogger(__name__)
base_config()


def add_recipe_to_db(recipe_dict: dict) -> None:
    dynamodb = boto3.client("dynamodb")
    RecipeID = (
        int(
            dynamodb.scan(TableName="aws-telegram-bot", Limit=1)["Items"][0][
                "RecipeID"
            ]["N"]
        )
        + 1
    )
    item_dict = {k: {"S": v} for k, v in recipe_dict.items()}
    item_dict.update({"RecipeID": {"N": str(RecipeID)}})
    dynamodb.put_item(TableName="aws-telegram-bot", Item=item_dict)
    logger.info(f"Recipe {item_dict['Title']['S']} was submitted successfully")
    return None
