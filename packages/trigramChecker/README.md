# Trigram Checker!

In this component of the project, I have implemented a trigram checker based using the [phrase finder online API](https://phrasefinder.io/)

### Code Structure:

2. The noun_id.py file adds '#' to the start of every noun present in the sentence using NLTK's very own tokenizer.
3. The main file, trigramChecker.py, has a function 'trigramCheck' which takes in a list of words and returns a list of list of suggestions for the word at the corresponding index in the input.

### Usage of Code

1. Here is a sample of how to run the code

 ```python
from path/to/trigramChecker import trigramCheck
from path/to/noun_id import noun_identifier
sentence = 'Indi is a beatiful county'

spellCheck(noun_identifier(sentence).split())       
 ```