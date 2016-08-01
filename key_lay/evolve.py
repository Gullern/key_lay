#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# Current language consits of 47 characters
base_characters = "1234567890qwertyuiopåasdfghjkløæzxcvbnm"
special_characters = "|+\¨'<,.-§!`\"#¤%&/()=?^*>;:_@£${}[]"
mutation_prob = 0.02
lambd = 0.5

# Create initial sample
def createSample(base_characters, special_characters, sampleSize):
	for i in xrange(0, sampleSize):
		keyboard = [[None]*13, [None]*13, [None]*12, [None]*12, [None]*12, [None]*12, [None]*12, [None]*12]
		for c in base_characters:
			row = random.randint(0,3)*2
			if(row == 0):
				col = random.randint(0,12)
			else:
				col = random.randint(0,11)
			org_col = col
			while(not (keyboard[row][col] == None)):
				col += 1
				if((row < 0 and col > 11) or col > 12):
					col = 0
				if(col == org_col):
					row += 1
					if(row > 3):
						row = 0
			keyboard[row][col] = c
			if(c.islower()):
				keyboard[row + 1][col] = c.upper()
		for c in special_characters:
			row = random.randint(0,3)*2
			if(row == 0):
				col = random.randint(0,12)
			else:
				col = random.randint(0,11)
			org_col = col
			while(not (keyboard[row][col] == None)):
				col += 1
				if((row < 0 and col > 11) or col > 12):
					col = 0
				if(col == org_col):
					row += 1
					if(row > 3):
						row = 0
			keyboard[row][col] = c
		samples.append(keyboard)
	return samples

	
# Perform optimization through evolution
def optimization(samples, mutation_prob, nr_consecutive):
	generation = list(samples)
	consecutive_best = 0
	max_fitness = 0
	fittest = ""
	# Evolution should continue until the same layout has been the fittest for nr_consecutive generations
	while(consecutive_best < nr_consecutive):
		results = {}
		# Evaluate fitness
		for keyboard in generation:
			fitness = getFitness(keyboard)
			results[keyboard] = fitness
		generation_ranked = sorted(results, key=results.get)
		if(max_fitness == generation_ranked[0]):
			consecutive_best += 1
		elif(max_fitness < generation_ranked[0]):
			max_fitness = generation_ranked[0]
			fittest = best_layout
		generation = createNewGeneration(generation_ranked)
	return fittest

	
# Create new generation.
# Takes in sorted list of current generation
def createNewGeneration(generation):
	new_generation = []
	new_generation.append(generation[0])
	for i in xrange(1, len(generation)):
		sample_1 = generation[random.expovariate(lambd)]
		sample_2 = generation[random.expovariate(lambd)]
		new_sample = combine(sample_1, sample_2)
		new_sample = mutate(new_sample)
		new_generation.append(new_sample)
	return new_generation

def combine(sample_1, sample_2):
	if(sample_1 == sample_2):
		return sample_1
	else:
		new_sample = sample_1
		return None
	
def mutate(sample):
	return None

