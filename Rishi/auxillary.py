import nltk
from nltk.corpus import stopwords

sT = set(stopwords.words('english'))

verbs = ['VB', 'VBP', 'VBZ', 'VBG', 'VBD']
def aux_replace(s):
	l = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	index = -1
	for i in tag:
		index = index + 1
		if i[1] in verbs and i[0].lower() in sT:
			l[index] = '?'
		elif i[0] == '?':
			l.pop(index)
			index = index - 1
	rs = " ".join(l)
	return rs