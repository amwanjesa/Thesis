from collections import Counter
import click
from nltk.tokenize import word_tokenize as wtk
from tqdm import tqdm
import numpy as np
import math
import json
import operator


tf_idf = {}
@click.command()
@click.argument('vocab_file')
@click.argument('output_file')
def count(vocab_file, output_file):
	vocab = {}
	with open(vocab_file, 'r', encoding='utf-8') as v:
		for line in v.readlines():
			entry = line.split()
			vocab[entry[1]] = float(entry[0])
		

		total_tokens = sum(vocab.values())
		for key, value in tqdm(vocab.items()):
			vocab[key] = value / total_tokens
		
		maximum = max(vocab.values())
		for key, value in tqdm(vocab.items()):
			vocab[key] = value / maximum
		
		vals = list(vocab.values())
		rf = np.array(vals, dtype=float)
		import pdb; pdb.set_trace()
	with open(output_file, 'w', encoding='utf-8') as o:
		json.dump(vocab, o)

if __name__ == "__main__":
	count()
