''' Program by Jeff Larson to aid solving the 9/04/2016 Sunday Puzzle
source: http://www.npr.org/2016/09/04/492557498/the-answer-remains-the-same-whichever-way-you-want-to-look-at-it
'''

# Collect 59 five letter words and 618 four letter words
def collect_unix_words():
	'''
	collects all five letter words with 'rn' and four letter words with 'm'
	OUTPUT:
		fives: set of strings
		fours: set of strings
	'''
	fives = set()
	fours = set()
	with open('/usr/share/dict/words') as f:
		for line in f:
			word = line[:-1]
			if word.isupper():
				continue	
			len_word = len(word)
			if (len_word == 5) & (word.find('rn') > -1):
				fives.add(word)
			elif (len_word == 4) & (word.find('m') > -1): 
				fours.add(word)
	return fives, fours

# compete the 'rn' -> 'm' operation on all five letter words
def cross_check(fives, fours):
	'''
	prints out possible solutions to the puzzle by transforming 'rn' -> 'm' on each 5-letter word and cross-checking it against the set of 4-letter words
	INPUT:
		fives, fours: sets of strings
	'''
	for five in fives:
		four = five.replace('rn', 'm')
		if four in fours:
			print 'Is %s the opposite of %s??' % (five, four) 
	return 

def screen_solutions():
	fives, fours = collect_unix_words()
	cross_check(fives, fours)
	return 

if __name__ == '__main__':
	screen_solutions()