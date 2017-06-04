import csv
import numpy as np 
from tqdm import tqdm
import operator
from scipy import stats
import click
import json


@click.command()
@click.argument('first')
@click.argument('second')
def main(first, second):
    with open(first, 'r') as w, open(second, 'r')  as r:
		wiki_lines = [word.split()[0] for word in w.readlines()]
		reddit_lines = [word.split()[0] for word in r.readlines()]
		diff = len(wiki_lines) - len(reddit_lines)
		reddit_lines += [None] * diff
		wiki = range(len(wiki_lines))
		reddit = []
		for word in tqdm(reddit_lines):
			try:
				reddit.append(wiki_lines.index(word))
			except:
				reddit.append(-1)
		print (stats.pearsonr(wiki, reddit))

if __name__ == '__main__':
    main()