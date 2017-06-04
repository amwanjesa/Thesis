import click
from tqdm import tqdm

@click.command()
@click.argument('original')
@click.argument('general')
@click.argument('prog')
def separate(original, general, prog):
    with open(original, 'r', encoding='utf-8') as og, open(general, 'w', encoding='utf-8') as n1, open(prog, 'w', encoding='utf-8') as n2:
        for line in tqdm(og):
            if '\tPROG\t' in line:
                n2.write(line)
            elif '\tGENERAL\t' in line:
                n1.write(line)
            else:
                continue
                


if __name__ == '__main__':
    separate()