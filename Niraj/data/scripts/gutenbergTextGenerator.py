# creates raw text from the gutenberg list of novels
# just throws out the text to stdio, so do pipeline to a file
import nltk
from nltk.corpus import gutenberg

for fileid in gutenberg.fileids():


