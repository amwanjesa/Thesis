"""
Load up the learned word embeddings in sys.argv[1] in memory; for a given search term q, find the 10 closest terms to q in each of the 51 states.

"""

import sys,math,operator

import numpy as np
from numpy import linalg as LA
import json


def get_embeddings(word, embeddings):
	word_emb = dict()
	for n in sorted(embeddings):
		if word in embeddings[n]:
			word_emb[n] = embeddings[n][word]
	return word_emb


def find(word, data, name, output_file):
	print ("Finding: %s in %s" % (word, name))
	scores={}
	if word not in data:
		print ("%s not in vocab" % word)
		return

	a=data[word]
	for word2 in data:
		try:
			score=np.inner(a, data[word2])
			scores[word2]=score
		except:
			pass

	sorted_x = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

	with open(output_file, 'a') as out:
		results = {word + '_' + name: sorted_x[:20]}
		json.dump(results, out)
		out.write('\n')

	for i in range(10):
		(k,v) = sorted_x[i]
		print ("%s\t%.3f" % (k,v))
	print ("")

def find_translation(word, vector, data, name, label, output_file):
	print ("Finding: %s from %s in %s" % (word, label, name))
	scores={}
	if word not in data:
		print ("%s not in vocab" % word)
		return
	
	# Vector of query word is now from the complement community of name and data. 
	a=vector
	for word2 in data:
		try:
			score=np.inner(a, data[word2])
			scores[word2]=score
		except:
			pass

	sorted_x = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

	with open(output_file, 'a') as out:
		results = {word + '_' + label + '_' + name: sorted_x[:20]}
		json.dump(results, out)
		out.write('\n')

	for i in range(10):
		(k,v) = sorted_x[i]
		print ("%s\t%.3f" % (k,v))
	print ("")

# find closest terms for all states
def bigfind(word, embeddings, output_file):
	for n in sorted(embeddings):
		print('Finding neigbors inside own community')

		# Neighbors inside community
		find(word, embeddings[n], n, output_file)

		print('Finding translation in different community')
		# Take the complement of the communty chosed: so if n is GENERAL, takes the complement -> ['PROG']
		complement = list(set(sorted(embeddings.keys())) - set([n]))


		try:
			# Provide the vectgor for the complement; so for dog this is the vecto dog in PROG communty if n is GENERAL
			find_translation(word, embeddings[complement[0]][word], embeddings[n], n, complement[0], output_file)
			print('\n\n')
		except KeyError:
			print ("%s not in vocab" % word)

# normalize vectors for faster cosine similarity calculation
def normalize(embeddings):
	for name in embeddings:
		for word in embeddings[name]:
			a=embeddings[name][word]
			norm=LA.norm(a, 2)

			a /= norm	
			embeddings[name][word]=a

# get all active facets in embeddings
def getFacets(filename):
	file=open(filename)
	facets={}
	for i, line in enumerate(file):
		if i == 0:
			continue
		cols=line.rstrip().split(" ")
		facets[cols[0]]=1
	file.close()

	# don't count the base facet
	del facets["MAIN"]

	return facets.keys()

def process(filename, output_file):
	file=open(filename)

	embeddings={}

	facets=getFacets(filename)

	# if you want to only consider a few metadata facets and not all 51 states, do that here.  e.g.:
	# facets=["MA", "PA"]
	# facets = facets + ['MAIN']
	for facet in facets:
		embeddings[facet]={}

	for line in file:
		line = line.replace(',','.')
		cols=line.rstrip().split(" ")
		if len(cols) < 10:
			continue

		facet=cols[0]

		if facet != "MAIN" and facet not in embeddings:
			continue

		word=cols[1]
		vals=cols[2:]
		a=np.array(vals, dtype=float)
		size=len(vals)

		## 
		# State embeddings for a word = the MAIN embedding for that word *plus* the state-specific deviation
		# e.g.
		# "wicked" in MA = wicked/MAIN + wicked/MA
		##

		if facet == "MAIN":
			for n in embeddings:
				if word not in embeddings[n]:
					embeddings[n][word]=np.zeros(size)
				
				embeddings[n][word]+=a

		else:
			if word not in embeddings[facet]:
				embeddings[facet][word]=np.zeros(size)
				
			embeddings[facet][word]+=a
		
	file.close()

	normalize(embeddings)

	print ("query (ctrl-c to quit): ")
	line = sys.stdin.readline()
	while line:
		word=line.rstrip()
		print (word)
		bigfind(word, embeddings, output_file)
		print ("query (ctrl-c to quit): ")
		line = sys.stdin.readline()

if __name__ == "__main__":
	process(sys.argv[1], sys.argv[2])
