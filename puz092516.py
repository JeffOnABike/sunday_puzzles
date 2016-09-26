''' Program by Jeff Larson to aid solving the 9/25/2016 Sunday Puzzle
puzzle source: http://www.npr.org/2016/09/25/495308799/want-to-get-an-a-better-know-your-words-backward-and-forward
'''

from collections import defaultdict

def collect_unix_words():
	'''
	collects words and their endings that meet the criteria of the puzzle
	OUTPUT:
		words: dict
		- words fitting puzzle criteria for first letter and length
		endings: dict
		 - unique endings for each word in words dict
	'''
	with open('/usr/share/dict/words') as f:
		words = defaultdict(set)
		endings = defaultdict(set)
		for line in f:
			word = line[:-1]
			if word.isupper():
				continue	
			len_word = len(word)
			if (len_word == 4):
				if word[0] == 'f':
					words['f'].add(word)
					endings['f'].add(word[-3:])
				elif word[0] == 's':
					words['s'].add(word)
					endings['s'].add(word[-3:])
			elif (len_word == 5) & (word[0] == 'g'):
				words['g'].add(word)
				endings['g'].add(word[-3:])
	return words, endings

def suss_out_possibles(words, endings):
	'''
	prints out all possible combinations from words and endings which meet the criteria of all having the same ending three letters
	INPUT:
		words, endings
	'''

	common_endings = endings['s'].intersection(endings['f'], endings['g'])
	for ending in common_endings:
		s_word = 's' + ending
		f_word = 'f' + ending
		g_words = filter(lambda w: w.endswith(ending), words['g'])
		for g_word in g_words:
			print ' : '.join([f_word, s_word, g_word])
	return 

if __name__ == '__main__':
	words, endings = collect_unix_words()
	suss_out_possibles(words, endings)
