import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pickle

with open('db.pickle', 'rb') as handle:
    WORDS_DB = pickle.load(handle)

def art_check(s):
	l = nltk.word_tokenize(s)
	pos = nltk.pos_tag(l)
	index = 0
	vowels = ['a','e','i','o','u','A','E','I','O','U']
	for i in pos:
		index = index+1
		if i[1]=='DT':
			try:
				if pos[index][0][0] in vowels and pos[index][0].lower() not in WORDS_DB:
					if(i[0]=='a'):
						l[index-1] = 'an'
					elif(i[0]=='A'):
						l[index-1] = 'An'
				else:
					if(i[0]=='an'):
						l[index-1] = 'a'
					elif(i[0]=='An'):
						l[index-1] = 'A'
				if pos[index][1] in ['RBS','JJS']:
					if i[0].isupper():
						l[index-1] = 'The'
					else:
						l[index-1] = 'the'
			except:
				continue
	print(pos)
	rs = TreebankWordDetokenizer().detokenize(l)
	return (rs)
	pass