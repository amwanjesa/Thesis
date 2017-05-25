from collections import Counter
import click
from nltk.tokenize import word_tokenize as wtk
from tqdm import tqdm
import mmap
from itertools import dropwhile

counter = Counter()
@click.command()
@click.argument('input_file')
@click.argument('general')
@click.argument('prog')
@click.argument('output_file')
def count(input_file, general, prog, output_file):
	with open(input_file, 'r', encoding='utf-8') as i:
		for line in tqdm(i):
			try:
				start = line.index('GENERAL\t') + len('GENERAL\t')
			except Exception as e:
				start = line.index('PROG\t') + len('PROG\t')
			counter.update(line[start:].lower().split())
	
	for key, count in dropwhile(lambda key_count: key_count[1] >= 100, counter.most_common()):
		del counter[key]
	with open(output_file, 'w', encoding='utf-8') as o:
		for c in tqdm(counter.most_common()):
			if checkForWord([general, prog], c[0]):
				o.write(str(c[1]) + '\t' + c[0] + "\n")
			else:
				print (c[0])
				continue

def checkForWord(files, word):
	flags = [False, False] 
	for i, source in enumerate(files):
		with open(source, 'r', encoding='utf-8') as f:
			data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
			flags[i] = data.find(str.encode(word)) != 1
	return flags[0] and flags[1]
if __name__ == "__main__":

	count()
