from django.shortcuts import render
from functions.utils import *

global_sent_list = []
global_types = []
global_words = []
global_suggestions = []

# Create your views here.
def main_view(request, *args, **kwargs):
	global global_sent_list
	global global_words
	global global_types
	default = ["hello yes", "world", "how"]
	my_context = {}
	my_context["my_list"] = default
	my_context["words"] = []
	my_context["original"] = ""
	my_context["curr_word"] = "-1"
	text = ""
	recompute = 1
	curr_word = -1
	changed_sent = -1
	replaced = -1
	types = []
	if request.method == "POST":
		text = request.POST.get("text", None)
		recompute = int(request.POST.get("recompute", None))
		my_context["curr_word"] = request.POST.get("curr_word", None)
		replaced = int(request.POST.get("replaced", None))
		try:
			curr_word = int(my_context["curr_word"])
			
		except:
			pass
		changed_sent = int(request.POST.get("changed", None)) 
	my_context["original"] = text
	sent_list = split_into_sentences(text)	
	words = form_words(sent_list)

	if(recompute==0):
		print("neel1")
		chInd = getIndex(sent_list, curr_word)
		types = global_types
		for x in range(0, len(types)):
			my_context["words"] += [[words[x], types[x]]]
		my_context["my_list"] = default
		# my_context["my_list"] = global_suggestions[chInd[0]][chInd[1]]
		# load suggestions here, nothing else
		return render(request, "main.html", my_context)

	if(replaced!=-1):
		new_word = my_context["my_list"][replaced]
		chInd = replace_in_sent(sent_list, curr_word, new_word)
		words = form_words(sent_list)
		global_words = words
		print(curr_word)
		my_context["original"] = ""
		for i in sent_list:
			my_context["original"] += " " + i
		my_context["original"] = my_context["original"][1:]
		my_context["my_list"] = default
		# process here words and sent_list
		updateTypes(curr_word, new_word)
		curr_word = -1
		types = global_types
		for x in range(0, len(types)):
			my_context["words"] += [[words[x], types[x]]]
		return render(request, "main.html", my_context)
	
	update(sent_list, words, types)
	types = global_types
	# process here words and sent_list
	for x in range(0, len(types)):
		my_context["words"] += [[words[x], types[x]]]
	return render(request, "main.html", my_context)

def update(sent_list, words, types):
	global global_sent_list
	global global_words
	global global_suggestions
	global global_types
	global_sent_list = sent_list
	global_words = words
	# if global_types==[]:
	# 	global_types = [1 for x in words]
	global_types = [1 for x in words]
	if global_suggestions == []:
		global_suggestions = [[[] for x in y.split()] for y in sent_list]

def replace_in_sent(sent_list, curr_word, new_word):
	global global_sent_list
	ind = 0
	ind2 = 0
	y = []
	for x in sent_list:
		leng = len(x.split())
		if(curr_word>=leng):
			curr_word-=leng
			ind+=leng
			ind2+=1
			continue
		ind+=curr_word
		y = x.split()
		y[curr_word] = new_word
		break
	sent_list[ind2]=""
	for i in y:
		sent_list[ind2] += " " + i
	sent_list[ind2] = sent_list[ind2][1:]
	global_sent_list[ind2] = sent_list[ind2]
	return ind2

def getIndex(sent_list, curr_word):
	ind2 = 0
	for x in sent_list:
		leng = len(x.split())
		if(curr_word>=leng):
			curr_word-=leng
			ind2+=1
			continue
		break
	return [ind2, curr_word]

def updateTypes(curr_word, new_word):
	global global_types
	types = global_types
	global_types = types[:curr_word]
	old = types[curr_word]
	for x in range(0,len(new_word.split())):
		global_types += [old+1]
	global_types += types[curr_word+1:]
	return