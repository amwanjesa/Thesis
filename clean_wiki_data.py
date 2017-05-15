from collections import Counter
import click
from nltk.tokenize import word_tokenize as wtk
from tqdm import tqdm

@click.command()
@click.argument('input_file')
@click.argument('output_file')
def count(input_file, output_file):
	id_count = 0
	with open(input_file, 'r', encoding='utf-8') as i, open(output_file, 'w', encoding='utf-8') as o:
		for line in tqdm(i):
			new_line = '\t'.join(line.split())
			o.write(new_line + ' \n')
	# with open(output_file, 'w', encoding='utf-8') as o:
	# 	for c in counter.most_common():
	# 		o.write(str(c[1]) + " " + c[0] + "\n")


if __name__ == "__main__":

	count()
