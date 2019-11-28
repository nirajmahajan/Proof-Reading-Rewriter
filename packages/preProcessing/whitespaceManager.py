import re

# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.
# Terms used
# Left : Punctuations that cannot have a space on the left but need a space on the right
# Right : Punctuations that cannot have a space on the right but need a space on the left


def isFullLeft(in_stringa):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	in_string = 'HASH!$$' + in_stringa + 'HASH!$$'
	rex = re.compile(r'HASH!\$\$[)\]}.,!?]+HASH!\$\$')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def isFullTerminator(in_stringa):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	in_string = 'HASH!$$' + in_stringa + 'HASH!$$'
	rex = re.compile(r'HASH!\$\$[.,!?]+HASH!\$\$')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def beginsWithLeft(in_stringa):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	in_string = 'HASH!$$' + in_stringa
	rex = re.compile(r'HASH!\$\$[)\]}.,!?]+')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def hasLeft(in_string):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	rex = re.compile(r'[)\]}.,!?]+')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def isFullRight(in_stringa):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	in_string = 'HASH!$$' + in_stringa + 'HASH!$$'
	rex = re.compile(r'HASH!\$\$[(\[{]+HASH!\$\$')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def endsWithRight(in_stringa):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	in_string =  in_stringa + 'HASH!$$'
	rex = re.compile(r'[(\[{]+HASH!\$\$')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def hasRight(in_string):
	# rex = re.compile(r'^[!\"#$%\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$')
	rex = re.compile(r'[(\[{]+')
	found = rex.search(in_string) != None
	if(found):
		return True
	else:
		return False

def preProcess(a1):
	a = re.sub('\.\.\.', '$$$ELL$$$', a1)
	a = re.sub('[\.]+', '.', a)
	a = re.sub('[!]+', '!', a)
	a = re.sub('[,]+', ',', a)
	a = re.sub('[?]+', '?', a)
	return a

def postProcess(a):
	a = re.sub('\$\$\$ELL\$\$\$', '...', a)
	return a

# Inputs a list of strings and removes extra white spaces around punctuations 
def spaceTrimmer(in_lista):
	in_list = in_lista.copy()
	out_list = []

	for i in range(len(in_list)):
		in_list[i] = preProcess(in_list[i])
		if(isFullLeft(in_list[i])):
			if(i == 0):
				continue
			else:
				out_list[len(out_list)-1] += in_list[i]
		elif (beginsWithLeft(in_list[i])):
			if(not i == 0):
				out_list[len(out_list)-1] += in_list[i][0]
			inserted = ""
			l_append = []
			for j in range(len(in_list[i])):
				if(not isFullTerminator(in_list[i][j])):
					inserted += in_list[i][j]
				elif(inserted != ""):
					l_append.append(inserted + in_list[i][j])
					inserted = ""
			if (inserted != ""):
				l_append.append(inserted)
			out_list += l_append
		elif(hasLeft(in_list[i])):
			inserted = ""
			l_append = []
			for j in range(len(in_list[i])):
				if(not isFullTerminator(in_list[i][j])):
					inserted += in_list[i][j]
				elif(inserted != ""):
					l_append.append(inserted + in_list[i][j])
					inserted = ""
			if (inserted != ""):
				l_append.append(inserted)
			out_list += l_append
		else:
			out_list.append(in_list[i])

	ans = []
	for i in range(len(out_list)):
		if(isFullRight(out_list[i])):
			if(i == len(out_list)-1):
				continue
			else:
				out_list[i+1] += out_list[i]
		elif(hasRight(out_list[i])):
			free = False # free to break
			inserted = ""
			l_append = []
			for j in range(len(out_list[i])):
				if(not isFullRight(out_list[i][j])):
					free = True;
					inserted += out_list[i][j]
				elif(free):
					free = False
					l_append.append(inserted)
					inserted = out_list[i][j]
				else:
					inserted += out_list[i][j]
			if(not inserted == "") :
				l_append.append(inserted)
			if(not endsWithRight(out_list[i])):
				ans += l_append
			else:
				if(i == len(out_list)-1):
					ans += l_append[0:-1]
				else:
					ans += l_append[0:-1]
					out_list[i+1] = l_append[-1] + out_list[i+1]
		else:
			ans.append(out_list[i])

	ans = [postProcess(a) for a in ans]
	return ans

	