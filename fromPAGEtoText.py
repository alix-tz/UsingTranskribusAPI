import os, datetime
from bs4 import BeautifulSoup
from config import textcollectionnames as collections

# ========================== #

def createFolder(directory):
	"""Creates a new folder
	source : https://gist.github.com/keithweaver/562d3caa8650eefe7f84fa074e9ca949
	"""
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError as e:
		print(e)
	return


def initiateLog():
	"""Initiates a log file with a timestamp
	"""
	collist = ""
	for collection in collections:
		collist = collist + "'%s' " % (collection)
	filepath = os.path.join(pathtologs, "log-%s.txt") % (timestamp)
	intro = """
	TRANSFORMING XML FILES (PAGE FORMAT) TO TEXT FILES

	Script ran at : %s
	For collections %s.

	---------------------
""" % (now, collist)
	with open(filepath, "w") as f:
		f.write(intro)
	return


def createlog(counter, pagecounter, document):
	""" Add logs to current log file
	"""
	if counter == 0:
		log = "No .xml file in '%s' directory.\n\n" % (document)
	else:
		log = "Found %s .xml file(s) in '%s' directory.\n" % (counter, document)
		if pagecounter == 0:
			log = log + "\tNo .xml file matched PAGE format (root must be '<PcGts>'.\n\n"
		else:
			log = log + "\tFound %s .xml file(s) matching PAGE format.\n\n" % (pagecounter)

	filepath = os.path.join(pathtologs, "log-%s.txt") % (timestamp)
	with open(filepath, "a") as f:
		f.write(log)
	return


# ========================== #

now = datetime.datetime.now()
timestamp = "%s-%s-%s-%s-%s" % (now.year, now.month, now.day, now.hour, now.minute)
currentdirectory = os.path.dirname(os.path.abspath(__file__))
pathtologs = os.path.join(currentdirectory, "__logs__")
initiateLog()

for collection in collections:
	path = os.path.join(currentdirectory, "data", collection)
	pathtotextexport = os.path.join(path, "__TextExports__") 
	createFolder(pathtotextexport)

	# PREPARATION DES FICHIERS

	try:
		collectioncontent = os.listdir(path)
		if "__TextExports__" in collectioncontent:
			collectioncontent.remove("__TextExports__")
		if "__AllInOne__" in collectioncontent:
			collectioncontent.remove("__AllInOne__")

		if len(collectioncontent) > 0:
			for document in collectioncontent:
				pathtodoc = os.path.join(path, document)
				try: 
					foldercontent = os.listdir(pathtodoc)
					sortedcontent = []
					if len(foldercontent) > 0:
						# METTRE LES FICHIERS XML DANS L'ORDRE
						# transformer les noms de fichiers en integer quand c'est possible
						for filename in foldercontent:
							if filename.endswith(".xml"):
								filename = filename.replace(".xml", "")
								try:
									sortedcontent.append(int(filename))
								except:
									sortedcontent.append(filename)
						sortedcontent.sort()
						if len(sortedcontent) > 0:
							textfile = os.path.join(pathtotextexport, "%s.txt") % document
							with open(textfile, "w") as f:
								f.write("")

						counter = 0
						foldercontent = []
						for filename in sortedcontent:
							filename = str(filename) + ".xml"
							counter += 1
							foldercontent.append(filename)

	# RECUPERATION DU TEXT DES FICHIERS XML
						pagecounter = 0
						for file in foldercontent:
							pagenr = file.replace(".xml", "")

							filepath = os.path.join(pathtodoc, file)
							with open(filepath, "r") as f:
								content = f.read()
							soup = BeautifulSoup(content, "xml")
							if soup.PcGts:
								pagecounter += 1
								textregions = soup.find_all("TextRegion")
								for textregion in textregions:
									regionid = textregion['id']
									textequivs = textregion("TextEquiv", recursive=False)
									for textequiv in textequivs:
										text = textequiv.Unicode.get_text()
	# CREATION DES FICHIERS TEXTE
	# avec signalement des séparations de zones et de pages 
										with open(textfile, "a") as f:
											f.write("%s\n\n[.../R fin de la zone %s]\n\n" %(text, regionid))
								with open(textfile, "a") as f:
									f.write("\n[.../... fin de la page %s]\n\n" % (pagenr))
						createlog(counter, pagecounter, document)



				except Exception as e:
					print(e)
	except Exception as e:
		print(e)

