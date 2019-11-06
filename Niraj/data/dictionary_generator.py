# Generates dictionary from the db.txt located in data
import re
import pickle
from collections import Counter

WORDS = {}

with open('db.txt','r') as f:
    for line in f:
        if line.strip() in WORDS:
        	WORDS[line.strip()] += 1
        else: 
        	WORDS[line.strip()] = 1

with open('db.pickle', 'wb') as handle:
	pickle.dump(set(WORDS.keys()), handle)
