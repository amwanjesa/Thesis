import numpy as np 
import click 
from tqdm import tqdm
from scipy import spatial
import operator
import pickle

PROG_matrix = 0
GENERAL_matrix = 0

@click.command()
@click.argument('vector_file')
@click.argument('dist_file')
def compute_distances(vector_file, dist_file):
    context_dist = {}
    with open(vector_file, 'r') as ifile:
        count = 0
        lines = ifile.readlines()[1:]
        interval = int(len(lines) / 3)
        main_lines = lines[:interval]
        for i, line in tqdm(enumerate(main_lines)):
            main = line.split()
            prog = lines[i + interval].split()
            general = lines[i + interval * 2].split()

            main_vec = np.array([float(value) for value in main[2:]])
            prog_vec = np.array([float(value) for value in prog[2:]])
            general_vec = np.array([float(value) for value in general[2:]])

            general_vec = np.add(main_vec, general_vec)
            prog_vec = np.add(main_vec, prog_vec)
            dist = 1 - spatial.distance.cosine(general_vec, prog_vec)
            context_dist[main[1]] = dist

    with open(dist_file, 'w') as ofile:
        sorted_dist = sorted(context_dist.items(), key=operator.itemgetter(1))
        for word in sorted_dist:
            ofile.write(word[0] + '\t' + str(context_dist[word[0]]) + '\n')

if __name__ == '__main__':
    compute_distances()