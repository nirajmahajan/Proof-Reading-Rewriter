import os
import urllib
import requests
import re
from noun_id import *
	
def APIexecute(query, i):
	encoded_query = urllib.parse.quote(query)
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

	response = requests.get('https://api.phrasefinder.io/search?' + params)

	assert response.status_code == 200

	out = response.json()
	ans = []
	for elem in out['phrases']:
		mc = elem["mc"]
		ans.append([mc, elem["tks"][i]['tt']])
	return ans

def APIsuggest(inl, targ):
	left = max(0, targ-1)
	right = min(targ+1, len(inl)-1)
	if(left == targ):
		if(targ+2 < len(inl)):
			string =  "? " + inl[targ+1] + " " + inl[targ+2]
			return sorted(APIexecute(string, 0), reverse=True)
		elif(targ+1 < len(inl)):
			string = "? " + inl[targ+1]
			return sorted(APIexecute(string, 0), reverse=True)
		else:
			return [(0, inl[targ],)]
	elif(right == targ):
		if(targ-2 >= 0):
			string = inl[targ-2] + " " + inl[targ-1] + " ?"
			return sorted(APIexecute(string, 2), reverse=True)
		elif(targ-1 >= 0):
			string = inl[targ-1] + " ?"
			return sorted(APIexecute(string, 1), reverse=True)
		else:
			return [(0, inl[targ],)]
	else:
		string = inl[targ-1] + " ? " + inl[targ+1]
		return sorted(APIexecute(string, 1), reverse = True)


# Inputs a list of strings
# Outputs a list of list of strings
# Each sublist will have probable suggestions. (Single sized lists if no spelling error)
# The only punctuations allowed are apostrophes and hifens
# . , ! ? ... should be independent new elements
# It is assumed that the input list is free of all other irrelevant punctuations

# takes a list of strings and return a list of list of suggestions
def trigramCheckSingleSentence(input):
	# using api
	nounIndices = set([i for i,word in enumerate(input) if word.startswith('#')])
	for it in nounIndices:
		input[it] = input[it][1:]

	articles = ['a', 'an', 'the']
	ans = []
	for it, word in enumerate(input):
		# print(ans)
		if(not re.search(r'^[^a-zA-Z]$', word) == None):
			ans.append([word])
			continue
		elif(it+1 in nounIndices):
			suggests = APIsuggest(input, it)
			if(suggests[0][1] == word):
				ans.append([word])
			else:
				ans.append([x[1] for x in suggests] + [word])

			input.insert(it+1, '?')	
			suggests = APIsuggest(input, it+1)
			# print(suggests[0][1])
			if(suggests[0][1].lower() in articles):
				ans.append([suggests[0][1]])
			input.pop(it+1)
		elif(not it in nounIndices):
			suggests = APIsuggest(input, it)
			if(suggests[0][1] == word):
				ans.append([word])
			else:
				ans.append([x[1] for x in suggests] + [word])
		else:
			ans.append([word])

	return ans