import nltk
import pickle
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem.wordnet import WordNetLemmatizer

nouns = {'he':'him','she':'her','i':'me','they':'them', 'we':'us', 'who':'whom'}
inv_nouns = {'him':'he','her':'she','me':'i','them':'they', 'us':'we', 'whom':'who'}
noun = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']
plural = ['NNS','NNPS']
det = ['DT', 'PDT', 'PRP$', 'POS']
haves = ['has', 'had' ,'have']
aux_plural = ['were', 'are']
aux_single = ['was', 'is', 'am']
present = ['VB', 'VBP', 'VBZ']
pcont = ['VBG']
past = ['VBD']
verbs = ['VB', 'VBP', 'VBZ', 'VBG', 'VBD']
does = ['do', 'did', 'does']
proper = ['NNP', 'NNPS']

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
	vL = []
	vTL = []
	for i in tag:
		if i[1] not in noun and i[0].lower()!='who' and not foundS:
			sub = sub + i[0].lower() + " "
		elif not foundS:
			subN = i[0].lower()
			if i[0].lower() not in nouns.keys() and i[1] not in proper:
				sub = sub + i[0] + " "
			elif i[0].lower() not in nouns.keys():
				sub = sub + i[0].lower() + " "
			else:
				sub = sub + nouns[i[0].lower()] + " "
			foundS = True
		elif not foundV:
			if i[1] in det:
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
				vL.append(i[0])
				vTL.append(i)
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
	if objT in plural or objN.lower() == 'you':
		count = 'plural'
	else:
		count = 'single'
	if objN == 'i':
		isI = 'i'
	newS = obj + analyse(vL,vTL,count,isI) + "by " + sub + extra
	return newS

def analyse(vL,vTL,c,isI):
	l = vL.copy()
	l1 = vL.copy()
	tag = vTL.copy()
	aux = False
	being_ = False
	index = -1
	sind = -1
	if c == 'single':
		for i in l1:
			index = index + 1
			sind = sind + 1
			if not aux and i in does:
				if i in ['do', 'does']:
					l[index] = 'is'
				else:
					l[index] = 'was'
				aux = True
			elif i in haves:
				if i in ['have']:
					l[index] = 'has'
				l.insert(index + 1, 'been')
				index = index + 1
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
			elif tag[sind][1] == 'MD':
				try:
					if l[index + 1] not in haves:
						if l[index + 1] != 'to':
							l.insert(index + 1, 'be')
							index = index + 1
						else:
							l.insert(index + 2, 'be')
							index = index + 1
					aux = True
				except:
					print("Not possible")
			elif not aux:
				aux = True
				if tag[sind][1] in present:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					if isI == 'i':
						l.insert(index, 'am')
					else:
						l.insert(index, 'is')
					index = index + 1
				else:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'was')
			elif aux:
				try:
					if tag[sind][0] == 'going' and tag[sind + 1][0] == 'to' and tag[sind + 2][1] in verbs:
						l.insert(index + 2, 'be')
						index = index + 1
						continue
				except:
					pass
				if tag[sind][1] in pcont:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed' 
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					if not being_:
						l.insert(index, 'being')
						index = index + 1
						being_ = True
				elif tag[sind][1] in verbs:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed' 
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]

	else:
		for i in l1:
			sind = sind + 1
			index = index + 1
			if not aux and i in does:
				if i in ['do', 'does']:
					l[index] = 'are'
				else:
					l[index] = 'were'
				aux = True
			elif i in haves:
				if i in ['has']:
					l[index] = 'have'
				l.insert(index + 1, 'been')
				index = index + 1
				aux = True
			elif i in aux_single:
				aux = True
				if i == 'was':
					l[index] = 'were'
				else:
					l[index] = 'are'
			elif i in aux_plural:
				aux = True
			elif tag[sind][1] == 'MD':
				try:
					if l[index + 1] not in haves:
						l.insert(index + 1, 'be')
						index = index + 1
					aux = True
				except:
					print("Not possible")
			elif not aux:
				aux = True
				if tag[sind][1] in present:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'are')
					index = index + 1
				else:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					l.insert(index, 'were')
					index = index + 1
			elif aux:
				try:
					if tag[sind][0] == 'going' and tag[sind + 1][0] == 'to' and tag[sind + 2][1] in verbs:
						l.insert(index + 2, 'be')
						index = index + 1
						continue
				except:
					pass
				if tag[sind][1] in pcont:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]
					if not being_:
						l.insert(index, 'being')
						index = index + 1
						being_ = True
				elif tag[sind][1] in verbs:
					if WordNetLemmatizer().lemmatize(l[index],'v') not in participles.keys():
						if WordNetLemmatizer().lemmatize(l[index],'v').endswith('e'):
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'd'
						else:
							l[index] = WordNetLemmatizer().lemmatize(l[index],'v') + 'ed'
					else:
						l[index] = participles[WordNetLemmatizer().lemmatize(l[index],'v')]

	rs = TreebankWordDetokenizer().detokenize(l) + " "
	return (rs)

def act_pas_helper(sen):
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
	vL = []
	vTL = []
	for i in tag:
		if i[1] not in noun and i[0].lower()!='who' and not foundS:
			sub = sub + i[0].lower() + " "
		elif not foundS:
			subN = i[0].lower()
			if i[0].lower() not in nouns.keys():
				sub = sub + i[0].lower() + " "
			else:
				sub = sub + nouns[i[0].lower()] + " "
			foundS = True
		elif not foundV:
			if i[1] in det:
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
				vL.append(i[0])
				vTL.append(i)
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
	if objT in plural or objN.lower() == 'you':
		count = 'plural'
	else:
		count = 'single'
	if objN == 'i':
		print(objN)
		isI = 'i'
	newS = obj + analyse(vL,vTL,count,isI) + "by " + sub + extra
	return [analyse(vL,vTL,count,isI), obj, sub, extra]