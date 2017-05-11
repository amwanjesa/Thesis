from collections import Counter
import click
from nltk.tokenize import word_tokenize as wtk

counter = Counter()
@click.command()
@click.argument('input_file')
@click.argument('output_file')
def count(input_file, output_file):
	with open(input_file, 'r', encoding='utf-8') as i:
		for line in i:
			try:
				start = line.index('GENERAL    ') + len('GENERAL    ')
			except Exception as e:
				start = line.index('PROG    ') + len('PROG    ')
			counter.update(line[start:].lower().split())
			# import pdb;pdb.set_trace()

	with open(output_file, 'a', encoding='utf-8') as o:
		for c in counter.most_common():
			o.write(str(c[1]) + " " + c[0] + "\n")

if __name__ == "__main__":

	count()
