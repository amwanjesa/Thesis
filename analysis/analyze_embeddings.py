import pandas as pd 
import numpy as np 
import click 
from tqdm import tqdm

PROG_matrix = 0
GENERAL_matrix = 0

@click.command()
@click.argument('vector_file')
def separate_vectors(vector_file):
    seen = []
    dfs= []
    with open(vector_file, 'r') as ifile:
        count = 0
        categories = {}
        for line in tqdm(ifile):
            if count == 0:
                count += 1
                continue
            parts = line.split()
            values = np.array([float(value) for value in parts[2:]])
            if parts[0] in categories.keys():
                vector = categories[parts[0]]
                categories[parts[0]] = np.vstack((vector, values))
            else:
                categories[parts[0]] = values
        import pdb; pdb.set_trace()
        PROG_matrix = np.add(categories['MAIN'], categories['PROG'])
        GENERAL_matrix = np.add(categories['MAIN'], categories['GENERAL'])

if __name__ == '__main__':
    separate_vectors()