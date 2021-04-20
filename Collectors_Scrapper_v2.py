# An url scrapper -- it gets the latest additions to the website every hour 
# and sends them directly to an e-mail address.
# Optimised to be used as a scheduled script on Google Cloud Platform

import requests
import pandas as pd
import email.message
import smtplib
import ssl
import os
from bs4 import BeautifulSoup
from datetime import datetime

def generate_email(sender, recipient, subject, body):
	message = email.message.EmailMessage()
	message["From"] = sender
	message["To"] = recipient
	message["Subject"] = subject
	message.set_content(body)

	return message

def send_email(message):
	port = 465
	password = "vqqozuwlckthncow"
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login("devbotalex@gmail.com", password)
		server.send_message(message)
		server.quit()

def url_scrapping (url):
	l= []
	r = requests.get(url, 
	                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
	c = r.content
	soup = BeautifulSoup(c,"html.parser")

	all = soup.find_all("div", {"class":"offer-wrapper"})

	for item in all:
	    item_dict = {}
	    date = item.find_all("div", {"class":"space rel"})[1].find_all("span")[1].text
	    if "Azi" in date:
	        item_dict ["Name"] = item.find("a", {"class":"marginright5"}).text.strip()
	        item_dict["Price"] = int(item.find("p", {"class":"price"}).text.strip().split()[0])
	        item_dict["Location"] = item.find_all("div", {"class":"space rel"})[1].find('span').text
	        item_dict["Link"] = item.find("a", href=True)["href"]
	        l.append (item_dict)
	    
	df = pd.DataFrame(l)
	return df

def webcrawler():
	df = url_scrapping("https://www.olx.ro/oferte/q-gameboy/")
	df_string = df.to_string()
	if 'Empty' in df_string:
		body = 'There are no new entries at this moment.'
	else:
		body = df_string
	title = "Report generated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)
	message = generate_email('devbotalex@gmail.com', 'alex.stanuta@gmail.com', title, body)
	send_email(message)
