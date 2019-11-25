# Main File!
# Inputs a single sentence and returns possible suggestions
# First applies the spell checker on the data
# Proceeds to grammar check only if the spell checker has no grievances
# The third aspect of this code has a rewriter and a voice changer
# The code will execute this rewriter, with the assumption that all spelling
#	 and grammatical errors have been cleared
import nltk
import re
from Niraj.spellChecker.spellChecker import *
from Niraj.preProcessing.caseCorrector import *
from Niraj.trigramChecker.trigramChecker import *
from Rishi.article_checker import *
from Rishi.act_pas_3 import active_to_passive

# conn = sqlite3.connect('Niraj/data/dumps/Trigram-Bigram-Dictionary.db')
# c = conn.cursor()

# Merges punctuations with the previous word
# INPUT : list of lists
# OUTPUT : list of lists
def prepare(lst):
	ans = []
	for elem in lst:
		if(len(elem) != 1):
			ans.append(elem)
			continue

		if (not re.match(r'^[^a-zA-Z]$', elem[0]) == None):
			# purely symmbolic
			if(len(ans) == 0):
				ans.append(elem)
			else:
				for i in range(0, len(ans[len(ans)-1])):
					ans[len(ans)-1][i] = ans[len(ans)-1][i] + elem[0]
		else:
			ans.append(elem)
	return ans

# Driver Function to run the code
# Three modes are possible
# 	1) grammar
# 	2) rewriter
# 	3) voice
# INPUT : sentence (string) and a mode(string)
# OUTPUT : list of words and a comment
def processSentence(sentence, mode):
	if mode == 'grammar':
		word_list = caseCorrector(nltk.word_tokenize(sentence))
		ans = spellCheck(word_list)
		spellAllCorrect = True
		to_art = []
		for elem in ans:
			to_art.append(elem[0])
			if(len(elem) > 1):
				spellAllCorrect = False

		if(not spellAllCorrect):
			return (prepare(ans), 'spell')
		# if reached here, then the spellings are all correct

		# run article checker
		art_ans = art_check(to_art)
		# now art_ans is a list of strings which are corrected wrt articles (tentatively)

		# run trigram matcher
		trigram_ans = trigramCheck(art_ans);
		return (prepare(trigram_ans), 'grammar')
		# grammarAllCorrect = True
		# to_rewriter = []
		# for elem in trigram_ans:
		# 	to_rewriter.append(elem[0])
		# 	if(len(elem) > 1):
		# 		grammarAllCorrect = False

		# if(not grammarAllCorrect):
		# 	return (trigram_ans, 'grammar')
	elif mode == 'rewriter':
		return ("Use rewriter here".split(), 'rewriter')
	elif mode == 'voice':
		return (active_to_passive(sentence), 'voice')
	return(('Dunno rewriting functions'.split(), 'voice'))

# conn.close()
# c.close()