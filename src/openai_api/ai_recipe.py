from typing import List


class AIRecipe:
    prompt_articles: List = ["Название", "Ингредиенты", "Метод приготовления"]

    def __init__(self, title: str, ingredients: str, recipe: str):
        self.title = title
        self.ingredients = ingredients
        self.recipe = recipe
        self.DB_dict = {
            "Title": self.title,
            "Ingredients": self.ingredients,
            "Recipe": self.recipe,
        }
        self.reply = (self.title, self.ingredients, self.recipe)
        self.check_attributes()

    @classmethod
    def from_dict(cls, input_d: dict):
        return cls(input_d["Title"], input_d["Ingredients"], input_d["Recipe"])

    def check_attributes(self):
        assert len(self.DB_dict) == len(self.prompt_articles), "Check articles"
        assert len(self.reply) == len(self.prompt_articles), "Check articles"

    def to_dict(self):
        return self.DB_dict

    def to_tuple(self):
        return self.reply
