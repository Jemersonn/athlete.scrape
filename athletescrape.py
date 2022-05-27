import csv
import requests
from bs4 import BeautifulSoup

athlete_id = 14102990;
#me 14102990
#jake 6068279

url = "https://www.athletic.net/TrackAndField/Athlete.aspx?AID=" + str(athlete_id)
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

#set up title
title = str(soup.title.string)
title = title.replace('\n','').replace('\t','').replace('\r','')
athlete_name = title.split('-')[0]

#open file, write name
file = open("athlete_times.txt", "w")
file.write("Name: %s\n" % athlete_name + '\n')

for text in soup.find_all('h5'):
	#print season titles and event name neatly
	if "Season" in str(text):
		file.write(('\n' + '\n' + str(text.contents[0])))
	elif ("DMR") in str(text) or ("Relay") in str(text):
		pass
	else:
		file.write('\n' + str(text.contents[0]) + '\n')

		#make long string of siblings ending when hitting an event name
		block = ""
		numTimes = 0
		for i in range(0,100):
			try:
				text = text.find_next_sibling()
				block = block + str(text) + '\n'
				if text.name == 'h5':
					block = block + '\n'
					break
			except:
				pass

		#sift through long string and print
		soupBlock = BeautifulSoup(block, features="html.parser")
		for t in soupBlock.select('tr td:nth-of-type(2) [href^="/result"]'):
			if not t.contents[0].startswith(("DN", "SCR", "NT")):
				file.write(str(t.contents[0]) + '\n')
				numTimes += 1			
		print(numTimes)

file.close()

#currently: finding all event names (h5) and finding all times (a) and printing all times after each event name
#should: find all h5 and add to list. for each index in list, findNext from that location
