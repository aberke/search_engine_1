# XML parser used in createIndex

import re
from porter import stem as stemToken

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
    
# input: string to turn into list of tokens
# output: list of tokens
def tokenize(stopWords_set, textString):
    token_list = []
   
    # 1) lowercase all the words in the stream, 
    textString = textString.lower()
    # 2) obtain the tokens (strings of alphanumeric characters [a-z0-9], terminated by a non alphanumeric character) 
    textString = re.sub('[^0-9a-zA-Z]+', ' ', textString)
    # split textString into list of words   
    text_list = textString.split()
    # 3) filter out all the tokens matching element of stopwords list
    for word in text_list:
        if not word in stopWords_set:
            word = stemToken(word)
            token_list.append(word)
    return token_list


#input: filename (fname) of the file collection
#output: dictionary mapping pageID to tuple 
# pageID: (titleString, textString)

def parse(fname):
    f = open(fname)
    pageID = ""
    dictionary = {} #dictionary initially empty

    # loop through entire document by line
    currLine = f.readline()
    while currLine:
        wordsList = []

        while (not "<id>" in currLine and currLine): currLine = f.readline()
        # currLine now contains the pageID, so parse that as needed
        currLine = currLine.replace("<id>", "")
        currLine = currLine.replace("</id>\n", "")
        if not currLine:
            break
        pageID = int(currLine)

        while (not "<title>" in currLine and currLine): currLine = f.readline()
        # currLine now contains the title, so parse that as needed

        titleString = currLine[7:len(currLine)-9]+'\n'

        #Do we need to remove the \n we added to the titleString??
        textString = titleString 

        while (not "<text>" in currLine and currLine): currLine = f.readline()
        # now we've reached the <text> section, so iterate through lines until reaching the end at </text>
        currLine = currLine.replace("<text>", "")
        while (not "</text>" in currLine and currLine):
            textString == textString + currLine
            currLine = f.readline()

        #now we know we've reached the last line of </text>
        currLine = currLine.replace("</text>", "")
        textString == textString + currLine

        titleTextTuple = titleString, textString
        dictionary.update({pageID:titleTextTuple})  #add entry for this page into dictionary
        currLine = f.readline()

    return dictionary