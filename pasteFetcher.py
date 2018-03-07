#!/usr/bin/python3

'''
Pastebin API scraper

https://pastebin.com/api_scraping_faq


'''
import requests, sqlite3, time, os


api_dev_key = ''    			#### update this
api_user_key = ''  			    #### update this

api_results_limit = '100'
api_option = 'list'
pastebin_vars = {'api_dev_key':api_dev_key,'api_user_key':api_user_key,'api_results_limit':api_results_limit,'api_option':api_option}

currentPath = os.cwd()
pastesPath = currentpath+"/pastes"  



startTime = time.time()

r = requests.post("https://pastebin.com/api_scraping.php?limit=100", data = pastebin_vars)

data = r.json()

i = 0
name = []

# Pastebin wants you to make this scrape request once per minute, 
# then take scrape urls and fetch them all
for p in data:
	paste = data[i]['scrape_url']
	i = i + 1
	name.append(paste) # this is the minutely list of downloads

# fetch db items and load them into a list
conn = sqlite3.connect("pastes.db")
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
query = c.execute("select name from pastes")
pasteDb = c.fetchall()

fc = 0
urls = name
for link in urls:
	if link not in pasteDb:
		linkName = link[43:]
		rawReq = requests.get(link)
		raw2Save = rawReq.text
		#print (raw2Save)
		raw2Save = raw2Save.encode('utf-8')
		outFile = open(pastesPath+linkName, "w")
		outFile.write(raw2Save)
		outFile.close()

		conn = sqlite3.connect('pastes.db')
		c = conn.cursor()
		try:
			c.execute("INSERT INTO pastes(name) VALUES (?)",[link])
			print ("Saved: {} to DB".format(link))
			conn.commit()
			conn.close()
			fc = fc + 1
		except sqlite3.IntegrityError:
			print ("Already have: {}".format(link))
			break

endTime = time.time()
duration = endTime - startTime

print ("Fetched {} pastes.".format(fc))
print ("Finished in {} seconds.".format(duration))

# TODO: purge db every 5 minutes, maybe cron job to copy a fresh copy of the db? schedule at the 50sec mark?

