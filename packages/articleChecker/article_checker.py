import nltk
import os
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pickle

# Written by Rishi Agarwal, Department of Computer Science, IIT Bombay.

pathDB = os.path.abspath('databases/rishi-databases/article.pickle')
with open(pathDB, 'rb') as handle:
    WORDS_DB = pickle.load(handle)
pro_det = ['WP','WDT','WP$']
a_an = ['a','an','A','An']
nouns = ['NN','NNS']
the_cases = ['RBS','JJS','NNS']
h_cases = ['hour', 'honest', 'honesty', 'honour', 'honoured']
def art_check(l):
	# l = nltk.word_tokenize(s)
	pos = nltk.pos_tag(l)
	index = 0
	vowels = ['a','e','i','o','u','A','E','I','O','U']
	for i in pos:
		index = index+1
		if i[1]=='DT':
			try:
				if (pos[index][0][0] in vowels and pos[index][0].lower() not in WORDS_DB) or pos[index][0].lower() in h_cases:
					if(i[0]=='a'):
						l[index-1] = 'an'
					elif(i[0]=='A'):
						l[index-1] = 'An'
				else:
					if(i[0]=='an'):
						l[index-1] = 'a'
					elif(i[0]=='An'):
						l[index-1] = 'A'
				if pos[index][1] in the_cases and i[0] in a_an:
					if i[0].isupper():
						l[index-1] = 'The'
					else:
						l[index-1] = 'the'
			except:
				continue
	count_det = 0
	index = 0
	for i in pos:
		if i[1]=='DT':
			count_det = count_det + 1
			last = index
		elif i[1] in nouns:
			try:
				if pos[index+1][1] in pro_det or i[1] in the_cases:
					if pos[last][0] in a_an:
						if pos[last][0].isupper():
							l[last] = 'The'
							continue
						else:
							l[last]='the'
							continue
			except:
				pass
			if count_det > 1:
				try:
					if pos[last][0] in a_an:
						if pos[index-1][0].isupper():
							l[last] = 'The'
						else:
							l[last]='the'
				except:
					count_det = 0
					continue
			count_det = 0
		index = index + 1 

	return l