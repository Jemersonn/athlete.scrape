import csv
import requests
from bs4 import BeautifulSoup

athlete_id = 14102990;

url = "https://www.athletic.net/TrackAndField/Athlete.aspx?AID=" + str(athlete_id)
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

#set up title
title = str(soup.title.string)
title = title.replace('\n','').replace('\t','').replace('\r','')
athlete_name = title.split('-')[0]

#open file, write name
file = open("athlete_times.txt", "r+")
file.write("Name: %s\n" % athlete_name + '\n')

for text in soup.find_all('h5'):
	#print season titles and event name neatly
	if "Season" in str(text):
		file.write(('\n' + '\n' + str(text.contents[0])))
	elif ("DMR") in str(text) or ("Relay") in str(text):
		pass
	else:
		#store event name for printing later
		event_name = ('\n' + str(text.contents[0]) + '\n')

		#make long string of siblings ending when hitting an event name
		block = ""
		for i in range(0,100):
			try:
				text = text.find_next_sibling()
				block = block + str(text) + '\n'
				if text.name == 'h5':
					block = block + '\n'
					break
			except:
				pass

		#sift through long string and add to list of times to write
		timesToWrite = []
		soupBlock = BeautifulSoup(block, features="html.parser")
		for t in soupBlock.select('tr td:nth-of-type(2) [href^="/result"]'):
			if not t.contents[0].startswith(("DN", "SCR", "NT")):
				timesToWrite.append(str(t.contents[0]) + '\n')

		#if the event has times, then write event name and all times
		if not len(timesToWrite) == 0:
			file.write(event_name)
			for time in timesToWrite:
				file.write(time)

file.close()
