# -*- encoding: utf-8 -*-
import xml.etree.ElementTree as ET
import click
import requests  # http://docs.python-requests.org/en/latest/
import json
import itertools
import warnings
import sys
import os
from random import randint
from collections import Counter
from nltk.tokenize import word_tokenize as wtk
from bs4 import BeautifulSoup as bs

seen = []
count = Counter()
warnings.filterwarnings('ignore')
supers = ['computers', 'software_development', 'software_engineering', 'algorithms', 'computer_programmers', 'programming_languages', 'debugging'] #'culture', 'outer_space', 'society', 'nature', 'science']
# get the subcategories of the top wikipedia category "Alles"
url="https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Computer_programming&cmprop=title&cmlimit=500&cmtype=subcat&format=json&rawcontinue"

def parse(title):
	print (title)
	page_url = "https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles=computer_programming&redirects=true"
	page_url = page_url.replace('computer_programming', title).replace(" ", "_")
	page = requests.get(page_url)
	
	text = page.text.replace('&lt;', '<').replace('&gt;', '>')
	soup = bs(text, 'html.parser')
	text = soup.get_text().replace('\n', " ")
	try:
		page_id = soup.find('page').attrs['pageid']
	except Exception as e:
		return
	
	count.update(wtk(text))
	return page_id + "    GENERAL    " + text + "    " + page_url + "\n"




@click.command()
@click.argument('title_file')
@click.argument('wiki_file')
@click.argument('vocab_file')
def main(title_file, wiki_file, vocab_file):
	with open(title_file, 'r', encoding='utf-8') as i:
		lines = i.readlines()

	with open(wiki_file, 'a',  encoding='utf-8') as outfile:
		while os.path.getsize(wiki_file) < 400000000:
			index = randint(0, len(lines) - 1)
			if index in seen:
				continue
			else:
				seen.append(index)
			title = lines[index].split()[1]
			page = parse(title)
			if page is None:
				continue
			else:
				outfile.write(page)

	with open(output_file, 'a', encoding='utf-8') as o:
		for key in count.keys():
			o.write(str(count[key]) + " " + key + "\n")

if __name__ == "__main__":

	main()

