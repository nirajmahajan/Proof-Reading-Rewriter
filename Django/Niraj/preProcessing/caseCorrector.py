import re
# Inputs a list of strings and returns corrections for Case
# This is based on the position of full stops and ^ characters.
# Corrects only the first letter of every sentence
def caseCorrector(in_list):
	out_list = in_list.copy()
	out_list[0] = out_list[0].capitalize()
	for i in range(len(out_list)):
		if (i == len(out_list)-1):
			continue
		else:
			rex = re.compile(r'[!.?]+$')
			found = rex.search(out_list[i]) != None
			if(found):
				out_list[i+1] = out_list[i+1].capitalize()

	return out_list