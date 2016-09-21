'''
puzzle: http://www.npr.org/2016/08/28/491699329/3-3-8-it-does-in-this-weeks-puzzle
updated: 8/30
'''
from collections import defaultdict
import requests

''' 'reigned' is in mielisetronk but 'reignited' is not '''

def collect_mielisetronk_words():
	url = 'http://www.mieliestronk.com/corncob_lowercase.txt'
	r = requests.get(url)
	sevens = defaultdict(set)
	nines = defaultdict(set)
	all_words = r.text.split('\r\n')
	for line in all_words:
		# word = line.strip()
		if line:
			word = line.strip()
			first_l = word[0]
			if word.islower():
				if len(word) == 7:
					sevens[first_l].add(word)
				# 'it' can only be found at positions 1-7
				# first_l 1 2 3 4 5 6 7 last_l	
				elif (len(word) == 9) and (0 < word.find('it') < 8): 
					nines[first_l].add(word)
	return sevens, nines

''' 'reigned' nor 'reignited' are in unix '''

def collect_unix_words():
	'''
	collects all ordinary seven and nine letter words from unix as dictionaries
	'''
	sevens = defaultdict(set)
	nines = defaultdict(set)
	with open('/usr/share/dict/words') as f:
		for line in f:
			word = line[:-1]
			first_l = word[0]
			if word.islower():
				if len(word) == 7:
					sevens[first_l].add(word)
				# 'it' can only be found at positions 1-7
				# first_l 1 2 3 4 5 6 7 last_l	
				elif (len(word) == 9) and (0 < word.find('it') < 8): 
					nines[first_l].add(word)
	return sevens, nines


def subtract_it(nine, i = 1):
	'''
	returns a list of words with valid positions of the letter combination 'it' removed from the input nine-letter word
	N.B.:
	i refers to the minimum absolute index from which 'it' is sought
	it_loc is a relative index starting from i where 'it' is found, if at all
	'''
 	it_loc = nine[i:8].find('it')
 	if it_loc < 0:
 		# no more 'it' is found, terminate recursion
 		return []
 	else: 
 		i += it_loc 
 		# split word at index where 'it' is found
 		start = nine[:i]
 		end = nine[i:]
 		# replace only the 'it' at the i index
 		word = start + end.replace('it', '', 1)
 		# move index past the 'it' index for next call
 		i += 2
 		return [word] + subtract_it(nine, i)


def check_a_nine(sevens, nine, first_l):
	'''
	given a nine letter word, return tuples of (seven, nine) that are valid to the puzzle instructions
	'''
	matches = []
	# for this nine letter word subtract 'it' every valid way and return as a set
	seven_set = set(subtract_it(nine))
	for seven in seven_set:
		# check for existence in dict
		if seven in sevens[first_l]:
			print 'found real word: ', nine, ' - "it" = ', seven
			matches.append((seven, nine))
	return matches

def check_for_letter(sevens, nines, first_l):
	'''
	given a starting letter for a word, return a list of tuples of all matches (seven, nine) starting with that letter
	'''
	letter_matches = []
	for nine in nines[first_l]:
		matches = check_a_nine(sevens, nine, first_l)
		if matches:
			letter_matches.extend(matches)	
	return letter_matches


def check_all_letters(sevens, nines):
	'''
	return all matches of (seven, nine) for all starting letters
	'''
	all_matches = []
	for first_l in nines:
		print 'now checking letter', first_l
		letter_matches = check_for_letter(sevens, nines, first_l)
		all_matches.extend(letter_matches)
		print
	return all_matches


if __name__ == '__main__':
	sevens, nines = collect_words()
	all_matches = check_all_letters(sevens, nines)
	print len(all_matches), 'matches to consider:'
	for each in all_matches:
		print each


# def syllables(word):
# 	'''
# 	Counts syllables of input word.
# 	Code sourced from post on Stack Overflow by AbigailB
# 	http://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
# 	'''
# 	count = 0
# 	vowels = 'aeiouy'
# 	word = word.lower().strip(".:;?!")
# 	if word[0] in vowels:
# 	    count +=1
# 	for index in range(1,len(word)):
# 	    if word[index] in vowels and word[index-1] not in vowels:
# 	        count +=1
# 	if word.endswith('e'):
# 	    count -= 1
# 	if word.endswith('le'):
# 	    count+=1
# 	if count == 0:
# 	    count +=1
# 	return count

# # def screen_one_sylls(sevens):
#  for seven in one_syll:
#     print seven
#     if raw_input('y?') == 'y':
#         screened_sevens.append(seven)
#    ....:         
