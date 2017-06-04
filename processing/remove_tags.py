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
    with open(first, 'r') as r, open(second, 'w') as w:
        for line in tqdm(r):
			try:
				start = line.index('GENERAL\t') + len('GENERAL\t')
			except Exception as e:
				start = line.index('PROG\t') + len('PROG\t')
			w.write(line[start:])

if __name__ == '__main__':
    main()