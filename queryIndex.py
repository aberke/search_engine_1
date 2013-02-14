# query index
from createIndex import create_stopwords_set


# reconstructs the invertedIndex that createIndex made by reading from file
# input: filename of inverted index file
# output: inverted index
def reconstruct_Index(ii_filename):
	# reconstruct invertedIndex from file starting with empty dictionary
	index = {} 
	ii_file = open(invertedIndex)

	line = ii_file.readline()
	while line != '': # read to EOF
		# TODO: REPLACE THIS WITH MORE EFFICIENT PARSER
		l = line.split('&') # split along the postings delimeter 
		
		# extract word and #occurances
		word_and_occurances = l[0].split()
		word = word_and_occurances[0]
		occurances = word_and_occurances[1]

		# build postings list from empty list
		postings = []
		for i in range(1, len(l)):
			p = l[i].split('%')
			if len(p) == 2:
				positions = [int(pos) for pos in p[1].split()]
				posting = [int(p[0]), 0, positions] # posting = [pageID, 0] where 0 means that there is no skip pointer here
			else:
				positions = [int(pos) for pos in p[2].split()]
				posting = [int(p[0]), int(p[1]), positions] # posting = [pageID, skip2Index]
			postings.append(posting)
		
		index[word] = [int(occurances), postings]
		line = ii_file.readline()

	ii_file.close()
	return index



def queryIndex(stopwords_filename, ii_filename, ti_filename):
	
	index = reconstruct_Index(invertedIndex)
	stopwords_set = create_stopwords_set(stopwords_filename)
	



