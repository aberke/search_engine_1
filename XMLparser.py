# XML parser used in createIndex

import re
from porter import stem as stemToken


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
            word = stem(word)
            token_list.append(word)
    return token_list


#input: filename (fname) of the file collection
#output: dictionary mapping pageID to tuple 
# pageID: (titleString, textString)

def parse(fname):
    f = open(fname)
    #f = open("sampleTextCollection.dat")
    stopWordsFile = open("stopWords.dat")
    stopWords = []
    pageID = ""
    dictionary = {} #dictionary initially empty

    # Initialize stopWords list
    for line in stopWordsFile:
        stopWords.append(line)

    # loop through entire document by line
    currLine = f.readline()
    while currLine:

        wordsList = []

        while (not "<id>" in currLine): currLine = f.readline()
        # currLine now contains the pageID, so parse that as needed
        currLine = currLine.replace("<id>", "")
        currLine = currLine.replace("</id>", "")
        pageID = currLine

        while (not "<title>" in currLine): currLine = f.readline()
        # currLine now contains the title, so parse that as needed

        titleString = currLine[7:len(currLine)-9]+'\n'


        textString = titleString 
        textSTring += ' '+currLine

        word: (pageID, titleString, textString)

        # title = currLine # Save title in original form
        # currLine = re.sub('[^0-9a-zA-Z]+', ' ', currLine) #remove all non-alphanumeric characters
        # currLine = currLine.lower()     #convert to all lowercase
        # possibleNewWords = currLine.split()
        # for currToken in possibleNewWords:      # Remove stop words
        #     if stopWords.count(currToken) == 0:
        #         currToken = stemToken(currToken)
        #         wordsList.append(currToken)

        while (not "<text>" in currLine): currLine = f.readline()
        # now we've reached the <text> section, so iterate through lines until reaching the end at </text>
        currLine = currLine.replace("<text>", "")
        while (not "</text>" in currLine):
            currLine = re.sub('[^0-9a-zA-Z]+', ' ', currLine)
            currLine = currLine.lower()
            possibleNewWords = currLine.split()
            for currToken in possibleNewWords:         # Remove stop words
                if stopWords.count(currToken) == 0:
                    currToken = stemToken(currToken)
                    wordsList.append(currToken)
            currLine = f.readline()

        #now we know we've reached the last line of </text>
        currLine = currLine.replace("</text>", "")
        currLine = re.sub('[^0-9a-zA-Z]+', ' ', currLine)
        currLine = currLine.lower()
        possibleNewWords = currLine.split()
        for currToken in possibleNewWords:          # Remove stop words
            if stopWords.count(currToken) == 0:
                currToken = stemToken(currToken)
                wordsList.append(currToken)

        wordsTuple = title, wordsList
        dictionary.update({pageID:wordsTuple})  #add entry for this page into dictionary
        currLine = f.readline()

    return dictionary