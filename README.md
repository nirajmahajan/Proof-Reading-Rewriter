# Proof Reading Re-writer

### Contributors -

[Niraj Mahajan](https://www.cse.iitb.ac.in/~nirajm) - 180050069  
[Rishi Agarwal](https://www.cse.iitb.ac.in/~rishiagarwal) - 180050086  
[Neel Aryan Gupta](https://www.cse.iitb.ac.in/~neelaryan) - 180050067  

### Introduction:

We have created a simple proof reading re-writer as a part of our course project in the Software Systems Lab(CS251).
This proof reading re-writer, built on a Django front end, this project includes interesting features like:

1. Error Check on Sentences
2. Quality upgrade (Rewriting Sentences)
3. Optical Character Recognition (not augmented into the front end)
4. Active to Passive Voice Converter

##### The code corrects errors like:

1. Spelling Errors
2. Grammatical Errors like those in:
   - Prepositions
   - Articles
   - Verb Forms
   - Pronouns
   - Demonstratives
   - Tenses
   - Auxiliary verbs

The project mainly uses the method of trigrams, where the probability of every word fitting in a particular position is calculated on the basis of it's position, that is, it's neighbouring words. (biased slightly using bigrams as well).

##### Apart from this, we also have mined a gargantuan database comprising of:

- 20399999 Bigrams
- 80278278 Trigrams
- 504651 Dictionary Words
- 2650877 Word Frequencies (not necessarily dictionary words, might contain slang words)

This data is mined with the help of text files downloaded from the Gutenberg corpora of books, available freely online.
(Refer [here](https://webapps.stackexchange.com/questions/12311/how-to-download-all-english-books-from-gutenberg) for more details)
The above reference gives a way to download several files with URLs. For the code, refer [here](https://github.com/nirajmahajan/Proof-Reading-Rewriter/tree/master/databases/data/gutenburgDownload). 

#### Usage of Code:

Simply run the main.py located in the root directory of the repository in the following manner

```bash
python3 main.py runserver # fire up the server
firefox localhost:8000 # if firefox installed
google-chrome localhost:8000 # if google-chrome installed
```





