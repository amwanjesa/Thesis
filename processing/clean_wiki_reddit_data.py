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
			if id_count in [323435, 666837, 695618, 697198, 831479, 963642, 1174660, 1246814, 1267846, 1348906, 1506175, 1542296, 1595709, 1681743, 1892157]:
				import pdb; pdb.set_trace()
				id_count +=1
				continue
			# assert line != ''
			# try:
			# 	index = line.index('\tGENERAL\t')
			# except Exception as e:
			# 	index = line.index('\tPROG\t')
			# new_line = str(id_count) + line[index:]
			id_count += 1
			o.write(line)
			# try:
			# 	new_line = line.replace('    GENERAL    ', '\tGENERAL\t')
			# 	assert line.index('    GENERAL    ')
			# except Exception as e:
			# 	new_line = line.replace('    PROG    ', '\tPROG\t')
			# 	assert line.index('    PROG    ')
			# # import pdb; pdb.set_trace()
			# o.write(new_line)


if __name__ == "__main__":

	count()
