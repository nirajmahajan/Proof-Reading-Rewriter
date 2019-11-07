from spacy.tokenizer import Tokenizer
from spacy.lang.en.examples import sentences
from suggest_synonym import *

def rewrite(sentence):
    rewrite_types = [u'NN', u'NNS', u'JJ', u'JJS']
    pos_tokenizer = nlp(sentence)
    words = []
    for token in pos_tokenizer:
        print(token.pos_, token.text, token.tag_)
        if token.tag_ in rewrite_types:
            words.append(token.text)
    rewrited_sentence = sentence
    for word in words:
        word_syn = best_syn(word)
        rewrited_sentence = rewrited_sentence.replace(word, word_syn)
    return rewrited_sentence
