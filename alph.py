#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Todo
# Distance

# Config
space_hand = 'r'
termination_symbols = ' ,.?!:;'
finger_symbols = {}

if True:
	finger_symbols['r1'] = 'yhn7ujmYHN/UJM'
	finger_symbols['r2'] = '8ik,9(IK;)'
	finger_symbols['r3'] = '0ol.=OL:'
	finger_symbols['r4'] = '+pø-?PØ_\åæÅÆ*^'
	finger_symbols['l1'] = '6tgb&TGB5rfv%RFV'
	finger_symbols['l2'] = '4edc¤EDC3#'
	finger_symbols['l3'] = '2wsx"WSX'
	finger_symbols['l4'] = '1qaz!QAZ|<§>'
else:
	finger_symbols['r1'] = 'fFdDbB7/gGhHmM'
	finger_symbols['r2'] = '8(cCtTwW9)'
	finger_symbols['r3'] = '0=rRnNvV'
	finger_symbols['r4'] = '+?lLsSzZ\^*-_<>'
	finger_symbols['l1'] = '6&yYiIxX5%pPuUkK'
	finger_symbols['l2'] = '4¤:.eEjJ3#'
	finger_symbols['l3'] = '2",;oOqQ'
	finger_symbols['l4'] = '1!åÅaAæÆøØ|§'

finger_symbols['r0'] = ''
finger_symbols['l0'] = ''
finger_symbols[space_hand + '0'] += ' '

# Counters
char_freq = {}
word_length_freq = {}
hand_freq = {}
hand_length_freq = {}
rolls = {}
for label in ['r', 'l', 'n']:
	hand_freq[label] = 0
	hand_length_freq[label] = {}
	rolls[label] = {}; rolls[label]['in'] = 0; rolls[label]['out'] = 0; rolls[label]['none'] = 0; rolls[label]['short'] = 0
finger_freq = {}
finger_length_freq = {}
for label in ['r1', 'r2', 'r3', 'r4', 'r0', 'l1', 'l2', 'l3', 'l4', 'l0', 'n']:
	finger_freq[label] = 0
	finger_length_freq[label] = {}

# Read file
f = open('input.txt', 'r')
text = f.read();

# Begin
word_length = 0
hand_length = 0
finger_length = 0
roll_buffer = []
hand_current = 'n'
finger_current = 'n'

def dict_increment(*arg):
	dict = arg[0]
	key = arg[-1]
	levels = len(arg) - 2
	current = dict
	for i in range(levels):
		current = current[arg[i + 1]]
	if (key in current):
		current[key] += 1
	else:
		current[key] = 1

def get_finger(char):
	for key in finger_symbols:
		if (c in finger_symbols[key]): return key
	return 'n'

def roll_direction(list):
	if (len(list) < 2):
		return 'short'
	not_out = False
	not_in = False
	for i in range(len(list) - 1):
		if list[i + 1] <= list[i]:
			not_out = True
		if list[i + 1] >= list[i]:
			not_in = True
	if (not_out and not_in):
		return 'none'
	return 'in' if not_out else 'out'

for c in text:
	# Characters and words
	dict_increment(char_freq, c)

	if (c in termination_symbols):
		dict_increment(word_length_freq, word_length)
		word_length = 0
	else:
		word_length += 1

	# Fingers
	finger_new = get_finger(c)
	if (finger_new[0] == 'n'):
		print(c)
	finger_freq[finger_new] += 1
	if (finger_new != finger_current):
		dict_increment(finger_length_freq, finger_current, finger_length)
		finger_current = finger_new
		finger_length = 1
	else:
		finger_length += 1

	# Hands and rolls
	hand_new = finger_new[0]
	hand_freq[hand_new] += 1

	if (hand_new != hand_current or c == ' '):
		if (len(roll_buffer) > 0):
			rolls[hand_current][roll_direction(roll_buffer)] += 1
		if (c == ' ' or hand_new == 'n'):
			roll_buffer = []
		else:
			roll_buffer = [finger_new[1]]
	elif (hand_new != 'n'):
		roll_buffer.append(finger_new[1])

	if (hand_new != hand_current):
		dict_increment(hand_length_freq, hand_current, hand_length)
		hand_current = hand_new
		hand_length = 1
	else:
		hand_length += 1

	finger_current = finger_new
	hand_current = hand_new


print(char_freq)
print()
print(word_length_freq)
print()
print(hand_freq)
print()
print(hand_length_freq)
print()
print(finger_freq)
print()
print(finger_length_freq)
print()
print(rolls)
print()
print()

same_finger_count = 0
for i in finger_length_freq:
	for j in finger_length_freq[i]:
		if j > 1:
			same_finger_count += finger_length_freq[i][j]
print(same_finger_count)




def plot(dict):
	import numpy as np
	import matplotlib.pyplot as plt
	
	plt.bar(range(len(dict)), dict.values(), align='center')
	plt.xticks(range(len(dict)), dict.keys())

	plt.show()

plot(char_freq)
plot(word_length_freq)
"""
hand_freq = {}
hand_length_freq = {}
rolls = {}
"""