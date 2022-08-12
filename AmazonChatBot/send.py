import telebot
#import constants
from telebot import types
from amazon_affiliate_url import AmazonAffiliateUrl, Country


bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])



def start(message):
  sent = bot.send_message(message.chat.id, 'dammi ASIN (codice prodotto) ')
  bot.register_next_step_handler(sent, hello)


def hello(message):
  
  try:
	  ASIN = message.text
	  TAG =  '190e8f-21'

	  URL= AmazonAffiliateUrl.url_cls(asin_or_url=ASIN, affiliate_tag=TAG, country=Country.Italy)

	  modURL = URL[:-3]

	  bot.send_message(message.chat.id, modURL)
  except:
    bot.send_message(message.chat.id, "hai sbagliato a mandarmi qualcosa")
  	  

bot.polling() 
