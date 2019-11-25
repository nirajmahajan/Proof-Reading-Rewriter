#!/bin/bash
# converts text from any raw format to the required format
# Every sentence on a new line
# include punctuations like . , ! ? ...  in the trigrams as seperate entities
# remove all numbers and other unecessary punctuations

INFILE='../textfiles/sentence_list.txt'

LINE_START=$(grep -m 1 -n 'CHAPTER I' $INFILE  | cut -d : -f 1)

echo 'Trimming The File'
sed -i '/^[ \t]*/d' $INFILE
echo 'Done'
echo


echo 'Temporarily removing new line characters'
sed -i ':a;N;$!ba;s/\r\n/ /g' $INFILE
echo 'Done'
echo

echo 'Removing digits and unnecessary punctuations'
sed -i 's/[]_~`<>\/();:0-9@#\$%\^&\*[]/ /g' $INFILE
echo 'Done'
echo

echo 'Protecting ellipsis with @@ on both side'
sed -i 's/\.\.\./@@/g' $INFILE
echo 'Done'
echo

echo 'Replacing .!? with space on both side'
sed -i 's/\([\.!\?]\)/ \1\n/g' $INFILE
echo 'Done'
echo

echo 'Removing " '
sed -i 's/"/\n/g' $INFILE
echo 'Done'
echo

echo 'Replacing , with space on both side'
sed -i 's/,/ , /g' $INFILE
echo 'Done'
echo

echo 'Restoring ellipsis '
sed -i 's/@@/ ...\n/g' $INFILE
echo 'Done'
echo

echo 'Removing extra lines and leading and lagging extra whitespace'
sed -i '/^[ ]*$/d' $INFILE
echo 'Done'
echo

echo 'Removing leading whitespace'
sed -i 's/^[ ]*//g' $INFILE
echo 'Done'
echo

echo 'Removing lagging whitespace'
sed -i 's/[ ]*$//g' $INFILE
echo 'Done'
echo

echo 'Finished!!'
# An alias on my laptop to shout out that the task is finished
# will cause an error on other systems
announceDone