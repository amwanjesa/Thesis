import csv
import numpy as np 
from tqdm import tqdm
import operator
from scipy import spatial
import click
import json

@click.command()
@click.argument('general_file')
@click.argument('prog_file')
@click.argument('word_file')
@click.argument('output_file')
def main(general_file, prog_file, word_file, output_file):
    with open(general_file, 'r', encoding='utf-8') as g, open(prog_file, 'r', encoding='utf-8') as p, open(word_file, 'r', encoding='utf-8') as w, open(output_file, 'w', encoding='utf-8') as out:
        words = [x.replace('\n', '') for x in w.readlines()]
        prog_reader = csv.reader(p, delimiter=',')
        results = {}
        for prog_index, prog_vec in tqdm(enumerate(prog_reader)):
            word_dist = []
            gen_reader = csv.reader(g, delimiter=',')
            prog_vec = np.array([prog_vec], dtype=float) 
            prog_vec = prog_vec / np.linalg.norm(prog_vec)

            for gen_index, gen_vec in tqdm(enumerate(gen_reader)):
                gen_vec = np.array([gen_vec], dtype=float)
                gen_vec = gen_vec / np.linalg.norm(gen_vec)
                dist = 1 - spatial.distance.cosine(gen_vec, prog_vec)
                word_dist.append((words[gen_index], abs(dist)))
            
            g.seek(0)
            word_dist.sort(key=lambda tup: tup[1])
            closest_words = [word for (word, k) in word_dist[:15]]

            if not closest_words:
                import pdb; pdb.set_trace()
            results[words[prog_index]] = closest_words

        json.dump(results, out)

if __name__ == '__main__':
    main()