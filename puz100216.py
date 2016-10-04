''' Program by Jeff Larson to aid solving the 10/02/2016 Sunday Puzzle
puzzle source: http://www.npr.org/2016/10/02/496211559/for-a-sunny-punny-sunday-trip-how-about-a-trip-to-the-grocery-isle
'''

from collections import defaultdict, Counter


def collect_unix_words():
	'''
	collects words according to the criteria of the puzzle
	OUTPUT:
		fives, sixes, elevnes: dict
		- each dict has string keys and Counter values
	'''
	with open('/usr/share/dict/words') as f:
		fives = {}
		sixes = {}
		elevens = {}
		for line in f:
			word = line[:-1]
			if word.istitle():
				continue	
			len_word = len(word)
			if (len_word == 5):
				fives[word] = Counter(word)
			elif (len_word == 6):
				sixes[word] = Counter(word)
			elif (len_word == 11) & (word[0] == 'h') & \
				(word.endswith('er') or word.endswith('ist')):
				elevens[word] = Counter(word)
	return fives, sixes, elevens

def check_elevens(fives, sixes, elevens):
	'''
	screens all possible combinations of five, six, and eleven letter words 
	in which the six and five letter word's letters combine to make the 11-letter word
	INPUT:
		fives, sixes, elevens: dicts
	OUTPUT:
		successes: dict
		- keys: 11-letter words
		- values: tuples : (5-letter word, 6-letter word)
	'''
	successes = defaultdict(set)
	for eleven in elevens:
		for five in fives:
			leftover = Counter(eleven) - Counter(five)
			if sum(leftover.values()) == 6:
				for six, c in sixes.iteritems():
					if leftover == c:
						successes[eleven].add((five, six))
						print eleven, ' : ', five, six
	return successes

def screen_answers():
	'''
	main block
	'''
	fives, sixes, elevens = collect_unix_words()
	successes = check_elevens(fives, sixes, elevens)
	return successes

if __name__ == '__main__':
	screen_answers()	