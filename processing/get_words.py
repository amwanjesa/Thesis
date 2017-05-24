import csv
import numpy as np 
from tqdm import tqdm
import operator
from scipy import spatial
import click
import json

@click.command()
@click.argument('word_file')
@click.argument('output_file')
def main(word_file, output_file):
    with open(word_file, 'r') as w, open(output_file, 'w') as out:
        count = 0
        lines = w.readlines()[1:]
        interval = len(lines) / 3
        main_lines = lines[:interval]
        for i, line in tqdm(enumerate(main_lines)):
            word = line.split()[1]
            out.write(word + '\n' )

if __name__ == '__main__':
    main()