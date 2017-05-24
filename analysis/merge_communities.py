import numpy as np 
import click 
from tqdm import tqdm
from scipy import spatial
import operator
import pickle
import csv

PROG_matrix = 0
GENERAL_matrix = 0

@click.command()
@click.argument('vector_file')
@click.argument('community')
@click.argument('word_file')
@click.argument('matrix_csv')
def merge_spaces(vector_file, community, word_file, matrix_csv):
    context_dist = {}
    communities = ['PROG', 'GENERAL']
    com = communities.index(community.upper()) + 1
    
    with open(vector_file, 'r') as ifile, open(matrix_csv, 'w') as m:
        count = 0
        lines = ifile.readlines()[1:]
        interval = len(lines) / 3
        words = []
        writer = csv.writer(m)
        for i, line in tqdm(enumerate(lines[:interval])):
            main = line.split()
            community = lines[i + interval * com].split()

            main_vec = np.array([float(value) for value in main[2:]])
            community_vec = np.array([float(value) for value in community[2:]])
            print (main_vec)
            print(community_vec)
            community_vec = np.add(main_vec, community_vec)
            print(community_vec)
            words.append(main[1])
            if main[1] == 'edinson':
                import pdb; pdb.set_trace()
            writer.writerow(community_vec.tolist())
    
    with open(word_file, 'w') as w:
        w.write('\n'.join(words))

if __name__ == '__main__':
    merge_spaces()