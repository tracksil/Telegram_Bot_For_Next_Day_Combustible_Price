from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from bs4 import BeautifulSoup
import requests
from lxml import etree

updater = Updater("5685293170:AAG2X1YT--VgZVdojXPeU0R_6Ifys-_mRjQ",
                  use_context=True)

driver_path = "developer/chromedriver.exe"
URL = 'https://www.anre.md/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                  "103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,ro;q=0.7"
}


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Vrei să afli pretul combustibililor mâine?\n "
        "Ai găsit locul potrivit\n "
        "Pentru a vedea toate posibilitățile vă rog scriți /help")


def helps(update: Update, context: CallbackContext):
    update.message.reply_text("Comenzi disponibile:\n"
                              "/motorina - pentru a afla prețul motorinei mâine\n"
                              "/benzina -  pentru a afla prețul benzinei mâine")


def benzina(update: Update, context: CallbackContext):
    webpage = requests.get(URL, headers=headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    dom = etree.HTML(str(soup))
    price = dom.xpath('/html/body/section[2]/div/div/div[1]/table/tbody/tr[1]/td[2]')[0].text

    update.message.reply_text(f"Mâine prețul benzinei va fi de: {price} lei")


def motorina(update: Update, context: CallbackContext):
    webpage = requests.get(URL, headers=headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    dom = etree.HTML(str(soup))
    price = dom.xpath('/html/body/section[2]/div/div/div[1]/table/tbody/tr[2]/td[2]')[0].text

    update.message.reply_text(f"Mâine prețul motorinei va fi de: {price} lei")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helps))
updater.dispatcher.add_handler(CommandHandler('benzina', benzina))
updater.dispatcher.add_handler(CommandHandler('motorina', motorina))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
