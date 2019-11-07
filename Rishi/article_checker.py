import nltk

def art_check(s):
	l = nltk.word_tokenize(s)
	pos = nltk.pos_tag(l)
	for i in pos:
		if i[1]=='DT':
			print("Yes")
	print(pos)
	pass