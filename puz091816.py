''' Program by Jeff Larson to aid solving the 9/18/2016 Sunday Puzzle
source: http://www.npr.org/2016/09/18/494382869/do-remember-the-first-3-letters-of-september
'''

from collections import defaultdict
from itertools import product
import time
import requests

def collect_unix_words():
	'''
	collects all non-proper nouns of length 3, 4, and 7 and stores them in a dictionary
	OUTPUT:
		words_by_len: dict
	'''
	words_by_len = defaultdict(set)
	with open('/usr/share/dict/words') as f:
		for line in f:
			word = line[:-1]
			if word.istitle():
				continue	
			len_word = len(word)
			if len_word in [3,4,7]:
				words_by_len[len_word].add(word)
	return words_by_len

words_by_len = collect_unix_words()

## approach: form every combo of 3 & 4 letter words
# 1420 3-letter words
# 5272 4-letter words
# 7486240 combinations to check
# * 2 permutations
# = 14,972,480 unique permutaions to check against 7s

def create_phrases(words_by_len):
	phrases = []
	for three, four in product(words_by_len[3],words_by_len[4]):
		if three + four in words_by_len[7]:
			phrases.append(four + ' and ' + three)
			print four + ' and ' + three
		if four + three in words_by_len[7]:
			phrases.append(three + ' and ' + four)
			print three + ' and ' + four
	return phrases

phrases = create_phrases(words_by_len)

## check all phrases against idiom in thefreedictionay.com
# the requests generate the following status codes:
# 404: the phrase isn't found
# 403: the request is not honored
# 200: the phrase IS FOUND
# The following loop tries to minimize the 

good_r = []
while phrases[i:]:
	for i, phrase in enumerate(phrases[i:], i):
		print 'checking', phrase, '...'
		if i % 50 == 0:
			print 'cooling down...'
			time.sleep(5)
		r = requests.get('http://idioms.thefreedictionary.com/%s' % phrase)
		print r.status_code
		if r.status_code == 200:
			print 
			print 'FOUND ONE::::'
			good_r.append(phrase)
			print phrase
			print
		elif r.status_code == 403:
			print 'PROBLEM! Status 403'
			time.sleep(15)
			break
		time.sleep(1)


