#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math
import sys
import numpy as np

class keyEvolver:
	
	def __init__(self, base_characters, special_characters, sample_size, mutation_lambda, select_lambda, row_sizes, nr_consecutive):
		self._base_characters = base_characters
		self._special_characters = special_characters
		self._sample_size = sample_size
		self._mutation_lambda = mutation_lambda
		self._select_lambda = select_lambda
		self._row_sizes = row_sizes
		self._nr_consecutive = nr_consecutive
		
		
	def evolve(self):
		start_samples = self._createSample()
		return self._optimize(start_samples)

		
	# Create initial sample base
	def _createSample(self):
		samples = []
		# For each sample
		for i in xrange(0, self._sample_size):
			# Create empty sample keyboard
			keyboard = []
			for i in xrange(0, len(self._row_sizes)):
				keyboard.append([None]*self._row_sizes[i])
				keyboard.append([None]*self._row_sizes[i])
			
			# Create randomized list of special characters
			special_chars = list(self._special_characters)
			random.shuffle(special_chars)
			
			# Create randomized lists of base spots and shifted spots
			base_spots = [(row, col) for row in xrange(0, len(self._row_sizes)*2, 2) for col in xrange(self._row_sizes[row/2])]
			shift_spots = [(row, col) for row in xrange(1, len(self._row_sizes)*2, 2) for col in xrange(self._row_sizes[row/2])]
			random.shuffle(base_spots)
			random.shuffle(shift_spots)
			
			# For all base characters, select a random base spot. If the base character is alfabetic assign the upper case version to the same shift spot
			for c in self._base_characters:
				spot = base_spots.pop()
				keyboard[spot[0]][spot[1]] = c
				if(c.islower()):
					shift_spots.remove((spot[0] + 1, spot[1]))
					keyboard[spot[0] + 1][spot[1]] = c.upper()

			# While there are still room on keyboard, select a random special character and assign it to location. First fill out base spots, then shift spots
			while(base_spots or shift_spots):
				c = special_chars.pop()
				if(base_spots):
					spot = base_spots.pop()
				else:
					spot = shift_spots.pop()
				keyboard[spot[0]][spot[1]] = c
			
			samples.append(keyboard)
		return samples

	
	# Perform optimization through evolution
	def _optimize(self, samples):
		generation = list(samples)
		consecutive_best = 0
		best_fitness = 100000
		fittest = []
		
		# Evolution should continue until the same layout has been the fittest for _nr_consecutive generations
		while(consecutive_best < self._nr_consecutive):
			results = {}
			
			# Evaluate fitness for all samples in generation
			i = 0
			for keyboard in generation:
				fitness = getFitness(keyboard)
				results[i] = fitness
				i += 1
			
			# Sort generation based on fittnes
			generation_ranked = []
			ranked_results = sorted(results, key=results.get)
			for i in ranked_results:
				generation_ranked.append(generation[i])
			
			# If the fitness is unchanged since last generation, increment consecutive_best, else reset consecutive counter
			if(best_fitness == results[ranked_results[0]]):
				consecutive_best += 1
			elif(best_fitness > results[ranked_results[0]]):
				best_fitness = results[ranked_results[0]]
				fittest = generation_ranked[0]
				consecutive_best = 0
				
			# Create new generation
			generation = self._createNewGeneration(generation_ranked)
			
		return fittest

	
	# Create new generation.
	# Takes in sorted list of current generation
	def _createNewGeneration(self, generation):
		
		# Transfer the 10% best samples directly to next generation
		new_generation = list(generation[:len(generation)/10])
		
		# Create new samples until the number of samples in new generation is the same as previous generation
		for i in xrange(len(generation)/10, len(generation)):
			
			# Select two random samples to "breed". Samples are selected from exponential distribution, increasing probability of selecting fitter samples
			sample_1 = generation[int(random.expovariate(self._select_lambda))]
			sample_2 = generation[int(random.expovariate(self._select_lambda))]
			
			# Combine samples to new sample, mutate, and add to new generation
			new_sample = self._combine(sample_1, sample_2)
			new_sample = self._mutate(new_sample)
			new_generation.append(new_sample)
		
		return new_generation

		
	# Combines two samples to a new sample
	def _combine(self, sample_1, sample_2):
		
		# If the two samples are the same, return unchanged
		if(sample_1 == sample_2):
			return list(sample_1)
			
		# Else create new sample by comining the two samples given
		else:
			new_sample = [[None]*i for i in self._row_sizes for _ in (0, 1)]
			observed = set()
			base_spots = [(row, col) for row in xrange(0, len(self._row_sizes)*2, 2) for col in xrange(self._row_sizes[row/2])]
			shift_spots = [(row, col) for row in xrange(1, len(self._row_sizes)*2, 2) for col in xrange(self._row_sizes[row/2])]
			
			# Fill new sample by comining base characters from right half of sample_1 and left half of sample_2
			for i in xrange(0, len(new_sample), 2):
				for j in xrange(0, len(new_sample[i])):
					if(j < len(new_sample[i])/2):
						c = sample_1[i][j]
					else:
						c = sample_2[i][j]
					if(c in self._base_characters):
						if(c not in observed):
							new_sample[i][j] = c
							base_spots.remove((i, j))
							if(c.islower()):
								new_sample[i + 1][j] = c.upper()
								shift_spots.remove((i + 1, j))
							observed.add(c)
			
			# Find unused base characters
			unused_base_chars = [i for i in self._base_characters if i not in observed]
			
			# Place unused base characters on free base spots
			for c in unused_base_chars:
				spot = base_spots.pop()
				new_sample[spot[0]][spot[1]] = c
				if(c.islower()):
					new_sample[spot[0] + 1][spot[1]] = c.upper()
					shift_spots.remove((spot[0] + 1, spot[1]))
			
			# Place shift characters from right half og sample_1 and left half of sample_2
			for i in xrange(0, len(new_sample)):
				for j in xrange(0, len(new_sample[i])):
					if(j < len(new_sample[i])/2):
						c = sample_1[i][j]
					else:
						c = sample_2[i][j]
					if(c and c in self._special_characters):
						if(c not in observed):
							if(i % 2 == 0):
								if((i, j) in base_spots):
									new_sample[i][j] = c
									observed.add(c)
									base_spots.remove((i, j))
							else:
								if((i + 1, j) in shift_spots):
									new_sample[i][j] = c
									observed.add(c)
									shift_spots.remove((i + 1, j))
				
			# Find unused shift characters
			unused_special_chars = [i for i in self._special_characters if i not in observed]
			random.shuffle(unused_special_chars)
			
			# Fill remaining spots with unused shift characters
			while(base_spots or shift_spots):
				c = unused_special_chars.pop()
				if(base_spots):
					spot = base_spots.pop()
				else:
					spot = shift_spots.pop()
				new_sample[spot[0]][spot[1]] = c
			
			return new_sample
			
		
	# Perform random mutation on a sample
	def _mutate(self, sample):
		# Randomly select number of mutations from poisson distribution with _mutation_lambda
		nr_mutations = int(np.random.poisson(self._mutation_lambda))
		
		# Perform the selected number of mutations
		for i in xrange(0, nr_mutations):
		
			# Randomly select a location to mutate
			row = random.randint(0, len(sample) - 1)
			col = random.randint(0, len(sample[row]) - 1)
			c = sample[row][col]
			if(c.isupper()):
				row -= 1
				c = c.lower()
			
			# If the selected character is a base character, swap with another character on base location
			if(c in self._base_characters):
				swap_row = random.randint(0, len(self._row_sizes) - 1)*2
				swap_col = random.randint(0, self._row_sizes[swap_row/2] - 1)
				temp = (sample[row][col], sample[row + 1][col])
				sample[row][col] = sample[swap_row][swap_col]
				sample[row + 1][col] = sample[swap_row + 1][swap_col]
				sample[swap_row][swap_col] = temp[0]
				sample[swap_row + 1][swap_col] = temp[1]
			
			# Else, replace character with another character from special_characters
			else:
				new_char = random.choice(self._special_characters)
				if(any(new_char in x for x in sample)):
					swap = self._getPosition(new_char, sample)
					swap_row = swap[0]
					swap_col = swap[1]
					sample[swap_row][swap_col] = c
				sample[row][col] = new_char
				
		return sample
		
		
	def _getPosition(self, char, keyboard):
		for i in xrange(0, len(keyboard)):
			if(char in keyboard[i]):
				return (i, keyboard[i].index(char))
		return None
		
def printKeyboard(keyboard):
	for i in keyboard:
		for j in i:
			print j,
		print
	print
		
def getFitness(sample):
	return 1;

def main():
	# Current language consits of 47 characters
	base_characters = unicode("1234567890qwertyuiopasdfghjklzxcvbnmæøå", "utf-8")
	special_characters = unicode("|+\\¨'<,.-§!`\"#¤%&/()=?^*>;:_@£${}[]", "utf-8")
	select_lambda = 0.75
	row_sizes = [13, 12, 12, 11]
	sample_size = 10
	mutation_lambda = 2
	nr_consecutive = 4
	evolver = keyEvolver(base_characters, special_characters, sample_size, mutation_lambda, select_lambda, row_sizes, nr_consecutive)
	optimal = evolver.evolve()
	printKeyboard(optimal)
	
main()
