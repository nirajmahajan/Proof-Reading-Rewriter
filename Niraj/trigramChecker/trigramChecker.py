import os
import urllib
import requests
import numpy as np
import re
from Niraj.trigramChecker.noun_id import *
	
# returns the distance in two strings
# Distance calculated on the basis of Levenshtein Distance Algorithm 
# Has a linear runtime
def distance(a, b):
	dp = np.zeros((len(a)+1, len(b)+1), dtype=int)
	for i in range(len(a)+1):
		dp[i, 0] = i
	for i in range(len(b)+1):
		dp[0, i] = i
	
	for i in range(1, len(a)+1):
		for j in range(1, len(b)+1):
			if(a[i-1] == b[j-1]):
				dp[i, j] = dp[i-1, j-1]
			else:
				dp[i, j] = min(dp[i, j-1], dp[i-1, j], dp[i-1, j-1]) + 1

	return dp[len(a), len(b)]

def APIexecute(query, i):
	encoded_query = urllib.parse.quote(query)
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 5}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

	response = requests.get('https://api.phrasefinder.io/search?' + params)

	assert response.status_code == 200

	out = response.json()
	ans = []
	for elem in out['phrases']:
		mc = elem["mc"]
		ans.append([mc, elem["tks"][i]['tt']])
	dic = {}
	for i in range(0, len(ans)):
		dic[ans[i][1]] = dic.get(ans[i][1], 0) + ans[i][0]

	return zip(dic.values(), dic.keys())

def APIsuggest(inl, targ):
	def sorter(a):
		dist = distance(a[1], inl[targ])
		ans = a[0]
		if(dist == 0):
			ans = ans + 10000000	
		elif(dist == 1):
			ans = ans + 1000000
		elif(dist == 2):
			ans = ans + 5000
		return ans

	left = max(0, targ-1)
	right = min(targ+1, len(inl)-1)
	if(left == targ):
		if(targ+2 < len(inl)):
			string =  "? " + inl[targ+1] + " " + inl[targ+2]
			return sorted(APIexecute(string, 0), reverse=True, key = sorter)
		elif(targ+1 < len(inl)):
			string = "? " + inl[targ+1]
			return sorted(APIexecute(string, 0), reverse=True, key = sorter)
		else:
			return [(0, inl[targ],)]
	elif(right == targ):
		if(targ-2 >= 0):
			string = inl[targ-2] + " " + inl[targ-1] + " ?"
			return sorted(APIexecute(string, 2), reverse=True, key = sorter)
		elif(targ-1 >= 0):
			string = inl[targ-1] + " ?"
			return sorted(APIexecute(string, 1), reverse=True, key = sorter)
		else:
			return [(0, inl[targ],)]
	else:
		string = inl[targ-1] + " ? " + inl[targ+1]
		return sorted(APIexecute(string, 1), reverse=True, key = sorter)


# Inputs a list of strings
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# . , ! ? ... should be independent new elements
# It is assumed that the input list is free of all other irrelevant punctuations

# takes a list of strings and return a list of list of suggestions
def trigramCheck(input):
	# using api
	nounIndices = set([i for i,word in enumerate(input) if word.startswith('#')])
	for it in nounIndices:
		input[it] = input[it][1:]

	articles = ['a', 'an', 'the']
	art_join = False
	ans = []
	for it, word in enumerate(input):
		# print(ans)
		if(not re.search(r'^[^a-zA-Z]$', word) == None):
			ans.append([word])
			continue
		elif(it+1 in nounIndices):
			suggests = APIsuggest(input, it)
			if(suggests == []):
				ans.append([word])
			elif(suggests[0][1] == word):
				ans.append([word])
			else:
				ans.append([x[1] for x in suggests] + [word])

			input.insert(it+1, '?')	
			suggests = APIsuggest(input, it+1)
			# print(suggests[0][1])
			if(suggests == []):
				ans.append([word])
			elif(suggests[0][1].lower() in articles):
				ans.append(['#' + suggests[0][1]])
				art_join = True
			input.pop(it+1)
		elif(not it in nounIndices):
			suggests = APIsuggest(input, it)
			if(suggests == []):
				ans.append([word])
			elif(suggests[0][1] == word):
				ans.append([word])
			else:
				ans.append([x[1] for x in suggests] + [word])
		else:
			ans.append([word])

	check for additional articles
	fa = []
	for i,elem in enumerate(ans):
		if (len(elem) == 1 and elem[0].startswith('#')):
			for j in range(0, len(ans[i+1])):
				ans[i+1][j] = elem[0][1:] + ' ' + ans[i+1][j]
		else:
			fa.append(elem)

	return fa
	# return ans