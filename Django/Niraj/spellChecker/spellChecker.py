import pickle
import sqlite3
import os
import re
from Niraj.spellChecker.helpers import *
# Inputs a list of strings 
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# It is assumed that the input list is free of all other irrelevant punctuations
conn = sqlite3.connect('/home/neelaryan2/Downloads/Proof-Reading-Rewriter/Django/Niraj/data/dumps/Trigram-Bigram-Dictionary.db', check_same_thread=False)
c = conn.cursor()

# Some helpers to access the sql database
def fetchTrigFreq(w1, w2, w3):
	c.execute('''SELECT freq FROM Trigrams WHERE first = ? AND second = ? AND third = ?''', [w1, w2, w3])
	data1 = c.fetchall()
	c.execute('''SELECT freq FROM Trigrams1 WHERE first = ? AND second = ? AND third = ?''', [w1, w2, w3])
	data2 = c.fetchall()
	if(len(data1) == 0 and len(data2) == 0):
		return 0
	elif(len(data1) == 0):
		return 4* data2[0][0]
	elif(len(data2) == 0):
		return data1[0][0]
	else:
		return data1[0][0] + 4*data2[0][0]

def fetchBigFreq(w1, w2):
	# print('call', flush=True)
	c.execute('''SELECT freq FROM Bigrams WHERE first = ? AND second = ?''', [w1, w2])
	data1 = c.fetchall()
	if(len(data1) == 0):
		return 0
	else:
		return data1[0][0]

# Calculates the score of a given target, with respect to it's neighbours
# lst is the list of strings while targ is a integer denoting the 
# position of the target string
def calculateScore(lst, targ):
	tscore = 0
	bscore = 0
	tcount = 0
	bcount = 0
	
	l2 = None
	l1 = None
	target = None
	r1 = None
	r2 = None
	if(targ-1 >= 0):
		l1 = lst[targ-1]
	if(targ-2 >= 0):
		l2 = lst[targ-2]
	target = lst[targ]
	if(targ+1 < len(lst)):
		r1 = lst[targ+1]
	if(targ+2 < len(lst)):
		r2 = lst[targ+2]
	

	if(l2 != None and l1 != None):
		tscore = tscore + 3*fetchTrigFreq(l2, l1, target)
		tcount = tcount + 1
	if(l1 != None and r1 != None):
		tscore = tscore + 4*fetchTrigFreq(l1, target, r1)
		tcount = tcount + 1
	if(r1 != None and r2 != None):
		tscore = tscore + 3*fetchTrigFreq(target, r1, r2)
		tcount = tcount + 1
	# if(not SQLON):
	if(True):
		if(r1 != None):
			bscore = bscore + fetchBigFreq(target, r1)
			bcount = bcount + 1
		if(l1 != None):
			bscore = bscore + fetchBigFreq(l1, target)
			bcount = bcount + 1

	if(not tcount == 0):
		tscore = tscore / tcount
	# if(not SQLON):
	if(True):
		if(not bcount == 0):
			bscore = bscore / bcount
		tscore = tscore + 0.3 * bscore
	return tscore

# unordered set of all dictionary words
# Extends an online db(check referneces) with the nltk words database
with open('/home/neelaryan2/Downloads/Proof-Reading-Rewriter/Django/Niraj/data/dumps/db.pickle', 'rb') as handle:
    WORDS = pickle.load(handle)

with open('/home/neelaryan2/Downloads/Proof-Reading-Rewriter/Django/Niraj/data/dumps/freq.pickle', 'rb') as handle:
    FREQ = pickle.load(handle)

# with open('../data/dumps/big.pickle', 'rb') as handle:
# 	Bigrams = pickle.load(handle)

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

	return ans

def spellCheck(in_list, limit = 5, only_wrong = True):

	iitbLingo = ['arbit','bandi','chamka','craxxxx','dac','dadda','ditch','dosa','enthu','farra','freshie','god','infi','insti','junta','liby','macha','matka','mug','paf']
	LingoMeans = ['arbitrary','girl','understand','achievement','Disciplinary Action Committee','Dual Degree Student','drop','Dean of Student Affairs','enthusiasm','FR','First Year Student','awesome','infinite','institute','people','library','rock','MTech Student','study','Performing Arts Festival']
	lingodic = {}
	for (lingo, meaning) in zip(iitbLingo, LingoMeans):
		lingodic[lingo] = meaning

	ans = []
	for elem in in_list:
		if(elem.lower() in lingodic):
			toadd = lingodic[elem]
			if elem[0].isupper():
				toadd = toadd.Capitalize()
			else:
				toadd = toadd.lower()
			ans.append([toadd])
		elif (re.match(r'^[^a-zA-Z]$', elem) == None):
			ans.append(processWord(elem, limit, only_wrong))
		else:
			ans.append([elem])

	for it, elem in enumerate(ans):
		def trigSorter(a):
			store = in_list[it]
			in_list[it] = a
			vla = calculateScore(in_list, it)
			in_list[it] = store
			return vla
		ans[it].sort(key = trigSorter, reverse=True)
		ans[it] = ans[it][0:min(limit,len(ans[it]))]
	# c.close()
	# conn.close()


	fa = []
	for elem in ans:
		seti = set()
		tempa = []
		for part in elem:
			if part in seti:
				continue
			else:
				seti.add(part)
				tempa.append(part)
		fa.append(tempa)
	return fa



	