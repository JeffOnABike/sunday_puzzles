'''
Next week's challenge, from listener Darrell Myers of Somerville, Mass.: Name a famous actress of the past — first and last names, 10 letters altogether. Change one letter in the first name and one letter in the last. The result is a two-word phrase naming a food item often found in a kitchen cabinet or refrigerator. What is it?

best answer so far: Jean Porter > Bean Sorter
'''
import requests
from bs4 import BeautifulSoup

def get_valid_names(url):
	'''
	for a first and last initial, scrape from available urls the names which best satisfy syllable compliance
	'''

	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	table = soup.find('table')
	valid_names = []
	for tr in table.findAll('tr')[8:]:
		attrs = []
		for td in tr.findAll('td'):
			attrs.append(td.text)
			
		name = attrs[0]
		split_name = name.split(' ')
		if len(split_name) > 1:
			name = ' '.join((split_name[0], split_name[-1]))
		else:
			name = split_name

		prof = attrs[1]

		dob = attrs[3][-4:]
		of_the_past = False
		if (len(dob) == 4) & (dob.isdigit()):
			of_the_past = int(dob) < 1940
		if (len(name) == 11) & (prof == 'Actor') & (of_the_past):
			valid_names.append(name)
		# if (len(split_name) > 1) and (split_name[0][0] == first_init):
	print
	return valid_names

def form_urls():
	urls = []
	for urlcode1, urlcode2 in zip(range(493, 519), range(63304, 63330)):
		url = 'http://www.nndb.com/lists/%s/%s/' % (urlcode1, str(urlcode2).zfill(9))
		urls.append(url)
	return urls

def collect_names():
	urls = form_urls()
	all_valid_names = []
	for url in urls:
		valid_names = get_valid_names(url)
		all_valid_names.extend(valid_names)
	return all_valid_names

def get_girlnames():
	with open('data/girlnames.txt', 'r') as f:
		girl_names = f.read()

	girlnames = []
	name = ''

	for char in girl_names:
		# is first letter of name
		if (not name) & (char.isupper()):
			name += char
		# is second letter of name
		elif not char.isupper():
			name += char
		# word is done
		elif (len(name) > 0) & (char.isupper()):
			girlnames.append(name)
			name = char
	return girlnames


all_valid_names = collect_names()	
all_valid_girlnames = filter(lambda x: x.split()[0] in girlnames, all_valid_names)
# new_names = []
# for l in all_valid_names:
# 	for name in l:
# 		new_names.append(name)

# with open('data/100916.pkl', 'w') as f:
# 	pickle.dump(new_names, f)
