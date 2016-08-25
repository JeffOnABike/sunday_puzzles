''' Program by Jeff Larson to aid solving the 8/21/2016 Sunday Puzzle. Ancillary function 'syllables' sourced from a post on Stack overflow by AbigailB
source: http://www.npr.org/2016/08/21/490647499/name-that-celebrity-all-you-have-to-do-is-rhyme'''

import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import cPickle as pickle

# url to list of celebrities by last initial:
urls = {'S': 'http://www.nndb.com/lists/511/000063322/',
		'M': 'http://www.nndb.com/lists/505/000063316/'
		}

def syllables(word):
	'''
	Counts syllables of input word.
	Code sourced from post on Stack Overflow by AbigailB
	http://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
	'''
	count = 0
	vowels = 'aeiouy'
	word = word.lower().strip(".:;?!")
	if word[0] in vowels:
	    count +=1
	for index in range(1,len(word)):
	    if word[index] in vowels and word[index-1] not in vowels:
	        count +=1
	if word.endswith('e'):
	    count -= 1
	if word.endswith('le'):
	    count+=1
	if count == 0:
	    count +=1
	return count

def check_syllable_compliance(split_name):
	'''
	Return names with (1,2) or (2,1) syllable patterns
	'''
	first_name, last_name = split_name[0], split_name[-1]
	first_name_syll = syllables(first_name)
	if first_name_syll < 3:
		last_name_syll = syllables(last_name)
		if (last_name_syll < 3) and (last_name_syll != first_name_syll):
			return (first_name_syll, last_name_syll)
	return None

def get_valid_names(first_init, last_init, urls):
	'''
	for a first and last initial, scrape from available urls the names which best satisfy syllable compliance
	'''
	let_url = urls[last_init]
	r = requests.get(let_url)
	print 'scraping for last initial %s from' % last_init, let_url
	soup = BeautifulSoup(r.content)
	table = soup.find('table')
	valid_names = {}
	for each in table.findAll('a'):
		name = each.text
		split_name = name.split()
		if (len(split_name) > 1) and (split_name[0][0] == first_init):
			name_syll = check_syllable_compliance(split_name)
			if name_syll:
				valid_names[name] = name_syll
	print
	return valid_names


def reverse_name_dict(name_dict):
	'''turn keys to values and vice versa'''
	name_dict_rev = defaultdict(set)
	for k,v in name_dict.iteritems():
	    name_dict_rev[v].add(k)
	return name_dict_rev

def match_last_letters(bs_rev, gm_rev):
	for syll_pattern in ((1,2),(2,1)):
		print 'syllable pattern: ',syll_pattern
		print 'first names to consider:'
		firsts = {name.split()[0] for name in bs_rev[syll_pattern].union(gm_rev[syll_pattern])}
		print sorted(firsts, key = lambda x: x[-1])
		print
	return

def screen_first(first_name, first_init_dict):
	first_let = first_name[0]
	valid_names = first_init_dict[first_let]
	results = [name for name in valid_names if name.split()[0] == first_name]
	print results
	return results

def make_name_dicts():
	'''
	makes dictionaries of 
		name: syll_pattern
		syll_pattern : name
	'''
	# 79 people
	bs = get_valid_names('B', 'S', urls)
	# 65 people	
	gm = get_valid_names('G', 'M', urls)
	# write dicts  to pickle in case site changes
	with open('data/082116_gm.pkl', 'w') as f:
		pickle.dump(gm, f)
	with open('data/082116_bs.pkl', 'w') as f:
		pickle.dump(bs, f)
	# organize entries by syllable pattern
	bs_rev = reverse_name_dict(bs)
	gm_rev = reverse_name_dict(gm)
	return bs, bs_rev, gm, gm_rev

def work_the_magic():
	''' 
	Does everything
	'''
	bs, bs_rev, gm, gm_rev = make_name_dicts()
	# print out first names alphabetized by last letter for inspection
	match_last_letters(bs_rev, gm_rev)
	first_init_dict = {
		'B' : bs,
		'G' : gm
		}	
	print 'might be these:'
	screen_first('B.', first_init_dict)
	screen_first('G.', first_init_dict)
	print 'maybe not...'
	print 
	print 'what about these:'
	screen_first('Ben', first_init_dict)
	screen_first('Glenn', first_init_dict)
	print 
	print 'My solution:'
	print 'https://en.wikipedia.org/wiki/Glenn_Miller'
	print 'https://en.wikipedia.org/wiki/Ben_Stiller'
	return

if __name__ == '__main__':
	work_the_magic()