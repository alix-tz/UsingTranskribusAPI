import os, datetime
from bs4 import BeautifulSoup
import lxml.etree as etree
from config import singlecollectionnames as collections

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
	BUILDING SINGLE XML DOCUMENT(PAGE FORMAT) FROM MULTIPLE XML FILES

	Script ran at : %s
	For collection %s.

	---------------------
""" % (now, collist)
	with open(filepath, "w") as f:
		f.write(intro)
	return


def createlog(log):
	""" Add logs to current log file
	"""
	filepath = os.path.join(pathtologs, "log-%s.txt") % (timestamp)
	with open(filepath, "a") as f:
		f.write(log)
	return

# ========================== #

now = datetime.datetime.now()
timestamp = "%s-%s-%s-%s-%s" % (now.year, now.month, now.day, now.hour, now.minute)
currentdirectory = os.path.dirname(os.path.abspath(__file__))
datacontent = os.path.join(currentdirectory, "data")
pathtologs = os.path.join(currentdirectory, "__logs__")
initiateLog()

for collection in collections:
	path = os.path.join(datacontent, collection)
	pathtoexports = os.path.join(path, "__AllInOne__")

	# PREPARING FILES
	try: 
		verifycollections = os.listdir(datacontent)
		if collection in verifycollections:
			createFolder(pathtoexports)
			try:
				collectioncontent = os.listdir(path)
				if "__TextExports__" in collectioncontent:
					collectioncontent.remove("__TextExports__")
				if "__AllInOne__" in collectioncontent:
					collectioncontent.remove("__AllInOne__")

				if len(collectioncontent) > 0:
					for document in collectioncontent:
						needend = False
						counter = 0
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
								# SORT
								sortedcontent.sort()
								# REBUILD FILE NAMES
								foldercontent = []
								for filename in sortedcontent:
									filename = "%s.xml" % (filename)
									foldercontent.append(filename)

								pathtoexport = os.path.join(pathtoexports, "%s.xml") % (document)
								# CREATE CONTENT FOR THE NEW FILE
								# CREATE HEADER
								i = 0
								top = len(foldercontent)
								while i != top:
									firstpagefile = os.path.join(pathtodoc, foldercontent[i])
									with open(firstpagefile, "r") as f:
										content = f.read()
									soup = BeautifulSoup(content, "xml")
									if soup.PcGts:
										intro = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15/pagecontent.xsd">"""
										header = intro + str(soup.Metadata) + "\n<PageGrp>"
										with open(pathtoexport, "w") as f:
											f.write(header)
										needend = True
										i = top
									else:
										i += 1
								# CREATE CONTENT
								for file in foldercontent:
									filepath = os.path.join(pathtodoc, file)
									with open(filepath, "r") as f:
										content = f.read()
									soup = BeautifulSoup(content, "xml")
									if soup.PcGts :
										counter += 1
										page = soup.Page									
										with open(pathtoexport, "a") as f:
											f.write("\n" + str(page))
								# CLOSE LAST TAGNAMES
								if needend is True:
									with open(pathtoexport, "a") as f:
										f.write("\n</PageGrp>\n</PcGts>")
									log = "Created 1 mashup file for '%s', from a total of %s file(s).\n" % (document, counter)
									createlog(log)
						except Exception as e:
							print(e)
			except Exception as e:
							print(e)
		else:
			print("No such collection name in data directory!")
	except Exception as e:
		print(e)


