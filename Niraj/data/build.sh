#!/bin/bash
# Script to build all data from an updated raw.txt file
# replace the raw.txt file in the 'raw' directory and run this script

if [[ ! $PWD == *data ]]; then
	echo "Echo to the data directory before running the script"
	exit 1
fi

if [[ ! -f  "raw/raw.txt" ]]; then
	echo "Please copy 'raw.txt' to the 'raw' directory before running the script"
	exit 1
fi

rm -rf textfiles > /dev/null 2>&1
mkdir textfiles



echo "Processing Raw Data"
cp raw/raw.txt textfiles/sentence_list.txt
cd scripts
./processText.sh
cd ..
echo "Raw text Processed"
echo

echo "Generating Word List"
cp textfiles/sentence_list.txt textfiles/db.txt
cd scripts
./wordIsolator.sh
cd ..
echo "Word List Generated"
echo



echo "Generating Dictionary and Frequency Data"
cd scripts
python3 frequencyDataGenerator.py
cd ..
echo "Frequency Data and dictionary Generated"
echo

echo "Generating Trigram Data"
cd scripts
python3 trigramGenerator.py --path ../textfiles/sentence_list.txt
cd ..
echo "Trigram Data Generated"
echo

# echo "Cleaning Up..."
# rm -rf textfiles > /dev/null 2>&1

echo "Done!"