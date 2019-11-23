import nltk
import pickle
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem.wordnet import WordNetLemmatizer

nouns = {'he':'him','she':'her','i':'me','they':'them', 'we':'us'}
inv_nouns = {'him':'he','her':'she','me':'i','them':'they', 'us':'we'}
noun = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']
plural = ['NNS','NNPS']

with open('participles.pickle', 'rb') as handle:
    participles = pickle.load(handle)
def act_pas(sen):
	l = nltk.word_tokenize(sen)
	tag = nltk.pos_tag(l)
	sub = ''
	obj = ''
	v = ''
	extra = ''
	index = 0
	foundS = False
	foundV = False
	foundO = False
	objN = ''
	objT = ''
	count = ''
	isI = 'ni'
	for i in tag:
		if i[1] not in noun and not foundS:
			sub = sub + i[0].lower() + " "
		elif not foundS:
			subN = i[0].lower()
			if i[0].lower() not in nouns.keys():
				sub = sub + i[0].lower() + " "
			else:
				sub = sub + nouns[i[0].lower()] + " "
			foundS = True
		elif not foundV:
			if i[1] == 'DT':
				foundV = True
				obj = obj + i[0] + " "
			elif i[1] in noun:
				foundV = True
				foundO = True
				if i[0] not in inv_nouns.keys():
					obj = obj + i[0] + " "
					objN = i[0]
				else:
					obj = obj + inv_nouns[i[0]] + " "
					objN = inv_nouns[i[0]]
				objT = i[1]
			else:
				v = v + i[0] + " "
		elif not foundO:
			if i[1] not in noun:
				obj = obj + i[0] + " "
			else:
				if i[0] not in inv_nouns.keys():
					obj = obj + i[0] + " "
					objN = i[0]
				else:
					obj = obj + inv_nouns[i[0]] + " "
					objN = inv_nouns[i[0]]
				foundO = True
				objT = i[1]
		else:
			extra = extra + i[0] + " "
	if objT in plural:
		count = 'plural'
	else:
		count = 'single'
	if objN == 'i':
		print(objN)
		isI = 'i'
	newS = obj + analyse(v,count,isI) + "by " + sub + extra
	return newS

def analyse(s,c,isI):
	l = nltk.word_tokenize(s)
	l1 = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	haves = ['has', 'had' ,'have']
	aux_plural = ['were', 'are']
	aux_single = ['was', 'is', 'am']
	present = ['VB', 'VBP', 'VBZ']
	pcont = ['VBG']
	past = ['VBD']
	aux = False
	index = -1
	if c == 'single':
		for i in l1:
			index = index + 1
			if i in haves:
				if i in ['have']:
					l[index] = 'has'
				l.insert(index + 1, 'been')
				aux = True
			elif i in aux_plural:
				aux = True
				if i == 'were':
					l[index] = 'was'
				else:
					if isI == 'ni':
						l[index] = 'is'
					else:
						l[index] = 'am'
			elif i in aux_single:
				if isI == 'i' and l[index] == 'is':
					l[index] = 'am'
				elif isI == 'ni' and l[index] == 'am':
					l[index] = 'is'
				aux = True
			elif tag[index][1] == 'MD':
				try:
					if l[index + 1] not in haves:
						l.insert(index + 1, 'be')
					aux = True
				except:
					print("Not possible")
			elif not aux:
				if tag[index][1] in present:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					if isI == 'i':
						l.insert(index, 'am')
					else:
						l.insert(index, 'is')
				else:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'was')
			elif aux:
				if tag[index][1] in pcont:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'being')
	else:
		for i in l1:
			index = index + 1
			if i in haves:
				if i in ['has']:
					l[index] = 'have'
				l.insert(index + 1, 'been')
				aux = True
			elif i in aux_single:
				aux = True
				if i == 'was':
					l[index] = 'were'
				else:
					l[index] = 'are'
			elif i in aux_plural:
				aux = True
			elif tag[index][1] == 'MD':
				try:
					if l[index + 1] not in haves:
						l.insert(index + 1, 'be')
					aux = True
				except:
					print("Not possible")
			elif not aux:
				if tag[index][1] in present:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'are')
				else:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'were')
			elif aux:
				if tag[index][1] in pcont:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'being')

	rs = TreebankWordDetokenizer().detokenize(l) + " "
	return (rs)