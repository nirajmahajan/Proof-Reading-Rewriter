from spacy.tokenizer import Tokenizer
from spacy.lang.en.examples import sentences
from suggest_synonym import *
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

def rewrite(sentence):
    ans = []
    rewrite_types = [u'NN', u'NNS', u'JJ', u'JJS']
    pos_tokenizer = nlp(sentence)
    words = []
    for token in pos_tokenizer:
        print(token.pos_, token.text, token.tag_)
        if token.tag_ in rewrite_types:
            words.append(token.text)
    rewrited_sentence = sentence
    for word in words:
        ans.append(syn_list(word))
        # word_syn = best_syn(word)
        # rewrited_sentence = rewrited_sentence.replace(word, word_syn)
    # l=(nltk.word_tokenize(rewrited_sentence))
    # rewrited_sentence=TreebankWordDetokenizer().detokenize(l)
    # return rewrited_sentence
    return ans
