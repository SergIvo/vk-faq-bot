# VKontakte FAQ bot 

## About

This is a demo version of a bot for VKontakte community. Bot reads FAQ from .xlsx file, and compares questions from FAQ with questions send in community chat by other users. If something similar to user's question does exist in FAQ, bot how it to user with the answers.

## Preparing project to run

1. Download files from GitHub with `git clone` command:
```
git clone https://github.com/SergIvo/vk-faq-bot
```
2. Create virtual environment using python [venv](https://docs.python.org/3/library/venv.html) to avoid conflicts with different versions of the same packages:
```
python -m venv venv
```
3. Then install dependencies from "requirements.txt" in created virtual environment using `pip` package manager:
```
pip install -r requirements.txt
```
4. To run the project scripts, you should first set some environment variables. To make environment variable management easier, you can create [.env](https://pypi.org/project/python-dotenv/#getting-started) file and store all variables in it. 
```
export VK_GROUP_TOKEN="API key of VKontakte group in which bot supposed to respond in the group chat"
export TG_API_KEY="your Telegram API key, needed by logger"
export TG_LOG_CHAT_ID="ID of the chat to there bot will log service information (warnings, error messages, etc.)"
```

## Running scripts

### VKontakte bot
Note that you should replace file `faq.xlsx` with .xlsx file with your own FAQ. File FAQ must contain two columns on the first worksheet, where first column must contain questions and second column must contain  answers.

When you have your FAQ entitled as `faq.xlsx` in the project's main directory, run bot with the following command:
```
python vk_bot.py
```

To run project in Docker, create image with command:
```
docker build -t faq_bot .
```
Then you can run bot in container:
```
docker run --name faq_bot --env-file ./.env -d faq_bot:latest
```
