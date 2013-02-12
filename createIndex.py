# createIndex.py
# file 1 for project

from XMLparser import parse
from porter import stem

# input: filename (fname) of the stopWords file
# output: set of stopwords
def stopWords(fname):
	f = open(stopwords, 'r')
	stopWords_set = set()

	w = f.readline()
	while w != '': # read to EOF
		if w[len(w)-1] == '\n':
			w = w[:len(w)-1] # strip off '\n'
		# add word to set of stopWords
		stopWords_set.add(w)		

		w = f.readline()
	f.close()
	return stopWords_set

# deals with appending to the titleIndex
# store the pageID and title as they appear -- but we don't really need to store them in a datastructure since we're not doing anything special with them
# -- just print them out
#
# input: open file to write to, pageID, title as output from parsing the xml file
def titleIndex_append(f, pageID, title):
	f.write(str(pageID)+' ')
	for w in title:
		if w[len(w)-1] == '\n':
			w = w[:len(w)-1] # strip off '\n'
		f.write(w+' ')
	f.write('\n')	


# input: <stopWords file>, <pagesCollection file>, <invertedIndex to be built>, <titleIndex to be built>
# output: write to the files
def createIndex(stopwords, pagesCollection, invertedIndex, titleIndex):
	# open up the files for writing
	invertedIndex_file = open(invertedIndex, 'w')
	titleIndex_file = open(titleIndex, 'w')

	# obtain the stopwords in a set for quick checking
	stopWords_set = stopWords(stopwords)
	
	# initialize empty index
	index = {}

	# obtain dictionary mapping pageID's to tuple (list of title words, list of title and text words)
	collection = parse(pagesCollection)
	# iterate over keys (pageID's) to fill the index
	for pageID in collection:
		title_list = collection[pageID][0]
		text_list = collection[pageID][1]
		
		# add to titleIndex:
		titleIndex_append(titleIndex_file, pageID, title_list)

		# add to index:
		position = 0
		for word in text_list:
		# 1) lowercase all the words in the stream, 
			word = word.lower()
		# 2) obtain the tokens (strings of alphanumeric characters [a-z0-9], terminated by a non alphanumeric character) 
			word = ''.join(ch for ch in word if ch.isalnum()))
		# 3) filter out all the tokens matching element of stopwords list
			if word in stopWords_set:
				continue
		# 4) stem each remaining token using porter stemmer
			word = stem(word)
			

		
		










