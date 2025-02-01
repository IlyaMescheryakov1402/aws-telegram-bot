import logging
import re
from typing import Optional

from logger_utils import base_config
from openai_api import AIRecipe

logger = logging.getLogger(__name__)
base_config()
logger.setLevel("INFO")


def postproc_llm_answer(text: str) -> Optional[AIRecipe]:
    # Ищем текст после ":" до пустой строки или конца текста
    pattern = r":(.*?)(?=\n\s*\n|$)"
    # Поиск совпадений
    # re.S позволяет учитывать переносы строк
    matches = re.findall(pattern, text, re.S)
    # Удаляем лишние пробелы и выводим результат
    results = [match.strip() for match in matches]
    if len(results) == len(AIRecipe.prompt_articles):
        title = results[0]
        logger.info(f"Title: {title}, preprocessing was done")
        return AIRecipe(*results)
    else:
        logger.info(f"Preprocessing failed: {results}")
        return None
