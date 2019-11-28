import numpy as np

# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.
#  returns a list of all elements at a distance 1 from the word
def one_away(stri):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	splits = [(stri[:i], stri[i:])    for i in range(len(stri) + 1)]
	deletions = [left + right[1:] for left, right in splits if (not right == "")]
	insertions = [left + add + right for (left, right) in splits for add in alphabet]
	switches = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right)>1]
	substitutes = [left + sub + right[1:] for left, right in splits if right for sub in alphabet]
	
	ans = deletions + switches + insertions + substitutes
	return set([x.lower() for x in ans] + [x.capitalize() for x in ans] + [stri.capitalize()] + [stri.lower()] + [stri.upper()])

def two_away(stri):
	l = one_away(stri)
	twos = [y for x in l for y in one_away(x)]
	return set(twos)

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

