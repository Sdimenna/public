import requests 
from bs4 import BeautifulSoup
import smtplib
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from collections import OrderedDict
import time
import random
from amazon_affiliate_url import AmazonAffiliateUrl, Country
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

Link = 'https://www.amazon.it/gp/goldbox?pf_rd_r=R433XET4W0GQ48X071Q7&pf_rd_p=488756fd-9e73-4604-9865-87bff840635f&pd_rd_r=4fe5995b-9ce7-49bf-815f-3f615daa00b2&pd_rd_w=TVPhr&pd_rd_wg=fjxje&ref_=pd_gw_unk'
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

def get_asin(URL_product):
    try:
        separate = URL_product.split('/')

        asin = separate[5]

        return asin[0:10]
    except:
        print("error")
def get_url(asin):
    try:
        ASIN = asin
        TAG =  '190e8f-21'

        URL= AmazonAffiliateUrl.url_cls(asin_or_url=ASIN, affiliate_tag=TAG, country=Country.Italy)

        modURL = URL[:-3]

        return modURL   
    except:
        print("error")

def rimuovi_cookie(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='sp-cc-accept']"))).click()

    print("cookie accettati")


def search_productOffer_tech(URL,headers):
    try:
        page = requests.get(URL,headers = headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        products = soup.find_all('li', "a-list-normal")

        #print(products)
        info = []
        for prod in products:
            link = prod.find('a', {'class' : 'a-size-base a-color-base a-link-normal a-text-normal'})['href']
            info.append(link)
        return list(dict.fromkeys(info))
    except:
        print("error")

def cambio_pagina(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']"))).click()
    
    print("Navigating to Next Page")

def get_all_links(driver):
    links = []

    rimuovi_cookie(driver)
    for i in range(15):
        time.sleep(5)
        elements = driver.find_elements(By.XPATH, "//a[@class = 'a-link-normal']")
        for elem in elements:
            href = elem.get_attribute("href")
            links.append(href)
        
        cambio_pagina(driver)
    
    lista_senza_rip = list(OrderedDict.fromkeys(links))
    #   print(lista_senza_rip)
    return lista_senza_rip

def avvio_selenium(Link):
    chrome_driver = ChromeDriverManager().install()
    driver = Chrome(service=Service(chrome_driver))

    driver.maximize_window()
    driver.get(Link)
    time.sleep(2)
    return driver

def check_links(lista_link,headers):

    link_funzionante = []
    
    for lnk in lista_link:
        try:
            prodotti = search_productOffer_tech(lnk,headers)
            link_funzionante.append(lnk)
        except:
            try:
                link_funzionante.append(lnk)
            except:
                pass

    
    link_funzionante = list(set(link_funzionante))
#   print(link_funzionante)
    return link_funzionante

def scrivi_csv(lista):
    with open("miei_link", 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(lista)

    print("fine scrittura...")

def main(Link, headers):
    driver = avvio_selenium(Link)
    tuttiLink = get_all_links(driver)
#   print(tuttiLink)
    link_funzionanti = check_links(tuttiLink,headers)
    scrivi_csv(link_funzionanti)
    print("-finish-")
main(Link,headers)