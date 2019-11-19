"""
Program by Jeff Larson (jeffonabike) to aid solving the 2019/11/17 Sunday Puzzle

puzzle source:
	https://www.npr.org/2019/11/17/780092243/sunday-puzzle-words-that-end-in-llo
This week's challenge: 
	The city of Mobile, Ala., has the interesting property that the name of the city has exactly the same consonants as its state (M, B, and L), albeit in a different order.
	What is the next-largest U.S. city for which this is true?
Data source:
	cities: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
Credit on code tips: 
	csvreader: https://docs.python.org/3/library/csv.html
	regex: https://www.tutorialspoint.com/How-to-remove-all-special-characters-punctuation-and-spaces-from-a-string-in-Python
"""

import csv
import re

def read_file(fname):
	rows = []
	with open(fname) as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			rows.append(row)
	return rows

def parse_row(row):
	rank = row[0]
	city = row[1]
	state = row[2]
	return rank, city, state

def clean_word(word):
	word = re.sub('[^A-Za-z]+', '', word)
	return word.lower()

def remove_vowels(word):
	letters = set(word)
	vowels = {'a', 'e', 'i', 'o', 'u'}
	return letters - vowels

def compare_city_state(city, state):
	city_letters = remove_vowels(city)
	state_letters = remove_vowels(state)
	return city_letters == state_letters

def work_the_magic(fname, header=None):
	rows = read_file(fname)
	res = []
	for row in rows:
		rank, city, state = parse_row(row)
		city_clean = clean_word(city)
		state_clean = clean_word(state)
		if compare_city_state(city_clean, state_clean):
			res.append([city, state, rank])
	return res

if __name__ == '__main__':
	fname = 'data/dat20191117.csv'
	res = work_the_magic(fname, header=None)
	print(res)