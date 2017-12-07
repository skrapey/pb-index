#!/usr/bin/python3

'''
Pastebin API scraper
https://pastebin.com/api_scraping_faq

'''
import requests 

pastesPath = "/path/to/pastes"  #### update this
api_dev_key = ''    			#### update this
api_user_key = ''  			    #### update this

api_results_limit = '100'
api_option = 'list'

pastebin_vars = {'api_dev_key':api_dev_key,'api_user_key':api_user_key,'api_results_limit':api_results_limit,'api_option':api_option}


r = requests.post("https://pastebin.com/api_scraping.php?limit=100", data = pastebin_vars)
data = r.json()


i = 0
urls = []

# Pastebin wants you to make this scrape request once per minute, likely control this with cron
# Then we will take scrape urls and fetch them all
for p in data:
	paste = data[i]['scrape_url']
	i = i + 1
	urls.append(paste)


for link in urls:
	linkName = link[43:]
	rawReq = requests.get(link)
	raw2Save = rawReq.text
	#print (raw2Save)
	outFile = open(pastesPath+linkName, "w")
	outFile.write(raw2Save)
	outFile.close()


