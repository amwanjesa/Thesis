# -*- encoding: utf-8 -*-
import xml.etree.ElementTree as ET
import click
import requests  # http://docs.python-requests.org/en/latest/
import json
import itertools
import warnings
import sys
from collections import Counter
from nltk.tokenize import word_tokenize as wtk
from bs4 import BeautifulSoup as bs

count = Counter()
warnings.filterwarnings('ignore')
supers = ['computers', 'software_development', 'software_engineering'] #'culture', 'outer_space', 'society', 'nature', 'science']
# get the subcategories of the top wikipedia category "Alles"
url="https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Computer_programming&cmprop=title&cmlimit=500&cmtype=subcat&format=json&rawcontinue"

def parse(filename, sum_cat):
	print (sum_cat)
	url.replace('computer_programming', sum_cat)
	top= requests.get(url) # download the data from the API
	topdict=top.json()

	if supers.index(sum_cat) == 0:
		mode = 'w'
	else:
		mode = 'a'

	with open(filename, mode,  encoding='utf-8') as outfile:
		for category in topdict['query']['categorymembers']:
			category_url = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Computer_programming&cmlimit=500&cmtype=page&format=json&rawcontinue"
			category_url.replace('computer_programming', category['title'].replace(" ", "_"))
			cat = requests.get(category_url).json()
			for child in cat['query']['categorymembers']:
				page_url = "https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles=computer_programming&redirects=true"
				page_url = page_url.replace('computer_programming', child['title']).replace(" ", "_")
				# import pdb;pdb.set_trace()
				page = requests.get(page_url)
				text = page.text.replace('&lt;', '<').replace('&gt;', '>')
				soup = bs(text, 'html.parser')
				text = soup.get_text().replace('\n', " ")
				page_id = soup.find('page').attrs['pageid']
				count.update(wtk(text))
				if supers.index(sum_cat) > 2:
					outfile.write(page_id + "    GENERAL    " + text + "    " + page_url + "\n")
				else:
					outfile.write(page_id + "    PROG    " + text + "    " + page_url + "\n")


@click.command()
@click.argument('filename')
@click.argument('output_file')
def main(filename, output_file):
	for cat in supers:
		parse(filename, cat)
	with open(output_file, 'a', encoding='utf-8') as o:
		for key in count.keys():
			o.write(str(count[key]) + " " + key + "\n")

if __name__ == "__main__":

	main()

