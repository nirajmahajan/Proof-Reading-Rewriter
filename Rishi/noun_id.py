import nltk
from nltk.corpus import stopwords

sT = set(stopwords.words('english'))
noun = ['NN', 'NNS', 'NNP', 'NNPS']
verbs = ['VB', 'VBP', 'VBZ', 'VBG', 'VBD']
def noun_identifier(s):
	l = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	index = -1
	for i in tag:
		index = index + 1
		if i[1] in noun:
			l[index] = '#' + l[index]
		elif i[0] == '?':
			l.pop(index)
			index = index - 1
	rs = " ".join(l)
	return rs