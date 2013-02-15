TEAM_NAME: Alex and Spencer

FULL_NAME: Alexandra Berke (SUBMITTER)
CS_LOGIN: aberke
EMAIL_ADDRESS: alexandra_berke@brown.edu

FULL_NAME: Spencer Caplan (TEAM-MATE)
CS_LOGIN: scaplan
EMAIL_ADDRESS: spencer_caplan@brown.edu


***** Questions for TA's: *********

For create Index:
- for title index, is it okay to just store <id, title string> on each line for each page?

- is it okay to completely parse/read in the entire collection and then create the index, rather than do it all at once?

- why do you say we should concatenate the title with the text?

queryIndex:
- It looks like the boolean parser is only meant for python 2.5 and python 2.6....and this is verified....does this mean you're always testing our projects using python 2.5 or 2.6?  Like I can make a point to test my code always with python 2.6, but how can I assure that the bash scripts also then always work?  ie, how can I assure that the default python to be used for our program is 2.6?

- can we assume BQ's well crafted where none of the words are stopwords?  Like can we assume we'll never encounter 'is AND forever'?



TODO: replace parser with more efficient method for reconstructing index


