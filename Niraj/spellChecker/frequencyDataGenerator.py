# Generates frequency data from the big.txt located in data
# credits : https://norvig.com/spell-correct.html
import re
import pickle
from collections import Counter

def words(text):
	return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('../data/big.txt').read()))
N=sum(WORDS.values())

with open('freq.pickle', 'wb') as handle:
	pickle.dump(WORDS, handle)
