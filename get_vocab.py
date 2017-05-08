from collections import Counter
import click

@click.command()
@click.argument('input_file')
@click.argument('output_file')
def count(input_file, output_file):
	count = Counter()
	with open(input_file, 'r') as f:
		for line in f:
			count.update(line.split())
	with open(output_file, 'a') as o:
		for key in count.keys():
			o.write(str(count[key]) + " " + key + "\n")

if __name__ == "__main__":

	count()