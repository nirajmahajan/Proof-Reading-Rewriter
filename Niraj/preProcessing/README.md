# Pre Processing of the Input Data

In this section, given an input of the data in the form of a list of strings, we will do some pre processing

1. ### Case Correction :  

   In this section, we aim at correcting errors in the case of the words that are at the start of the sentences.

   

2. ### White Space Corrector:

   In this section we remove unnecessary white space from the words and add space wherever necessary.

   - Punctuations like full stops, commas, exclamation marks, question marks and closing brackets cannot be preceded by a space, but need to have a space afterwards
   - Similarly, opening brackets need a space before them, but cannot have following space!
   - We have also implemented a feature to remove repetitions in punctuations; 
     - For example : Gondor has no king....  --------> Gondor has no king.  
     - For example : Ride light and swift!!!!!  ---------> Ride light and swift!

