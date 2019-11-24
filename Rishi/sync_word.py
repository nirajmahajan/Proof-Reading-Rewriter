import nltk

def sync_word(w1, w2):
	l1 = nltk.word_tokenize(w1)
	w = l1.pop(0)
	ans = w2
	if w[0].isupper():
		ans = w2.capitalize()
	for i in l1:
		ans = ans + i
	return ans