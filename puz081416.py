import requests
from bs4 import BeautifulSoup

''' Program by Jeff Larson to aid solving the 8/14/2016 Sunday Puzzle
source: http://www.npr.org/2016/08/14/489898589/the-end-remains-the-same-all-youve-got-to-do-is-find-it'''

# Get countries
def get_countries():
	url = 'https://simple.wikipedia.org/wiki/List_of_countries'
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	countries = []
	for p in soup.findAll('p'):
		stuff =  p.findAll('a')
		if stuff:
			for c in stuff:
				countries.append(c['title'])
	# eliminate dupes
	countries = list(set(countries))
	# make a dict of the set of letters for each country
	country_dict = {}
	for country in countries:
		country = country.lower().replace(' ', '')
		country_dict[country] = set(country)
	return country_dict

# Get body parts
def get_body_parts():
	url = 'http://www.enchantedlearning.com/wordlist/body.shtml'	
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	table = soup.findAll('table')[4]
	parts = table.text.split('\n')
	body_parts = filter(lambda x: (len(x) > 1) & x.islower(), parts)
	# make a dict of the set of letters for each body part
	body_parts_dict = {}
	for body_part in body_parts:
		body_part = body_part.replace(' ', '')
		body_parts_dict[body_part] = set(body_part)
	return body_parts_dict

def cross_out(body_part, country):
	leftover = ''
	for i, l in enumerate(country):
		if l == body_part[0]:
			# drop first letter on body_part word remaining
			body_part = body_part[1:]
			# if body_part word has been completely found
			if body_part == '':
				return leftover + country[i+1:]
		else:
			leftover += l
	return False

def check_one_country(country_dict, country, body_parts_dict):
	country_set = country_dict[country]
	leftovers = []
	for body_part in body_parts_dict:
		body_part_set = body_parts_dict[body_part]
		# see if body_part is plausibly in country
		if body_part_set.issubset(country_set):
			leftover = cross_out(body_part, country)
			if leftover:
				leftovers.append(leftover)
				print country, '-', body_part, '=', leftover
				print
	return leftovers

def check_all_countries(country_dict, body_parts_dict):
	print
	answers = []
	for country in country_dict:
		leftovers = check_one_country(country_dict, country, body_parts_dict)
		answers.extend(leftovers)
	return answers

def view_possible_answers(return_answers = False):
	country_dict = get_countries()
	body_parts_dict = get_body_parts()
	answers = check_all_countries(country_dict, body_parts_dict)
	if return_answers:
		return answers

if __name__ == '__main__':
	view_possible_answers()
