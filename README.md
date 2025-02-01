# AWS Telegram bot

Делаем полезного telegram бота с максимальным количеством AWS Free Tier сервисов

## Функционал

+ **PING** - проверка работоспособности сервиса

+ **RECIPE** - обращение к OpenAI модели для вывода нового рецепта (с занесением в базу данных) с указанным ингредиентом и метода приготовления

+ **SEARCH** - обращение к базе данных для вывода рецепта с указанным ингредиентом

+ **GET** - обращение к базе данных для вывода рецепта с определенным ID

## Кастомизация

Структуру выводимых рецептов (а также абзацы, заносимые в БД) можно изменять через файл [ai_recipe.py](src/openai_api/ai_recipe.py). При этом, если нужен другой язык вывода, не забудьте изменить промпт в файле [request.py](src/openai_api/ai_recipe.py)

## [AWS DynamoDB](https://aws.amazon.com/dynamodb/)

Была создана таблица в AWS DynamoDB c названием aws-telegram-bot, в качестве Partition key используем RecipeID (порядковый номер рецепта в базе). В качестве Table settings указываем Default settings.


## [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide)

### AWS CLI
https://docs.aws.amazon.com/cli/latest/reference/codepipeline/create-pipeline.html

### AWS Console
Создаем пайплайн через кнопку [Create pipeline](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipeline/new?region=us-east-1)

1. **Step 1** - *Choose creation option* - Выбираем Create pipeline from template

2. **Step 2** - *Choose template* - В Category выбираем Continuous Integration, в Template - CI Build Python

3. **Step 3** - *Choose source* - в Source provider выбираем Github (via Github App), в поле Connection выбираем Connect to Github. После этого появляется всплывающее окно, в котором нужно будет ввести (придумать - например aws-github-conn) имя будущего соединения с github и нажать на Connect to Github. Github будет спрашивать разрешение на интеграцию с AWS и репозитории, которые будут доступны в рамках этого connection. Соглашаемся и ждем закрытия окна (или сообщения об успешном коннекте). Возвращаемся в изначальное окно, в поле Connection выбираем только что созданный connection, в поле Repository name выбираем наш репозиторий, в поле default branch выбираем main. В поле Output artifact format выбираем CodePipeline default.

4. **Step 4** - *Configure template* - в поле CodePipelineName вводим имя (например DefaultPipeline), в CICodeBuildSpec - содержимое файла [codepipeline.yaml](aws_services/codepipeline.yaml)