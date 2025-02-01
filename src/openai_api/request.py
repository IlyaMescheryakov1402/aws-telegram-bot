import logging
from typing import List

from openai import OpenAI

from logger_utils import base_config

logger = logging.getLogger(__name__)
base_config()


def openai_chat_completion(
    openai_api_key: str, ingredient: str, model: str, titles: List
) -> str:
    # ingredient = "лосось,сливки"
    prompt = f"Найди пожалуйста рецепт который содержит следующие \
        ингредиенты: {ingredient}. Выведи ответ в виде \
        {' - '.join(titles)}. \
        Не выводи символы * и #"
    client = OpenAI(api_key=openai_api_key)
    r0 = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    # logger.info(f"ChatCompletion: {r0.choices[0].message.content}")
    return r0.choices[0].message.content
