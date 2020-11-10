# An url scrapper -- it gets the latest additions to the website
# and sends them in csv format to an e-mail address.

#!/usr/bin/env python

import requests
import pandas as pd
import Email_Sender
import os
from bs4 import BeautifulSoup
from datetime import datetime

def url_scrapping (url):
	l = []
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
	df.to_csv("olx_gameboy_hourly_report.csv", index=False)
	return print("Scrapping OK!")

if __name__ == "__main__":
	url_scrapping("https://www.olx.ro/oferte/q-gameboy/")
	title = "Report generated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)
	if os.path.getsize("olx_gameboy_hourly_report.csv") != 0:
		message = Email_Sender.generate_email('sender@gmail.com', 
					'recepient@gmail.com', title, "New Report", 
					"olx_gameboy_hourly_report.csv")
	else:
		message = Email_Sender.generate_email('sender@gmail.com', 
					'recepient@gmail.com', title, "There are no new items")
	Email_Sender.send_email(message)