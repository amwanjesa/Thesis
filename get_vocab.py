from collections import Counter
import click
from nltk.tokenize import word_tokenize as wtk

@click.command()
@click.argument('input_file')
@click.argument('output_file')
def count(input_file, output_file):
	with open(input_file, 'r', encoding='utf-8') as i, open(output_file, 'a', encoding='utf-8') as o:
		for line in i:
			end = line.index('    https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles=')
			o.write(line[:end])

	# with open(output_file, 'a', encoding='utf-8') as o:
	# 	for key in count.keys():
	# 		o.write(str(count[key]) + " " + key + "\n")

if __name__ == "__main__":

	count()