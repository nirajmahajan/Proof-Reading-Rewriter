from Rishi.act_pas_2 import *

does = ['do', 'did', 'does']
wh_q = ['when', 'where', 'how', 'why']
obQ = ['what', 'which', 'xyz']
def pas_other(s):
	l = nltk.word_tokenize(s)
	tag = nltk.pos_tag(l)
	if tag[0][1] in verbs or tag[0][0].lower() in does:
		word = l.pop(0).lower()
		i = 1
		while tag[i][1] not in noun:
			#print(i)
			i = i + 1
		l.insert(i,word)
		[v,obj,sub,extra] = act_pas_helper(TreebankWordDetokenizer().detokenize(l))
		vL = v.split()
		first = vL.pop(0)
		str1 = " "
		rs = first + " " + obj + str1.join(vL) + " by " + sub + extra
		return rs
	if tag[0][0].lower() in aux_single or tag[0][0].lower() in aux_plural or tag[0][0].lower() in haves or tag[0][1] == 'MD':
		word = l.pop(0).lower()
		i = 1
		while tag[i][1] not in noun:
			#print(i)
			i = i + 1
		l.insert(i,word)
		rs = TreebankWordDetokenizer().detokenize(l)
		#print(rs)
		#print(rs)
		rs = act_pas(rs)
		#print(rs)
		rl = nltk.word_tokenize(rs)
		rl.remove(word)
		rs = word + " " + TreebankWordDetokenizer().detokenize(rl)
		return rs
	if tag[0][0].lower() in wh_q:
		word = l.pop(0).lower()
		rs = TreebankWordDetokenizer().detokenize(l)
		rs = pas_other(rs)
		rs = word + " " + rs
		return rs
	if tag[0][0].lower() in obQ:
		if tag[0][0].lower() == 'what':
			tp = l.pop(0)
			index = 2
			while tag[index][1] not in verbs:
				index = index + 1
			l.insert(index, 'shit')
			rs = TreebankWordDetokenizer().detokenize(l)
			#print(rs)
			rs = pas_other(rs)
			#print(rs)
			rl = rs.split()
			rl.remove('shit')
			rs = 'What ' + " ".join(rl)
			return rs
		if tag[0][0].lower() == 'xyz':
			tp = l.pop(0)
			index = 2
			while tag[index][1] not in verbs:
				index = index + 1
			l.insert(index, 'rivers')
			rs = TreebankWordDetokenizer().detokenize(l)
			#print(rs)
			rs = pas_other(rs)
			#print(rs)
			rl = rs.split()
			rl.remove('rivers')
			rs = 'What ' + " ".join(rl)
			return rs
		if tag[0][0].lower() == 'which':
			first = l.pop(0)
			index = 1
			while tag[index][1] not in noun:
				#print(tag[index][0],tag[index][1])
				index = index + 1
				first = first + " " + l.pop(0)
			main_noun = l.pop(0)
			main_tag = tag[index][1]
			if main_tag in plural:
				rs = 'xyz ' + TreebankWordDetokenizer().detokenize(l)
			else:
				rs = 'what ' + TreebankWordDetokenizer().detokenize(l)
			first = first + " " + main_noun
			rs = pas_other(rs)
			#print(rs)
			rl = rs.split()
			tp = rl.pop(0)
			rs = first + " " + " ".join(rl)
			return rs
	return act_pas(s)

def active_to_passive(s):
	rs = pas_other(s)
	rl = nltk.word_tokenize(rs)
	rl[0] = rl[0].capitalize()
	rs = TreebankWordDetokenizer().detokenize(rl)
	index = -1
	for i in rl:
		index = index + 1
		if i == 'i':
			rl[index] = 'I'

	return rs

