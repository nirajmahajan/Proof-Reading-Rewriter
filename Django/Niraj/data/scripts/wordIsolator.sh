#/bin/bash
# To be run only after processText.sh

# converts text from proccessed format to one word on each line

# INFILE='../textfiles/db.txt'
INFILE='good.txt'

# replace punctuations with new lines
sed -i 's/\([\.!\?,]\)/\n/g' $INFILE

# each word on a new line
sed -i 's/[ ,]/\n/g' $INFILE

# remove lines with purely characters
sed -i '/^[^a-zA-Z]*$/d' $INFILE

# remove extra lines and leading and lagging extra whitespace
sed -i '/^[ ]*$/d' $INFILE
sed -i 's/^[ ]*//g' $INFILE
sed -i 's/[ ]*$//g' $INFILE