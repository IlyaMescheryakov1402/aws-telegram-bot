import logging
import re
from typing import List, Optional

from logger_utils import base_config

logger = logging.getLogger(__name__)
base_config()


class AIRecipe:
    title: str
    ingredients: str
    recipe: str


def postproc_llm_answer(text: str, titles: List[str]) -> Optional[AIRecipe]:
    # Ищем текст после ":" до пустой строки или конца текста
    pattern = r":(.*?)(?=\n\s*\n|$)"
    # Поиск совпадений
    # re.S позволяет учитывать переносы строк
    matches = re.findall(pattern, text, re.S)
    # Удаляем лишние пробелы и выводим результат
    results = [match.strip() for match in matches]
    if len(results) == len(titles):
        title, ingredients, recipe = results
        logger.info(f"Title: {title}, preprocessing was done")
        return AIRecipe(title=title, ingredients=ingredients, recipe=recipe)
    else:
        logger.info(f"Preprocessing failed: {results}")
        return None
