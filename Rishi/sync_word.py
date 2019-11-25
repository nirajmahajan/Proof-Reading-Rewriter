import nltk

def sync_word(w1, w2):
	l1 = nltk.pos_tag(nltk.word_tokenize(w1))
	w = l1.pop(0)
	ans = w2
	if w[0][0].isupper():
		ans = w2.capitalize()
	else:
		ans = w2.lower()
	for i in l1:
		if i[1] != 'RB':
			ans = ans + i[0]
	return ans