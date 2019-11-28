# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.

# creates raw text from the gutenberg list of novels
# just throws out the text to stdio, so do pipeline to a file
import nltk
from nltk.corpus import gutenberg

for fileid in gutenberg.fileids():
	emma = gutenberg.words(fileid)

	out = []
	for iter in range(0,len(emma)):
		x = emma[iter]
		if(len(out) == 0):
			last_added = ""
		else:
			last_added = out[len(out)-1]	
		if(last_added.endswith('\'') or last_added.endswith('-')):
			out[len(out)-1] += x
		elif(x == '\'' or x == '-'):
			out[len(out)-1] += x
		else:
			out.append(x)

	[print(a, end=" ") for a in out]