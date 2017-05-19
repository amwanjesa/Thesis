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
			try:
				new_line = line.replace('    GENERAL    ', '\tGENERAL\t')
				assert line.index('    GENERAL    ')
			except Exception as e:
				new_line = line.replace('    PROG    ', '\tPROG\t')
				assert line.index('    PROG    ')
			# import pdb; pdb.set_trace()
			o.write(new_line)


if __name__ == "__main__":

	count()
