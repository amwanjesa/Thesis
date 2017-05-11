# -*- encoding: utf-8 -*-
import xml.etree.ElementTree as ET
import click
import requests  # http://docs.python-requests.org/en/latest/
import json
import os
import itertools
import warnings
import sys
from collections import Counter
from nltk.tokenize import word_tokenize as wtk
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
seen = []
warnings.filterwarnings('ignore')
# get the subcategories of the top wikipedia category "Alles"

def parse(filename, categories):
	with open(filename, 'w',  encoding='utf-8') as outfile:
		for category in tqdm(categories):
			print (os.path.getsize(filename) / 1000, ' kb')
			if os.path.getsize(filename) > 4000000000:
				break
			category_url = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:computer_programming&cmlimit=500&cmtype=page&format=json&rawcontinue"
			category_url = category_url.replace('Category:computer_programming', category).replace(" ", "_")
			cat = requests.get(category_url).json()
			for child in tqdm(cat['query']['categorymembers']):
				page_url = "https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles=computer_programming&redirects=true"
				page_url = page_url.replace('computer_programming', child['title']).replace(" ", "_")
				page = requests.get(page_url)
				text = page.text.replace('&lt;', '<').replace('&gt;', '>')
				soup = bs(text, 'html.parser')
				text = soup.get_text().replace('\n', " ")
				try:
					page_id = soup.find('page').attrs['pageid']
				except Exception as e:
					continue
				outfile.write(page_id + "    PROG    " + ' '.join(wtk(text)) + "\n")

def collect_categories(cat, depth, max_depth):
	url="https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:computer_programming&cmprop=title&cmlimit=500&cmtype=subcat&format=json&rawcontinue"
	url = url.replace('Category:computer_programming', cat).replace(" ", "_")
	print ('depth: ', depth)
	print (cat)
	# if cat == 'Category:4chan phenomena':
	# 	import pdb;pdb.set_trace()
	top= requests.get(url) # download the data from the API
	topdict=top.json()
	children = [x['title'] for x in topdict['query']['categorymembers']]

	if cat in seen:
		return []
	else:
		seen.append(cat)

	if not children:
		return []
	else:
		if depth >= max_depth:
			return children
		else:
			deeper = []
			for child in children:
				deeper = deeper + [member for member in collect_categories(child, depth + 1, max_depth)]
				# print deeper
			return children + deeper

@click.command()
@click.argument('text_file')
# @click.argument('vocab_file')
def main(text_file):
	categories = collect_categories('Category:computer_programming', 0, 5)
	parse(text_file, categories)
	# with open(vocab_file, 'a', encoding='utf-8') as o:
	# 	for key in count.keys():
	# 		o.write(str(count[key]) + " " + key + "\n")

if __name__ == "__main__":

	main()
