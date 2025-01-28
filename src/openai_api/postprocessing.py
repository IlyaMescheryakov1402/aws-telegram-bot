import re


def postproc_llm_answer(text: str):
    # Ищем текст после ":" до пустой строки или конца текста
    pattern = r":(.*?)(?=\n\s*\n|$)"
    # Поиск совпадений
    # re.S позволяет учитывать переносы строк
    matches = re.findall(pattern, text, re.S)
    # Удаляем лишние пробелы и выводим результат
    results = [match.strip() for match in matches]
    # print("Найденные тексты:")
    # for idx, result in enumerate(results):
    #     print(f"{titles[idx]} ------ {result}")
    return results
