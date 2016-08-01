#!/usr/bin/env python
# -*- coding: utf-8 -*-

######## Todo #########
# - Distance
# - Bad sequences
# - Shift
#######################

# Imports
from itertools import compress
import numpy as np
import matplotlib.pyplot as plt


########## Config ##########
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
                            }

shift_key_distance_multiplier = 2.0
column_row_offset = [0,1,1,0]
distance_matrix = [[5.0,5.0,4.0,4.0,4.0,3.5,4.5,4.0,4.0,4.0,4.0,4.0,4.5],
                   [2.0,2.0,2.0,2.0,2.5,3.0,2.0,2.0,2.0,2.0,2.5,4.0],
                   [0.0,0.0,0.0,0.0,2.0,2.0,0.0,0.0,0.0,0.0,2.0,4.0],
                   [3.0,2.0,2.0,2.0,2.0,3.5,2.0,2.0,2.0,2.0,2.0]
                  ]

language = [['|', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '\\'], ['§', '!', '"', '#', '¤', '%', '&', '/', '(', ')', '=', '?', '`'], ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', '¨'], ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Å', '^'], ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ø', 'æ', "'"], ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ø', 'Æ', '*'], ['<', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-'], ['>', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_']]


########## Generate lookup tables ##########
char_2_row = {}
char_2_column = {}
char_2_distance = {}
char_2_finger = {}

finger_array = {finger: [[int(char) for char in mask] for mask in physical_finger_placement[finger]] for finger in physical_finger_placement}

# Parse language string
for i, row in enumerate(language):
    for j, char in enumerate(row):
        char_2_row[char] = i // 2
        char_2_column[char] = j + column_row_offset[i // 2]
        distance_multiplier = 1 if i % 2 == 0 else shift_key_distance_multiplier
        char_2_distance[char] = distance_matrix[i // 2][j] * distance_multiplier
        char_2_finger[char] = 'n'
        for finger in finger_array:
            if (finger_array[finger][i // 2][j]):
                char_2_finger[char] = finger


########## Stats counters ##########
counters = {
            'distance': {},
            'hand': {},
            'hand_length': {finger[0]: {} for finger in physical_finger_placement},
            'finger': {},
            'finger_length': {finger: {} for finger in physical_finger_placement},
            'rolls': {finger[0]: {} for finger in physical_finger_placement},
            'sequence': {}
           }


########## Funcitons ##########
def dict_increment(string, *arg):
    """ Increment dict if key exists, else set = 1 """
    dict = counters[string]
    key = arg[-1]
    levels = len(arg) - 2
    current = dict
    for i in range(levels):
        current = current[arg[i + 1]]
    if (key in current):
        current[key] += 1
    else:
        current[key] = 1

def get_roll_direction(index_list):
    """ Return roll direction of sequence of indeces """
    if (len(index_list) < 2):
        return 'short'
    is_out = True
    is_in = True
    for i in range(len(index_list) - 1):
        if index_list[i + 1] <= index_list[i]:
            is_out = False
        if index_list[i + 1] >= index_list[i]:
            is_in = False
    if (not is_out and not is_in):
        return 'none'
    return 'in' if is_in else 'out'


########## Begin ##########
# Read file
f = open('input.txt', 'r')
text = f.read();

# Buffers and counters
hand_length = 0
finger_length = 0
roll_buffer = []
hand_current = 'n'
finger_current = 'n'
previous_char = ''


for char in text:
    # Get current finger and hand
    finger_new = char_2_finger.get(char, 'n')
    hand_new = finger_new[0]

    # Finger stats
    dict_increment('finger', finger_new)
    if (finger_new != finger_current and finger_length > 0):
        dict_increment('finger_length', finger_current, finger_length)
        finger_length = 1
    elif (previous_char != char):
        """ Avoid penalizing repeated characters """
        finger_length += 1

    # Hands stats
    dict_increment('hand', hand_new)
    if (hand_new != hand_current and hand_length > 0):
        dict_increment('hand_length', hand_current, hand_length)
        hand_length = 1
    else:
        hand_length += 1

    # Distance and sequence
    dict_increment('distance', char_2_distance.get(char, 0))
    # TODO: sequence
    
    # Rolls stats triads
    length = len(roll_buffer)
    if (hand_new != hand_current):
        """ Roll TRIADS terminate when switching hands """
        if (length > 0):
            dict_increment('rolls', hand_current, get_roll_direction(roll_buffer))
        if (hand_new == 'n'):
            roll_buffer = []
        else:
            roll_buffer = [finger_new[1]]
    elif (length == 2):
        dict_increment('rolls', hand_current, get_roll_direction(roll_buffer + [finger_new[1]]))
        roll_buffer[0] = roll_buffer[1]
        roll_buffer[1] = finger_new[1]
    elif (hand_new != 'n'):
        roll_buffer.append(finger_new[1])
    
    # Prepare for next iteration
    finger_current = finger_new
    hand_current = hand_new

