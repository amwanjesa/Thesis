import xml.etree.ElementTree as ET
import click
import requests  # http://docs.python-requests.org/en/latest/
import json
import itertools
import warnings
import sys
from nltk.tokenize.moses import MosesTokenizer

warnings.filterwarnings('ignore')
supers = ['computers', 'software_development', 'software_engineering', 'culture', 'outer_space', 'society', 'nature', 'science']
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

	with open(filename, mode) as outfile:
		for category in topdict['query']['categorymembers']:
			category_url = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Computer_programming&cmlimit=500&cmtype=page&format=json&rawcontinue"
			category_url.replace('computer_programming', category['title'].replace(" ", "_"))
			cat = requests.get(category_url).json()
			for child in cat['query']['categorymembers']:
				page_url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=computer_programming"
				page_url.replace('computer_programming', child['title'].replace(" ", "_"))
				page = requests.get(page_url).json()
				page_id = str(child['pageid'])
				page_text = page['query']['pages']['5311']['revisions'][0]['*']
				for symbol in ['[', '>', '<', '[', '=', '}', '{', ']', '|', '#', '\n', '\r', "\'", "*", "(", ")", ","]:
					if symbol in ['*', '\r', '/', ':', '\'', ',']:
						page_text = page_text.replace(symbol, " ")
					else:
						page_text = page_text.replace(symbol, "")
				if supers.index(sum_cat) > 2:
					outfile.write(page_id + "    GENERAL    " + page_text + "    " + page_url + "\n")
				else:
					outfile.write(page_id + "    PROG    " + page_text + "    " + page_url + "\n")


@click.command()
@click.argument('filename')
def main(filename):
	for cat in supers:
		parse(filename, cat)


if __name__ == "__main__":

	main()

