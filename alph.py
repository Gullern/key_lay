#!/usr/bin/env python
# -*- coding: utf-8 -*-

######## Todo #########
# - Distance
# - Bad sequences
# - Double letter
#######################

# Imports
from itertools import compress


# Config
space_hand = 'r'
termination_symbols = ' ,.?!:;'
physical_finger_placement = {
                             'l4': ('1100000000000', '100000000000', '100000000000', '11000000000'),
                             'l3': ('0010000000000', '010000000000', '010000000000', '00100000000'),
                             'l2': ('0001100000000', '001000000000', '001000000000', '00010000000'),
                             'l1': ('0000011000000', '000110000000', '000110000000', '00001100000'),
                             'r1': ('0000000100000', '000001100000', '000001100000', '00000011000'),
                             'r2': ('0000000011000', '000000010000', '000000010000', '00000000100'),
                             'r3': ('0000000000100', '000000001000', '000000001000', '00000000010'),
                             'r4': ('0000000000011', '000000000111', '000000000111', '00000000001'),
                             'l0': (),
                             'r0': (),
                             'n':  ()
                            }


# Languages
languages = {
             'qwerty': '|1234567890+\§!"#¤%&/()=?`qwertyuiopå¨QWERTYUIOPÅ^asdfghjkløæ\'ASDFGHJKLØÆ*<zxcvbnm,.->ZXCVBNM;:_',
             'dvorak': '|1234567890+\§!"#¤%&/()=?`å,.pyfgcrl\'¨Å;:PYFGCRL*^aoeuidhtns-<AOEUIDHTNS_>øæqjkxbmwvzØÆQJKXBMWVZ'
            }

def load_finger_symbols(languages):
    get_mask = lambda key: (int(character) for character in ''.join(element * 2 for element in physical_finger_placement[key]))
    finger_symbols = {language: {key: ''.join(compress(languages[language], get_mask(key))) for key in physical_finger_placement} for language in languages}
    for language in finger_symbols:
        finger_symbols[language][space_hand + '0'] += ' '

finger_symbols = load_finger_symbols(languages)

# Counters
counters = {language: {
                       'char_freq': {},
                       'word_length_freq': {},
                       'hand_freq': {finger[0]: 0 for finger in physical_finger_placement},
                       'hand_cont_length_freq': {finger[0]: {} for finger in physical_finger_placement},
                       'finger_freq': {finger: 0 for finger in physical_finger_placement},
                       'finger_cont_length_freq': {finger: {} for finger in physical_finger_placement},
                       'rolls': {finger[0]: {'in': 0, 'out': 0, 'short': 0, 'mixed': 0} for finger in physical_finger_placement}
                       }
            for language in languages
            }

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

##################### OBS #################################
# Currently rewriting to handle multiple languages, etc. 
# Reach this far
# It will break
###########################################################

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



