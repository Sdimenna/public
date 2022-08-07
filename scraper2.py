import random
import time
from amazon_affiliate_url import AmazonAffiliateUrl, Country
from bs4 import BeautifulSoup
import requests
import telegram
import csv

# PROGRAMMA MADE BY DI MENNA SIRO LEON alias SDIMENNA01 
#questo programma consente di ottere il link affiliato amazon ma non è molto efficace dato che non utilizza api da amazon ma esegue uno web-scraping
# e quindi in futuro avrà bisogno di una manuntenzione.


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


#FUNZIONE che ricava il link affiliato
def get_url(asin):
	ASIN = asin
	TAG =  '190e8f-21'

	URL= AmazonAffiliateUrl.url_cls(asin_or_url=ASIN, affiliate_tag=TAG, country=Country.Italy)

	modURL = URL[:-3]

	return modURL

#FUNZIONE che mi trova il codice Asin del prodotto, utile per ricavare link affiliato
def get_asin(URL_product):

	separate = URL_product.split('/')

	asin = separate[5]

	return asin[0:10]


# FUNZIONE che mi permette trovare tutti i prodotti della categoria tech
def search_productOffer_tech(URL):

	#URL = 'https://www.amazon.it/deal/c97b811f?showVariations=true&ref=dlx_deals_gd_dcl_img_6_c97b811f_dt_sl6_6d'
	page = requests.get(URL,headers = headers)

	soup = BeautifulSoup(page.content, 'html.parser')

	products = soup.find_all('li', "a-list-normal")

	#print(products)
	info = []
	for prod in products:
		link = prod.find('a', {'class' : 'a-size-base a-color-base a-link-normal a-text-normal'})['href']
		info.append(link)
	return list(dict.fromkeys(info))


def get_price(URL):

	page = requests.get(URL,headers = headers)

	soup = BeautifulSoup(page.content, 'html.parser')


	try:
		price = soup.find(id = 'corePrice_feature_div').get_text()
		
		#print("price", price)
		ex_price = soup.find('span', {'class' : "a-price a-text-price a-size-base"}).get_text()

	except:
		price = soup.find('td', {'class' : "a-color-secondary a-size-base a-text-right a-nowrap"}).get_text()
		#print("prezzo_")
	
	c_price = price.split("€")
	c_ex_price = ex_price.split('€')

	all_price = c_price[0] + '/' + c_ex_price[1]
	
	return all_price


def get_Title(URL):
	page = requests.get(URL, headers = headers)

	soup = BeautifulSoup(page.content, 'html.parser')

	#print(soup.prettify())

	title = soup.find('span', {'class' : "a-size-large product-title-word-break"}).get_text()

	title.split(',')
	return title

def send_message_Telegram(Link_affiliato, vecchio_prezzo, nuovo_prezzo, percentuale_scontata, titolo):
#	chrome_driver = ChromeDriverManager().install()
#	driver = Chrome(service=Service(chrome_driver))

#	token  = '5367203183:AAGazC_CBHZVJla6B9NuMLV3EyoeVPJ7LV4'
	
#	URL_mess = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=@asasasassssssssssssss&text='  + Link_affiliato
#	driver.get(URL_mess)



#	bot = telebot.TeleBot('5367203183:AAGazC_CBHZVJla6B9NuMLV3EyoeVPJ7LV4')


#	bot.send_message(message.channel.id, 'ciao')

#	bot.polling()	
	
	emoji = ['🔥', '🎉', '😎' , '🙌' , '🤑']

	con_vecchio_prezzo = str(vecchio_prezzo)
	con_nuovo_prezzo = str(nuovo_prezzo)

	bot = telegram.Bot('TOKEN BOT')

	testo_lungo =  '\n' + titolo.strip() + '\n' + '\n' + "<b>PASSA DA " + con_vecchio_prezzo + "€ A SOLI " + con_nuovo_prezzo + '€ </b>'+ random.choice(emoji) + '\n' +  " <a href ='" + Link_affiliato + "'><b>👉clicca qui👈</b></a>"
	bot.send_message(text=testo_lungo, chat_id = '@asasasassssssssssssss', parse_mode=telegram.ParseMode.HTML )

	print("messaggio inviato...")

def leggi_csv():
	URL = []
	with open('miei_link', "r") as readfile:
		read = csv.reader(readfile)
		for line in read:
			for l in line:
				URL.append(l)
	print(URL)
	return URL
	
	

#cuore del programama
def main():


#	array che contiene tutti gli url amazon utili
	URLS = leggi_csv()
	

	esecuzioni = 0 
	count_errori = 0
	while True:
		try:
			esecuzioni = esecuzioni + 1
		#seleziono un url casuale dall' array e poi prendo un 
		#prodotto casuale per infine creare il link affiliato. alla fine conto i numeri di errore
			try:
				URL = random.choice(URLS)
			except:
				URL = random.choice(URLS)	
			ControlloURL = URL.split('/')
			if ControlloURL[3] == 'deal':
				product = search_productOffer_tech(URL)
				try:
					productChoosen = random.choice(product)
				except:
					productChoosen = random.choice(product)
				stringCompleta = "https://www.amazon.it" + productChoosen
				asin = get_asin(stringCompleta)
			else:
				asin = get_asin(URL)
			#print(asin)
			
			Link_affiliato = get_url(asin)
		#	print(Link_affiliato)
			prezzo = get_price(Link_affiliato)
			prezzi = prezzo.split('/')

				
			try:
				vecchio_prezzo = float(prezzi[1].replace(',','.'))
				nuovo_prezzo = float(prezzi[0].replace(',','.'))
					
					
			except:
				vecchio_prezzo = prezzi[1]
				nuovo_prezzo = prezzi[0]
				
				maketrans = vecchio_prezzo.maketrans
				vecchio_prezzo = vecchio_prezzo.translate(maketrans(',.', '.,'))
				
				maketrans = nuovo_prezzo.maketrans
				nuovo_prezzo = nuovo_prezzo.translate(maketrans(',.', '.,'))

				vecchio_prezzo = vecchio_prezzo.replace(',','')
				nuovo_prezzo = nuovo_prezzo.replace(',','')
				#print(vecchio_prezzo, nuovo_prezzo)

			differenza_prezzo = float(vecchio_prezzo) - float(nuovo_prezzo)
			percentuale_scontata = 100 - ((float(vecchio_prezzo) - (differenza_prezzo))/float(vecchio_prezzo)) * 100 

			titolo = get_Title(Link_affiliato)
		

			print(Link_affiliato)

			print(nuovo_prezzo)
			print(vecchio_prezzo)
			print(titolo)
				
			send_message_Telegram(Link_affiliato, vecchio_prezzo, nuovo_prezzo, percentuale_scontata, titolo)
#			time.sleep(300)

		except:
			count_errori = count_errori+1
			print(count_errori)


main()
