import re
import sys
import os
import nltk
import urllib
import json
from nltk.tokenize.treebank import TreebankWordDetokenizer
from functions.main import *

# sys.path.insert(0, '../../')
from main import *

# made the strings raw
alphabets = r"([A-Za-z])"
prefixes = r"(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = r"(Inc|Ltd|Jr|Sr|Co)"
starters = r"(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = r"([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = r"[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\r", "")
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]",
                  "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>",
                  text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    sentences = [
        TreebankWordDetokenizer().detokenize(nltk.word_tokenize(s))
        for s in sentences
    ]
    return sentences


def form_words(sent_list):
    l = []
    for x in sent_list:
        l += x.split()
    return l


def getSuggestions(sentence, mode):
    # tempans = [[[] for x in sentence.split()], 1]
    (ans, comment) = processSentence(sentence, 'grammar')
    #returns [a, b] where a are suggestions and b is the mode of sentence currently
    return [ans, 1]
    # return tempans

def sync_word(w1, w2):
    l1 = nltk.pos_tag(nltk.word_tokenize(w1))
    w = l1.pop(0)
    ans = w2
    if w[0][0].isupper():
        ans = w2.capitalize()
    else:
        ans = w2.lower()
    for i in l1:
        if i[1] != 'RB':
            ans = ans + i[0]
    return ans

def syn_list(word):
    url = "https://api.datamuse.com/words?ml=" + word
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    json_data = json.loads(data)
    word_list = []
    for x in json_data:
        word_list.append(x['word'])
    return word_list


def getPassive(sent_list):
    rl = [active_to_passive(s) for s in sent_list]
    return " ".join(rl)

def join(li):
    return " ".join(li)

# def rewrite(sentence):
#     rewrite_types = [u'NN', u'NNS', u'JJ', u'JJS']
#     pos_tokenizer = nlp(sentence)
#     words = []
#     for token in pos_tokenizer:
#         print(token.pos_, token.text, token.tag_)
#         if token.tag_ in rewrite_types:
#             words.append(token.text)
#     rewrited_sentence = sentence
#     for word in words:
#         word_syn = best_syn(word)
#         rewrited_sentence = rewrited_sentence.replace(word, word_syn)
#     l=(nltk.word_tokenize(rewrited_sentence))
#     rewrited_sentence=TreebankWordDetokenizer().detokenize(l)
#     return rewrited_sentence