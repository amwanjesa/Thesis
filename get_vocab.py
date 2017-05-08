from collections import Counter
import click

@click.command()
@click.argument('filename')
def count(filename):
	count = Counter()
	with open(filename, 'r') as f:
		for line in f:
			count.update(line.split())
	import pdb;pdb.set_trace()
	print(count)

if __name__ == "__main__":

	count()