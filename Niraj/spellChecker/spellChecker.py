import pickle
import sqlite3
from helpers import *
# Inputs a list of strings 
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# It is assumed that the input list is free of all other irrelevant punctuations

conn = sqlite3.connect('../data/dumps/Trigram-Bigram-Dictionary.db')
c = conn.cursor()

# unordered set of all dictionary words
# Extends an online db(check referneces) with the nltk words database
with open('../data/dumps/db.pickle', 'rb') as handle:
    WORDS = pickle.load(handle)

with open('../data/dumps/freq.pickle', 'rb') as handle:
    FREQ = pickle.load(handle)

# Helper function to acces the Words table in the database
def inDictionary(w):
	# print(w)
	# c.execute('''SELECT id FROM Words WHERE word = ? LIMIT 1''', [w])
	# data1 = c.fetchall()

	# if(len(data1) == 0):
	# 	return False
	# else:
	# 	return True
	return w in WORDS

# Helper Function to access the Frequencies Table in the Database
def getFrequency(w):
	# print(w)
	# c.execute('''SELECT freq FROM Frequencies WHERE word = ? LIMIT 1''', [w])
	# data1 = c.fetchall()

	# if(len(data1) == 0):
	# 	return 0
	# else:
	# 	return data1[0][0]
	return FREQ.get(w, 0)

def processWord(stri, limit, only_wrong):

	def sorter(a):
		if(distance(a, stri) == 1):
			return getFrequency(a) + 7000
		else:
			return getFrequency(a) - 150 

	if(only_wrong):
		# if(stri.capitalize() in WORDS_DB and stri.lower() in WORDS_DB):
		# 	return [stri.lower()] + [stri.capitalize()]
		if(inDictionary(stri)):
			return [stri]
		elif(inDictionary(stri.capitalize())):
			return [stri.capitalize()]
		elif(inDictionary(stri.lower())):
			return [stri.lower()]
		elif(inDictionary(stri.upper())):
			return [stri.upper()]

	ans = (([a for a in one_away(stri) if (inDictionary(a))] + [a for a in two_away(stri) if (inDictionary(a))]).sort(key = sorter))
	ans = [a for a in one_away(stri) if (inDictionary(a))] + [a for a in two_away(stri) if (inDictionary(a))]
	ans.sort(key=sorter, reverse=True)

	# # now give priority to those ending with the same letter
	# ret = [a for a in ans if a.endswith(stri[len(stri)-1])]
	# ret2 = [a for a in ans if not a.endswith(stri[len(stri)-1])]
	# ans = ret + ret2
	
	# now give priority to those starting with the same letter
	ret = [a for a in ans if a.startswith(stri[0])]
	ret2 = [a for a in ans if not a.startswith(stri[0])]
	ans = ret + ret2

	# if length less than or equal to three, then give max priority to orignal spelling if exists
	if(len(stri) <= 3):
		if(stri in ans):
			ans.remove(stri)
			ans = [stri] + ans

	return ans[:min(limit,len(ans))]

def spellCheck(in_list, limit = 6, only_wrong = True):
	return [processWord(a, limit, only_wrong) for a in in_list]
	