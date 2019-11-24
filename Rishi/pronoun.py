import nltk
from nltk.corpus import stopwords

sT = set(stopwords.words('english'))

pronoun = ['this', 'that', 'these', 'those']
def demon_replace(s):
	l = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	index = -1
	for i in tag:
		index = index + 1
		if i[0].lower() in pronoun:
			l[index] = '?'
		elif i[0] == '?':
			l.pop(index)
			index = index - 1
	rs = " ".join(l)
	return rs