# query index
import sys
import heapq # using heap to sort documents as find them
from porter import stem #porter stemmer
from bool_parser import bool_expr_ast # provided boolean parser for python2.6

from createIndex import create_stopwords_set


def test(f):
	print('start')
	l = f.readline()
	count = 0
	while l:
		count +=1 
		if l[:7]=='<text>' and not l[len(l)-9]=='</title>\n':
			print(count)
			print(line)
		l = f.readline()
	return


#word&pageID_0%pos_0 pos_1&pageID_1%pos_0 pos_1 pos2&pageID_2%pos_0

# postings = []
# word = ''
# ch = 0
# while(ch < len(line)):
# 	while(line[ch] != '&')
# 		word += line[ch]
# 		ch += 1
# 	post = []




# reconstructs the invertedIndex that createIndex made by reading from file
# input: filename of inverted index file
# output: inverted index
def reconstruct_Index(ii_filename):
	# reconstruct invertedIndex from file starting with empty dictionary
	index = {} 
	ii_file = open(ii_filename)

	line = ii_file.readline()
	while line != '': # read to EOF
		# TODO: REPLACE THIS WITH MORE EFFICIENT PARSER
		l = line.split('&') # split along the postings delimeter   [word, [post0],[post1],...]
		
		# extract word 
		word = l[0]

		# build postings list from empty list
		postings = []
		for i in range(1, len(l)):
			p = l[i].split('%')
			positions = [int(pos) for pos in p[1].split()]
			posting = [int(p[0]), positions] # posting = [pageID, positions] 
			postings.append(posting)
		
		index[word] = postings
		line = ii_file.readline()

	ii_file.close()
	return index

# helper functions to 
# input: two positions lists: positions_1 corresponds to the positions list of the first word, positions_2 corresponds to the positions list of second word
# output: new (intersection) positions list that contains exactly the entries of positions_1 
#			where there is an entry in positions_2 that is one position after a position in positions_1
# Note of use:
#	This function is meant to be called iteratively, so that if the PQ is "Space Adventure 2001", we take:
#								>>> postings_AND_positional(postings_AND_positional(index['Adventure'], index['Space']), index['2001'])
#									  	where len(index['Adventure']) < len(index['Spage']) < len(index['2001'])
def positions_AND(positions_1, positions_2):
	pass

# helper to both handle_BQ and handle_PQ -- handles the AND
# takes two postings lists and boolean where true means using for handle_BQ and false means using for handle_PQ:
#		if true: returns the intersection over the pageID's
#		if false: returns the intersection over the pageID's and positions (where position_2 directly after position_1)

# TODO: DEAL WITH UPDATING SKIP POINTERS IN INTERSECTION
def pageIDs_AND(postings_1, postings_2, handle_bool):
	intersection = []  # Even if just matching PageID's, I want this to still be a full postings list rather than just pageIDs so that we can continue to utilize skip-pointers in further iterations
	pageIndex_1 = 0
	pageIndex_2 = 0
	while (i_1 < len(postings_1)) and (i_2 < len(postings_2)):
		post_1 = postings_1[i_1]
		post_2 = postings_2[i_2]
		pageID_1 = post_1[0]
		pageID_2 = post_2[0]
		if pageID_1 == pageID_2: # pageID's match!
			if handle_bool: 
				# we're just ANDing over pageIDs so we reached a match
				intersection.append(post_1) # keep that post since it belongs in intersection
			else: 
				# we're also matching positions, so keep checking for match in positions
				positions_1 = post_1[2]
				positions_2 = post_2[2]
				position_intersection = positions_AND(positions_1, positions_2) # take intersection of positions lists
				intersection.append([pageID_1, position_intersection])
			# increment both page indecies
			i_1 += 1 
			i_2 += 1
		elif pageID_1 < pageID_2:
			skip_pointer = post_1[1]# check if there's a skip pointer there
			if skip_pointer and (postings_1[skip_pointer][0] <= pageID_2): 
				# skip to skip pointer!
				i_1 = skip_pointer
			else:
				i_1 += 1
		else: # pageID_1 > pageID_2
			skip_pointer = post_2[1]
			if skip_pointer and (postings_2[skip_pointer][0] <= pageID_1):
				# skip to skip pointer!
				i_2 = skip_pointer
			else:
				i_2 += 1
	return intersection

# helper to handle_BQ -- handles the AND
# takes two postings lists and returns the intersection over the pageID's
# uses helper function postings_AND
def BQ_AND(postings_1, postings_2):
	return postings_AND(postings_1, postings_2, true)


def BQ_OR(postings_1, postings_2):
	union = [] # I want this to still be a full postings list rather than just pageIDs so that we can continue to utilize skip-pointers in further iterations
	i_1 = 0
	i_2 = 0
	while 1:
		# check if we're at the end of one of the postings lists
		if i_1 == len(postings_1):
			# tack on the rest of the postings_2 to union and we're done
			while i_2 < len(postings_2):
				if postings_1[i_1-1][0] != postings_2[i_2][0]:
					union.append(postings_2[i_2])
				i_2 += 1
			break

		if i_2 == len(postings_2):
			# tack on the rest of the postings_1 to union and we're done
			while i_1 < len(postings_1):
				if postings_2[i_2-1][0] != postings_1[i_1][0]:
					union.append(postings_1[i_1])
				i_1 += 1
			break
		# verified we're not at the end of one of the postings lists
		post_1 = postings_1[i_1]
		post_2 = postings_2[i_2]
		pageID_1 = post_1[0]
		pageID_2 = post_2[0]
		
		if pageID_1 == pageID_2:
			union.append(post_1)
			i_1 += 1
			i_2 += 1
		elif pageID_1 < pageID_2:
			union.append(post_1)
			i_1 += 1
		else: #pageID_1 > pageID_2
			union.append(post_2)
			i_2 += 1

	return union




def handle_BQ(stopwords_set, index, query):

	# utilize #occurances here by using it to decide which AND's to compute first
	# start with smallest set always
	# eg, for >>> bool_expr_ast('here AND there\n AND again')
	#			('AND', ['here', 'there', 'again'])

	# use helper functions BQ_AND and BQ_OR

	return



# input: set of stopwords (stopwords_set)
#		 inverted index (index)
# 		 query (query) -- from which we obtain list of stream of words (stream_list) [t0, t1, t2, ..., tk]
# output: prints out the matching documents in order of pageID
# 			for FTQ matching documents contain at least one word whose stemmed version is one of the ti's
def handle_FTQ(stopwords_set, index, query):

	stream_list = query_to_stream(stopwords_set, query)
	documents_set = set() # set allow to quickly check if document already in heap
	documents_heap = [] # heap allows us to sort document ID's as we go

	for term in stream_list:
		if term in index:
			postings = index[term][1]
			for post in postings:
				pageID = post[0]
				if not pageID in documents_set:
					documents_set.add(pageID)
					heapq.heappush(documents_heap, pageID)
	documents = ''
	for i in range(len(h)):
		pageID = heapq.heappop(h)
		documents += str(pageID)+' '
	
	return documents


# input: set of stopwords (stopwords_set)
#		 inverted index (index)
# 		 query (query) -- from which we obtain list of stream of words (stream_list) [t0, t1, t2, ..., tk]
# output: prints out the matching documents in order of pageID
# 			for FTQ matching documents contain subsequence [t1, t2, .., tk] in this order with adjacent terms
def handle_PQ(stopwords_set, index, query):
	# obtain stream of terms from query -- also handles removing operators "" and newline '\n'
	stream_list = query_to_stream(stopwords_set, query)
	if not len(stream_list):
		# there were no tokens in the stream
		return ''
	documents_set = set() # set allow to quickly check if document already in heap
	documents_heap = [] # heap allows us to sort document ID's as we go	

	# obtain all postings corresponding to first word t0
	t_0 = stream_list[0]
	potential_postings = index[t_0]
	for i in range(1, len(stream_list)):
		p_i = []
		t_i = stream_list[i]


		#for post in potential_postings:

	return

# sanitizes the query into a stream of tokens (for OWQ, FTQ, AND PQ)
# input: set of stopwords (stopwords_set)
#		 query (query) to sanitize to stream of tokens
# output: stream of tokens in list form
def query_to_stream(stopwords_set, query):
	stream_list = []
	query_list = query.split() #split query into list of words
	for word in query_list:
		# lowercase all the words in the query
		word = word.lower()
		# obtain all the tokens in the stream
		word = ''.join(ch for ch in word if ch.isalnum())
		# filter out stopwords
		if word in stopwords_set or word == '':
			continue
		# stem token
		word = stem(word)
		# add resulting token to stream of tokens
		stream_list.append(word)

	return stream_list


# helper routine to queryIndex -- determines type of query and passes off to further handling
def handle_query(stopwords_set, index, query):
	# determine query type (OWQ, FTQ, PQ, BQ)
	if ('AND' in query or 'OR' in query or ')' in query or '(' in query):  # note that the boolean parser strips off trailing '\n'
		# handle BQ in its own way
		return handle_BQ(stopwords_set, index, query)

	if query[0]=='"' and query[len(s1)-1]=='"':
		return handle_PQ(stopwords_set, index, query)
		
	
	return handle_FTQ(stopwords_set, index, query)

# main function
def queryIndex(stopwords_filename, ii_filename, ti_filename):
	
	index = reconstruct_Index(ii_filename)
	stopwords_set = create_stopwords_set(stopwords_filename)
	
	while 1: # read queries from standard input until user enters CTRL+D
		try:
			query = sys.stdin.readline()
		except KeyboardInterrupt:
			break
		if not query:
			break
		documents = handle_query(stopwords_set, index, query)
		print(documents)
	return	



