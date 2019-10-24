import pickle
from helpers import *
# Inputs a list of strings 
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# It is assumed that the input list is free of all other irrelevant punctuations


# unordered set of all dictionary words
# Extends an online db(check referneces) with the nltk words database
with open('../data/db.pickle', 'rb') as handle:
    WORDS_DB = pickle.load(handle)

# dictionary of all common words with frequency
with open('../data/freq.pickle', 'rb') as handle:
    FREQ_TABLE = pickle.load(handle)


def processWord(stri, limit, only_wrong):

	def sorter(a):
		if(distance(a, stri) == 1):
			return FREQ_TABLE[a] + 150
		else:
			return FREQ_TABLE[a] - 150 

	if(only_wrong):
		if(stri.capitalize() in WORDS_DB and stri.lower() in WORDS_DB):
			return [stri.lower()] + [stri.capitalize()]
		elif(stri.capitalize() in WORDS_DB):
			return [stri.capitalize()]
		elif(stri.lower() in WORDS_DB):
			return [stri.lower()]
		elif(stri.upper() in WORDS_DB):
			return [stri.upper()]

	ans = (([a for a in one_away(stri) if (a in WORDS_DB)] + [a for a in two_away(stri) if (a in WORDS_DB)]).sort(key = sorter))
	ans = [a for a in one_away(stri) if (a in WORDS_DB)] + [a for a in two_away(stri) if (a in WORDS_DB)]
	ans.sort(key=sorter, reverse=True)
	return list(set(ans[:min(limit,len(ans))]))

def spellCheck(in_list, limit = 6, only_wrong = True):
	return [processWord(a, limit, only_wrong) for a in in_list]
	