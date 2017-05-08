from collections import Counter
import click

@click.command()
@click.argument('filename')
def count(filename):
	c = Counter()
	for line in data.splitlines():
	    c.update(line.split())
	print(c)