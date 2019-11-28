import nltk

# Written by Rishi Agarwal, Department of Computer Science, IIT Bombay.

noun = ['NN', 'NNS', 'NNP', 'NNPS']
def noun_identifier(s):
	l = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	index = -1
	for i in tag:
		index = index + 1
		if i[1] in noun:
			# l.insert(index, '?')
			# index = index + 1
			l[index] = '#' + l[index]
		# elif i[0] == '?':
		# 	l.pop(index)
		# 	index = index - 1
	# rs = " ".join(l)
	# return rs
	return l 