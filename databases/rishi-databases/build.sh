#!/bin/bash
# Just a simple script to build databases
# Credits to the python script : Rishi Agarwal

if [[ ! $PWD == *rishi-databases ]]; then
	echo "Echo to the rishi-databases directory before running the script"
	exit 1
fi

if [[ ! -f  "scripts/participles.csv" ]]; then
	echo "Please copy participles.csv to the scripts directory before running the script"
	exit 1
fi

if [[ ! -f  "scripts/words-beginning-vowel-no-an.csv" ]]; then
	echo "Please copy words-beginning-vowel-no-an.csv to the scripts directory before running the script"
	exit 1
fi

if [[ ! -f  "scripts/participles.py" ]]; then
	echo "Please copy participles.py to the scripts directory before running the script"
	exit 1
fi

if [[ ! -f  "scripts/list-vowel-no-an.py" ]]; then
	echo "Please copy list-vowel-no-an.py to the scripts directory before running the script"
	exit 1
fi

cd scripts

echo "Creating participles database"
python3 participles.py
echo "Done"
echo

echo "Creating articles database"
python3 list-vowel-no-an.py
echo "Done"
echo

cd ..
echo "Finished!"
