from django.shortcuts import render
from functions.utils import *
from bisect import bisect_left

global_sent_list = []
global_types = []
global_words = []
global_suggestions = []


# Create your views here.
def main_view(request, *args, **kwargs):
    global global_sent_list
    global global_words
    global global_types
    global global_suggestions
    default = ["hello yes", "world", "how"]
    default = []
    my_context = {}
    my_context["my_list"] = default
    my_context["words"] = []
    my_context["original"] = ""
    my_context["curr_word"] = "-1"
    my_context["passive"] = 0
    my_context["passiveForm"] = ""
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

    if (recompute == 0):
        chInd = getIndex(sent_list, curr_word)
        my_context["words"] = context_words()
        # my_context["my_list"] = default
        my_context["my_list"] = global_suggestions[chInd[0]][chInd[1]]
        # return render(request, "main.html", my_context)

    elif (replaced != -1):
        if (curr_word == -1):
            my_context["my_list"] = default
        else:
        	chInd = getIndex(sent_list, curr_word)
        	my_context["my_list"] = global_suggestions[chInd[0]][chInd[1]]
        	new_word = my_context["my_list"][replaced]
        	chInd = replace_in_sent(sent_list, curr_word, new_word)
        	global_words = form_words(sent_list)
        	my_context["original"] = " ".join(sent_list)
        	my_context["my_list"] = default
        	mode = updateTypes(chInd, new_word)
        	[global_suggestions[chInd[0]], mode] = getSuggestions(global_sent_list[chInd[0]], mode)
        	temp = []
        	for x in global_types[chInd[0]]:
        		temp += [[x[0], mode]]
        	global_types[chInd[0]] = temp
        	curr_word = -1
    else:
        update(sent_list)

    my_context["passive"] = checkPassive()
    if (my_context["passive"] == 1):
        my_context["passiveForm"] = getPassive(sent_list)
    else:
        my_context["passiveForm"] = ""
    global_words = form_words(sent_list)
    my_context["words"] = context_words()
    updateSuggestions()
    return render(request, "main.html", my_context)

def context_words():
    l = []
    types = [item[0] for sublist in global_types for item in sublist]
    for x in range(0, len(types)):
        l += [[global_words[x], types[x]]]
    return l

def update(sent_list):
    global global_sent_list
    global global_words
    global global_suggestions
    global global_types
    sorted_sent = global_sent_list
    sorted_sent.sort()
    old = len(global_sent_list)
    new = len(sent_list)
    new_sugg = [[[] for x in y.split()] for y in sent_list]
    new_type = [[[0, 1] for x in y.split()] for y in sent_list]
    for i in range(0, new):
        ind = bisect_left(sorted_sent, sent_list[i])
        if (ind == old):
            # load new suggestions here
            [new_sugg[i], mode] = getSuggestions(sent_list[i], 1)
            new_type[i] = []
            for x in new_sugg[i]:
                if (len(x) == 1):
                    new_type[i] += [[0, mode]]
                else:
                    new_type[i] += [[mode, mode]]
        else:
            new_sugg[i] = global_suggestions[ind]
            new_type[i] = global_types[ind]
    global_suggestions = new_sugg
    global_types = new_type
    global_sent_list = sent_list
    global_words = form_words(global_sent_list)

def updateSuggestions():
	global global_types
	global global_suggestions
	for x in range(0, len(global_types)):
		y = [i[0]==0 for i in global_types[x]]
		if(all(y)):
			print("hello")
			t = []
			for i in global_types[x]:
				t += [[i[1], i[1]]]
			global_types[x] = t
			global_suggestions[x] = getSuggestions(global_sent_list[x], t[1][1])

def replace_in_sent(sent_list, curr_word, new_word):
    global global_sent_list
    ind = 0
    ind2 = 0
    y = []
    for x in sent_list:
        leng = len(x.split())
        if (curr_word >= leng):
            curr_word -= leng
            ind += leng
            ind2 += 1
            continue
        ind += curr_word
        y = x.split()
        y[curr_word] = new_word
        break
    try:
        sent_list[ind2] = ""
    except:
        sent_list += [""]
    for i in y:
        sent_list[ind2] += " " + i
    sent_list[ind2] = sent_list[ind2][1:]
    global_sent_list[ind2] = sent_list[ind2]
    return [ind2, curr_word]


def getIndex(sent_list, curr_word):
    ind2 = 0
    for x in sent_list:
        leng = len(x.split())
        if (curr_word >= leng):
            curr_word -= leng
            ind2 += 1
            continue
        break
    return [ind2, curr_word]


def checkPassive():
    try:
    	m = min([min([x[1] for x in c]) for c in global_types])
    except:
    	return 0
    if (m > 0):
        return 1
    else:
        return 0

def updateTypes(chInd, new_word):
    global global_types
    [i, j] = chInd
    c = global_types[i][:j]
    [a, b] = global_types[i][j]
    for x in range(0, len(new_word.split())):
        c += [[0, b + 1]]
    try:
        c += global_types[i][j + 1:]
    except:
        pass
    global_types[i] = c
    return min([x[1] for x in c])
