import sqlite3
import pickle
import os
import urllib
import requests

USEAPI = True
SQLON = False

if (not USEAPI)
	# Establish connection to the sql database
	try:
		conn = sqlite3.connect('../data/dumps/Trigram-Bigram-Dictionary.db')
		c = conn.cursor()
	except Exception as e:
		raise e
		os._exit(1)

	if(not SQLON):
		with open('../data/dumps/trig.pickle', 'rb') as handle:
		    TRIG = pickle.load(handle)

		with open('../data/dumps/big.pickle', 'rb') as handle:
		    BIG = pickle.load(handle)

# Some helpers to access the sql database
def fetchTrigFreq(w1, w2, w3):
	print('call', flush=True)
	if(SQLON):
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
			return data1[0][0] + 4* data2[0][0]
	else:
		key1 = w1 + '$' + w2 + '$' + w3
		return TRIG.get(key1, 0)

def fetchBigFreq(w1, w2):
	print('call', flush=True)
	if(SQLON):
		c.execute('''SELECT freq FROM Bigrams WHERE first = ? AND second = ?''', [w1, w2])
		data1 = c.fetchall()
		if(len(data1) == 0):
			return 0
		else:
			return data1[0][0]
	else:
		key1 = w1 + '$' + w2
		return BIG.get(key1, 0)

def fetchABx(w1, w2):
	c.execute('''SELECT third FROM Trigrams WHERE first = ? AND second = ?''', [w1, w2])
	data1 = c.fetchall()
	c.execute('''SELECT third FROM Trigrams1 WHERE first = ? AND second = ?''', [w1, w2])
	data2 = c.fetchall()
	return set(data1 + data2)

def fetchAxB(w1, w3):
	c.execute('''SELECT second FROM Trigrams WHERE first = ? AND third = ?''', [w1, w3])
	data1 = c.fetchall()
	c.execute('''SELECT second FROM Trigrams1 WHERE first = ? AND third = ?''', [w1, w3])
	data2 = c.fetchall()
	return set(data1 + data2)

def fetchxAB(w2, w3):
	c.execute('''SELECT first FROM Trigrams WHERE second = ? AND third = ?''', [w2, w3])
	data1 = c.fetchall()
	c.execute('''SELECT first FROM Trigrams1 WHERE second = ? AND third = ?''', [w2, w3])
	data2 = c.fetchall()
	return set(data1 + data2)

def fetchAx(w1):
	c.execute('''SELECT second FROM Bigrams WHERE first = ?''', [w1])
	data1 = c.fetchall()
	return set(data1)

def fetchxA(w2):
	c.execute('''SELECT first FROM Bigrams WHERE second = ?''', [w2])
	data1 = c.fetchall()
	return set(data1)


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

# returns a set of suggestions for words at a given index
def suggest(lst, targ):
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

	out = set()
	assigned = False
	if(l2 != None and l1 != None):
		if(not assigned):
			assigned = True
			out = fetchABx(l2, l1)
		else:
			out = out.intersection(fetchABx(l2, l1))
	if(l1 != None and r1 != None):
		if(not assigned):
			assigned = True
			out = fetchAxB(l1, r1)
		else:
			out = out.intersection(fetchAxB(l1, r1))
	if(r1 != None and r2 != None):
		if(not assigned):
			assigned = True
			out = fetchxAB(r1, r2)
		else:
			out = out.intersection(fetchxAB(r1, r2))
	# if(r1 != None):
	# 	if(not assigned):
	# 		assigned = True
	# 		out = fetchxA(r1)
	# 	else:
	# 		out = out.intersection(fetchxA(r1))
	# if(l1 != None):
	# 	if(not assigned):
	# 		assigned = True
	# 		out = fetchAx(l1)
	# 	else:
	# 		out = out.intersection(fetchAx(l1))

	# print(out)
	return set([x[0] for x in list(out)])
	
APIexecute(query, i):
	encoded_query = urllib.parse.quote('how did ?')
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

	response = requests.get('https://api.phrasefinder.io/search?' + params)

	assert response.status_code == 200

	out = response.json()
	i = 2
	ans = []
	for elem in out['phrases']:
		mc = elem["mc"]
		ans.append([elem["tks"][i]['tt'], mc])
	return ans

APIsuggest(inl, targ):



# Inputs a list of strings
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# . , ! ? ... should be independent new elements
# It is assumed that the input list is free of all other irrelevant punctuations

# takes a list of strings and return a list of list of suggestions
def trigramCheckSingleSentence(input):
	if(not USEAPI):
		THRESHOLD = 2000
		print(input)
		scoreList = []
		for (i, elem) in enumerate(input):
			scoreList.append(calculateScore(input, i))

		print(scoreList)
		THRESHOLD = min(THRESHOLD, max(scoreList)/2.2)
		print(THRESHOLD)
		ans = []
		it = -1
		for score, word in zip(scoreList, input):
			it = it + 1
			if(score > THRESHOLD):
				ans.append([word])
			else:
				def sortfunc(x):
					input[it] = x
					if(it == 0 and (x == ',' or x == '?')):
						return 0
					temp = calculateScore(input, it)
					input[it] = word
					if(temp < THRESHOLD):
						return 0
					else:
						return temp

				temp = sorted(list(suggest(input, it)), key = sortfunc, reverse = True)
				ans.append(temp[1:min(5, len(temp))])

		return ans
	else:
		# using api
		nounIndexes = set([i for i,word in enumerate(input) if word.startswith('#')])
		QueryIndexes = set([i for i,word in enumerate(input) if word == '?'])

		for it, word in enumerate(input):