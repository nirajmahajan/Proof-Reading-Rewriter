# Spell Checker!

In this component of the project, I have implemented an efficient spellchecker based on the [Levenshtein Algorithm](https://dzone.com/articles/the-levenshtein-algorithm-1
) of calculating the minimum distance. I have used a database of words from python's own nltk.corpus, augmented further by data obtained from [this](https://github.com/dwyl/english-words
) GitHub repository. I also have used a database on frequencies of words [from](https://norvig.com/spell-correct.html), which has over a million words, to have better and more relevant suggestions to spelling errors. 

### Code Structure:

1. The database files are stored as pickle files in the data folder, where the freq.pickle file has a dictionary of, Ill, frequencies! And the db.pickle has an unordered_set of words. The only reason that made me augment the additional database into the nltk.corpus database was that nltk.courpus did not have words with apostrophe's.
2. The helpers.py file has helper functions that compute the distance between two strings, and a couple other that return all the strings that have a distance of 'one' and 'two' with respect to a particular string. These functions can be accessed by other sub units as Ill since they are a bit general functions to the project.
3. The main file, spellChecker.py, has a function 'spellChecker' which takes in a list of words, and an optional argument to specify the maximum suggestions output by the code. (default 6).

### Technicalities

1. In implementing the spellchecker, I had two options. Either to iterate over all words in the dictionary and check if the distance is feasible or not, or, to generate all such strings which have a distance of one and two from the input string and check for the existence of all these strings. I have chosen the later, which is indeed more efficient since looking up a particular string in the Dictionary takes up O(logn) while there will be hardly 100 such strings, or perhaps 200. But iterating throughout the dictionary linearly will be too costly.
2. After establishing the possible suggestions, I used the frequency table, generated and saved as mentioned earlier, and sorted the probable suggestions according to their frequencies. In this as well, I have given a penalty of 150 frequency points to words that have a distance of '2' from the original string, while I have give a bonus of 150 frequency points to those words having a distance of '1' from the original string, to generate a clear bias and advantage for words with just on change/difference

### Usage of Code

1. Here is a sample of how to run the code

 ```python
from path/to/spellChecker import spellCheck
sentence = 'Indi is a beatiful county'

# Ensure that the only punctuations passed are hifens and apostrophe
spellCheck(sentence.split(), limit = 10, only_wrong = True)
# only wrong will give suggestions only for those words with incorrect spellings
       
   
 ```