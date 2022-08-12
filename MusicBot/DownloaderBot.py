import pytube
from youtubesearchpython import *
import requests
from telebot import TeleBot
from telebot import types
from os import listdir
from os.path import isfile, join


bot = TeleBot("5573307606:AAEmTPPiMY_bHjP7dOjIdk1YS8bFCTHM8gY")
titles = ""
search = ""
chat_id= ""
destination = "Z:/programminoSiro/python/eserciziPy/youtubeDownload/DownloadMusica"

@bot.message_handler(commands=['start'])

@bot.message_handler(commands=['donate'])

def donate(message):
	global chat_id
	chat_id = message.chat.id
	messaggio = "Forse hai cliccato per sbaglio il bottone per donare o forse no, io ti ringrazio comunque per star usando il mio bot!🙏🫂"
	try:
		keyboard = types.InlineKeyboardMarkup()
		button = types.InlineKeyboardButton("💸donare💸", url="https://paypal.me/graziemille2001?country.x=IT&locale.x=it_IT")
		keyboard.add(button)
		bot.send_message(chat_id, text = messaggio, reply_markup=keyboard)
	except:
		bot.send_message(chat_id, text = "in questo momento è impossibile donare ☹️ apprezzo comunque il gesto 🫂")

def start(message):
	global chat_id
	try:
		chat_id = message.chat.id
		sent = bot.send_message(message.chat.id, 'Benvenuto!! Digita il titolo della canzone che vuoi ascoltare')
		bot.register_next_step_handler(sent, gestione)
	except:
		bot.send_message(chat_id, text = "boh c' e stato un errore prova con una canzone piu bella")


def gestione(message):
	
		prefix = "youtube.com"
		global chat_id
		
		chat_id = message.chat.id
		nome_Canzone = message.text
		if prefix in nome_Canzone:
			dest = download(nome_Canzone)
			onlyfiles = [f for f in listdir(destination) if isfile(join(destination, f))]
			bot.send_audio(chat_id=chat_id, audio=open(dest + "/" + onlyfiles[0], 'rb'))
		else:	
			sent = bot.send_message(message.chat.id, 'Ho trovato queste canzoni, quale preferisci?')
			global titles
			titles = titoli(nome_Canzone)
			st = ""
			n = 0
			keyboard = types.InlineKeyboardMarkup()
			for t in titles:
				st = st + str(n) + ": " + t + "\n"
				button = types.InlineKeyboardButton(str(n), callback_data=str(n), resize_keyboard = True)
				keyboard.add(button)
				n = n + 1
			bot.send_message(message.chat.id, text = st, reply_markup=keyboard )
#	except:
#		bot.send_message(chat_id, text = "boh c' e stato un errore prova con una canzone piu bella")
@bot.message_handler(func=gestione)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	try:
		global titles, chat_id, destination
		canzone = call.data
		dest = getMP3(canzone)
		print("fatto")

		onlyfiles = [f for f in listdir(destination) if isfile(join(destination, f))]
		print(onlyfiles)
		bot.send_audio(chat_id=chat_id, audio=open(dest + "/" + onlyfiles[0], 'rb'))
		
		

#		bot.send_message(chat_id, text = "digita il no per una nuova canzone!")
	except:
		bot.send_message(chat_id, text = "boh c' e stato un errore prova con una canzone piu bella")
def download(link):
		global destination
		video = pytube.YouTube(link)
		audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
		titolo = video.title.split(" ")
			
		destination = destination + "/" + titolo[0]
		audio.download(destination)
		print("completato")
		return destination
def titoli(titolo):
	try:
		global search
		global chat_id
		search = titolo
		videosSearch = VideosSearch(titolo, limit = 8).result()

		links = []
		title = []
		keys = ['result']
		for key in keys:
			list_videos = videosSearch.get(key)


		for titolo in list_videos:
			title.append(titolo.get('title'))
		return title
	except:
		bot.send_message(chat_id, text = "boh c' e stato un errore prova con una canzone piu bella")
def getMP3(scelta):
	try:
		global chat_id
		global search
		global destination
		videosSearch = VideosSearch(search, limit = 8).result()
		links = []
		keys = ['result']
		for key in keys:
			list_videos = videosSearch.get(key)
		for url in list_videos:
			links.append(url.get('link'))

		video = pytube.YouTube(links[int(scelta)])
		audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
		titolo = video.title.split(" ")
			
		destination = destination + "/" + titolo[0]
		audio.download(destination)
		print("completato")
		return destination
	except:
		send_message(chat_id, text = "boh c' e stato un errore prova con una canzone piu bella")
			



bot.polling()