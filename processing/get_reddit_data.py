# -*- encoding: utf-8 -*-
from collections import Counter
import click
import json
import os
from nltk.tokenize import word_tokenize as wtk
from ast import literal_eval as le
from tqdm import tqdm

@click.command()
@click.argument('folder')
@click.argument('output_file')
@click.argument('user_file')
def clean(folder, output_file, user_file):
    for original in tqdm(os.listdir(folder)):
        print (original)
        with open(folder + original, 'r',  encoding='utf-8') as og, open(output_file, 'a',  encoding='utf-8') as new, open(user_file, 'a',  encoding='utf-8') as users:
            for line in og:
                if os.path.getsize(folder + original) < 4000000000:
                    json_string = le(line)
                    try:
                        text = json_string['title']
                    except Exception as e:
                        text = json_string['body']
                    post_id = json_string['id']
                    user = json_string['author']

                    new.write(post_id + "\tPROG\t" + ' '.join(wtk(text.replace('\n', ' '))) + "\n")
                    if user is None:
                        user = ''
                    users.write(user + '\n')
                else:
                    return

if __name__ == '__main__':
        clean()
