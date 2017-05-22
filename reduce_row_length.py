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
				start = line.index('GENERAL    ') + len('GENERAL    ')
			except Exception as e:
				start = line.index('PROG    ') + len('PROG    ')
			tokens = line[start:].split(' ')

			if len(tokens) > 30:
				chunks, chunk_size = len(tokens), len(tokens) // 30
			else:
				chunks, chunk_size = len(tokens), 30
			for i in range(0, chunks, chunk_size):
				# if i == 11940:
				# 	import pdb; pdb.set_trace()
				# print(i), print (len(tokens))
				if 'GENERAL    ' in line:
					o.write(str(id_count) + '    GENERAL    ' + ' '.join(tokens[i:i+chunk_size]) + '\n')
				else:
					o.write(str(id_count) + '    PROG    ' + ' '.join(tokens[i:i+chunk_size]) + '\n')
				id_count = id_count + 1

	# with open(output_file, 'w', encoding='utf-8') as o:
	# 	for c in counter.most_common():
	# 		o.write(str(c[1]) + " " + c[0] + "\n")


if __name__ == "__main__":

	count()
