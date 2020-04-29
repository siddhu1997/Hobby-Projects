import os
import sys
import re
import random

os.system('color') #For windows based machines

#creating a list of years so that we can randomly select a year from the list to get film plots each time

years = [str(i) for i in range(1879,2020)]
domain = 'https://en.wikipedia.org'

try:
	try:
		import requests
		from bs4 import BeautifulSoup
	except Exception as e:
		print("\033[1;31;40m"+str(e)+"\033[1;37;40m")
		sys.exit(0)
	n = int(sys.argv[1])


except IndexError:
	print('\033[1;37;41mPlease supply number of "Films" to be scrapped as a command line argument! \033[1;37;40m')
	print("\033[1;33;40mSupply number of films now? [Y]es or [N]o\033[1;37;40m")
	choice = input()
	if choice.lower() == 'n' or choice.lower() == 'no':
		print("\033[1;37;41mSorry cannot proceed further! Exiting...\033[1;37;40m")
		sys.exit(0)
	elif choice.lower() == 'y' or choice.lower() == 'yes':
		print("Enter number of films: ")
		n = int(input())
	else:
		print("\033[1;37;41mDidn't get you...Quitting!\033[1;37;40m")
		sys.exit(0)
 
except:
	print("\033[1;37;41mERROR: Please check if all the necessary libraries are installed properly! \033[1;37;40m")
	sys.exit(0)

film_links = list()
f_film_links = list()
previous_length = len(f_film_links)

if os.path.exists("flinks.txt"):
	os.remove("flinks.txt")

#Remove Production/Film houses names by importing filter.txt

if not os.path.exists("filter.txt"):
	print("\033[1;31;40m[!]'filter.txt', a file used to identify false links is missing.\n[!]Without it, chances of successfully scrapping is drastically reduced!\n[!]Please add the file to the present working directory!\033[1;37;40m")
	sys.exit(0)

if not os.path.exists("output"):
	os.mkdir("output")

if os.path.exists("/output/plot_dataset.txt"):
	os.remove("/output/plot_dataset.txt")

### Phase 1 Link Extraction

try:
	with requests.session() as _session_:

		_session_.headers['user-agent'] = 'Mozilla/5.0'

		print("\033[1;32;40m[+] Scrapping started!\033[1;37;40m")
		while len(years) != 0 and len(f_film_links) <= n:
			year = random.choice(years)
			years.remove(year)
			#year = '1939'

			url = "https://en.wikipedia.org/wiki/"+year+"_in_film"
			req = _session_.get(url)

			print("\033[1;33;40m=> Trying Year: "+year+"\033[1;37;40m") 				#To not to repeat films from same years
			print("Requesting URL: \033[2;37;40m"+url+"\033[1;37;40m")

			parser = BeautifulSoup(req.content,'html5lib')
			table = str(parser.find('table',{'class':'wikitable sortable'}))
			parser = BeautifulSoup(table,'html5lib')

			for link in parser.find_all('a'):
				film_links.append(link.get('href'))

			for i in film_links:
				if re.search(r'^#cite',i):
					film_links.remove(i)
				elif re.search(r'^#end',i):
					film_links.remove(i)

			flinks = open('flinks.txt','a')

			for i in film_links:
				flinks.write(i+"\n")

			film_links = list()
			flinks.close()
			flinks = open('flinks.txt','r')
			_filter = open('filter.txt','r') 

			for link in flinks:
				film_links.append(link)
			flinks.close()
			dup = list()
			for link in _filter:
				dup.append(link)

			index = list()
			for i in range(len(film_links)):
				if film_links[i] in dup:
					index.append(i)

			#f_film_links = list() 						#filtered film_links
			for i in range(len(film_links)):
				if i in index:
					continue
				else:
					f_film_links.append(film_links[i])

			f_film_links = list(dict.fromkeys(f_film_links))

			k = 0
			f_len = len(f_film_links)

			while(k < f_len):
				if(f_film_links[k] == "\n"):
					f_film_links.remove(f_film_links[k])
					f_len = f_len - 1
				k = k + 1

			if previous_length == len(f_film_links):
				print("\033[1;31;40m[-] No Highest-grossing films section found in year: ",year+"\033[1;37;40m")
			elif len(f_film_links) < n:
				print("\033[1;33;40m[!] Acquired film links lesser than user requested count! Trying another year...Current numbers: ",len(f_film_links),"\033[1;32;40m")
				previous_length = len(f_film_links)
			else:
				print("\033[1;32;40m[+] Acquired Film Links: ",len(f_film_links),", and number of links user requested:",n,"\033[1;37;40m")
				break

except Exception as e:
	print(e)
	sys.exit(0)

_filter.close()

### Phase 2 plot extraction

plot = list()

f_film_links = [ i[:-1] for i in f_film_links] 	#removing '\n' from the urls!

try:

	with requests.session() as s:
		for link in f_film_links: 
			url = domain + link
			req = s.get(url)
			parser = BeautifulSoup(req.content,'html5lib')
			tag = parser.select_one('#Plot')
			if tag == None:
				continue
			else:
				print("Requesting Film URL: \033[1;35;40m",url+"\033[1;37;40m")
				tag = tag.find_parent('h2').find_next_sibling()
				while tag.name == 'p':
					plot.append(tag.text)
					tag = tag.find_next_sibling()

	plot_len = len(plot)

	if plot_len != 0:
		directory = "output"
		file = "plot_dataset.txt"
		path = os.path.join(directory,file)
		fp_plot = open(path,"w")
		for paragraph in plot:
			fp_plot.write(paragraph)
		fp_plot.close()
		print("\033[1;32;40m[+]Scrapping completed successfully! Output saved in 'plot_dataset.txt' in the output folder!\033[1;37;40m")
		sys.exit(0)

	else:
		print("\033[1;31;40m[-]Could not scrap properly! \033[1;37;40m")
		sys.exit(0)

except Exception as e:
	print("\033[1;31;40m"+str(e)+"\033[1;37;40m")