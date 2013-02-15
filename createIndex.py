# createIndex.py
# file 1 for project

# need sqrt and floor so that skips can occur every floor(sqrt(L)) pageID's where L = #pageID's
from math import sqrt
from math import floor

from XMLparser import parse
from porter import stem

# input: filename (fname) of the stopWords file
# output: set of stopwords
def create_stopwords_set(fname):
	f = open(fname, 'r')
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


def fakeParse():
	d = {}
	for i in range(10):
		s = "This is the number "+str(i)
		s_text = "Even though I said +"+str(i)+", really "+str(i-1)+" is my favorite number"
		d[i] = (s.split(), s.split()+s_text.split())
	return d


# input: <stopWords file>, <pagesCollection file>, <invertedIndex to be built>, <titleIndex to be built>
# output: write to the files
def createIndex(stopwords_filename, pagesCollection_filename, ii_filename, ti_filename):
	# open up the files for writing
	invertedIndex_file = open(ii_filename, 'w')
	titleIndex_file = open(ti_filename, 'w')

	# obtain the stopwords in a set for quick checking
	stopWords_set = create_stopwords_set(stopwords_filename)
	
	# initialize empty index
	index = {}

	# obtain dictionary mapping pageID's to tuple (list of title words, list of title and text words)
	#collection = parse(pagesCollection)
	collection = fakeParse()
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
			word = ''.join(ch for ch in word if ch.isalnum())
			# 3) filter out all the tokens matching element of stopwords list
			if word in stopWords_set:
				continue
			# 4) stem each remaining token using porter stemmer
			word = stem(word)
			# now put word in index which has structure: 
				#{'word': [<#occurances>, [[pageID,, <skiplist pointer(to be put later)>, [position for position in page]]for each pageID]}
			if not word in index:
				# create new entry in index:  occurances = 0
				index[word] = [0,[]]
			# increase number of occurances of word in dictionary

			index[word][0] = index[word][0] + 1
			postings = index[word][1]
			# check if we need to add position to already posted document
			if (len(postings) > 0) and (pageID == postings[len(postings)-1][0]):
				# append position
				positions = postings[len(postings)-1][1]
				positions.append(position)
			else:
				# append document
				postings.append([pageID, [position]])
			# now just adjust position
			position += 1

	# now the index is built
	titleIndex_file.close() # done writing to titleIndex

	# write out index in format:  word occurances&pageID_0%skipToIndex%pos_0 pos_1&pageID_1 skipToIndex%pos_0 pos_1 pos2&pageID_2 skipToIndex skipToPageID%pos_0

	# print one line for each word in index and add skip list pointers while printing to file
	for word in index:
		w_info = index[word]
		w_occurances = w_info[0]
		w_postings = w_info[1]
		invertedIndex_file.write(word+" "+str(w_occurances)) # so far have: "word occurances"
		
		# for adding skips need to know how often to skip and counter for when to skip
		skip = int(floor(sqrt(len(w_postings))))
		skip_count = 0

		for i in range(len(w_postings)):
			post = w_postings[i]
			page_ID = post[0]
			positions = post[1]

			invertedIndex_file.write("&"+str(page_ID))  # so far have: "word occurances&page_ID"
			if skip_count == skip:
				# print skipToIndex 
				skipToIndex = i+skip
				if len(post) < skipToIndex:  # checks that there's a next document to skip to
					invertedIndex_file.write("%"+str(skipToIndex))  # so far have: "word occurances&page_ID skipToIndex"
				# reset skip counter
				skip_count = 0
			else: # increment skip_count
				skip_count += 1	

			# write out positions list
			invertedIndex_file.write("%"+str(positions[0]))
			for p in range(1, len(positions)):
				invertedIndex_file.write(" "+str(positions[p])) # so far have: "word occurances&page_ID skipToIndex%pos_0 pos_1 pos_2, ..."

		invertedIndex_file.write('\n')
	invertedIndex_file.close()
	return index
				
		
		









