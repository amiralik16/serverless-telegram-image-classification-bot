import logging
import azure.functions as func
import json
import os
import telegram
from telegram import Update
import requests

# Import helper script
from .predict import predict_image_from_url

try:
    token = os.getenv("BotToken")
    bot = telegram.Bot(token)
except Exception as e:
    logging.exception("An exception was thrown!")
    logging.info(f'ERROR: {e}')
finally:
    pass

def extract_photo(bot, update):
    file_id = update.message.photo[-1]
    newFile = bot.getFile(file_id)
    bot.sendMessage(chat_id=update.message.chat_id, text="Processing photo")
    return newFile

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info(f'Recieved json is: {req.get_json()}')
        update = Update.de_json(req.get_json(), bot)
        botFile = extract_photo(bot, update)
        results = predict_image_from_url(botFile._get_encoded_url())
        bot.sendMessage(chat_id=update.message.chat_id, text=f"It is a {results['predictedTagName']}")

        headers = {
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }

    except Exception as e:
        logging.exception("An exception was thrown!")
        logging.info(f'ERROR: {e}')
    
    finally:
        results = {"Result": "Fail"}
        headers = {}
    return func.HttpResponse(json.dumps(results), headers = headers)