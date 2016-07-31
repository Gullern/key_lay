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

def load_finger_chars(languages, physical_finger_placement):
    # Generate dict with list of characters for each finger
    get_mask = lambda key: (int(char) for char in ''.join(
            element * 2 for element in physical_finger_placement[key])
            )
    finger_2_chars = {language: {
                                 finger: ''.join(compress(languages[language], get_mask(finger))) for finger in physical_finger_placement
                                } 
                      for language in languages
                     }

    # Attach space
    for language in languages:
        finger_2_chars[language][space_hand + '0'] += ' '

    # Generate reverse: associated finger for each char, makes relevant lookup faster
    def get_finger_slow(language, char):
        for finger in finger_2_chars[language]:
            if (char in finger_2_chars[language][finger]):
                return finger
        return 'n'

    char_2_finger = {language: {
                                char: get_finger_slow(language, char) for char in languages[language] + ' '
                                """ Remembers to attach space to the language string """
                               } 
                     for language in languages
                    }
    return finger_2_chars, char_2_finger

# Finger lookup dictionaries
finger_2_chars, char_2_finger = load_finger_chars(languages, physical_finger_placement)

# Stats counters
counters = {language: {
                       'char_freq': {},
                       'word_length_freq': {},
                       'hand_freq': {},
                       'hand_length_freq': {finger[0]: {} for finger in physical_finger_placement},
                       'finger_freq': {},
                       'finger_length_freq': {finger: {} for finger in physical_finger_placement},
                       'rolls': {finger[0]: {} for finger in physical_finger_placement}
                       }
            for language in languages
           }

# Functions
def get_finger(language, char):
    return char_2_finger[language].get(char, 'n')

def dict_increment(*arg):
    """ args: language, dictionary, key1, key2, ..., keyn """
    dict = counters[arg[0]][arg[1]]
    key = arg[-1]
    levels = len(arg) - 3
    current = dict
    for i in range(levels):
        current = current[arg[i + 2]]
    if (key in current):
        current[key] += 1
    else:
        current[key] = 1

def get_roll_direction(index_list):
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


# Read file
f = open('input.txt', 'r')
text = f.read();

# Begin processing
word_length = 0
hand_length = 0
finger_length = 0
roll_buffer = []
hand_current = 'n'
finger_current = 'n'
previous_char = ''

for language in languages:
    for char in text:
        # Characters and words stats
        dict_increment(language, 'char_freq', char)

        if (char in termination_symbols):
            if (word_length > 0):
                """ Avoid recording empty words, e.g. for '. ' """
                dict_increment(language, 'word_length_freq', word_length)
            word_length = 0
        else:
            word_length += 1

        # Get current finger and hand
        finger_new = get_finger(language, char)
        hand_new = finger_new[0]

        # Finger stats
        dict_increment(language, 'finger_freq', finger_new)
        if (finger_new != finger_current and finger_length > 0):
            dict_increment(language, 'finger_length_freq', finger_current, finger_length)
            finger_length = 1
        elif (previous_char != char):
            """ Avoid multiple counting for repeated characters """
            finger_length += 1

        # Hands stats
        dict_increment(language, 'hand_freq', hand_new)
        if (hand_new != hand_current and hand_length > 0):
            dict_increment(language, 'hand_length_freq', hand_current, hand_length)
            hand_length = 1
        else:
            hand_length += 1

        # Rolls stats
        if (hand_new != hand_current or char == ' '):
            """ Rolls terminate when switching hands OR at a space """
            if (len(roll_buffer) > 0):
                dict_increment(language, 'rolls', hand_current, get_roll_direction(roll_buffer))
            if (char == ' ' or hand_new == 'n'):
                roll_buffer = []
            else:
                roll_buffer = [finger_new[1]]
        elif (hand_new != 'n'):
            roll_buffer.append(finger_new[1])
        
        # Prepare for next iteration
        finger_current = finger_new
        hand_current = hand_new

for language in languages:
    print('============ ' + language + ' ============')
    for stats in counters[language]:
        print(stats)
        print(counters[language][stats])
        print()
    print('=' * (2 * 13 + len(language)))

"""
same_finger_count = 0
for i in finger_length_freq:
    for j in finger_length_freq[i]:
        if j > 1:
            same_finger_count += finger_length_freq[i][j]
print(same_finger_count)
"""

fig_sizes = {
             'char_freq': (15,6),
             'word_length_freq': (8,6),
             'hand_freq': (8,6),
             'finger_freq': (10,7),
             'hand_length_freq': (18,7),
             'finger_length_freq': (30,18),
             'rolls': (10,10)
            }


def plot_bar(figure_num, stats_string, multiple = False, num_levels = 0):
    """ Make a bar plot of the counter specified with stats_string 
    
    :param multiple: Whether a plot should be made for each language or not
    :param num_levels: The number of levels of dictionaries from which to extract the data from
    
    """
    plt.figure(num = figure_num, figsize = fig_sizes[stats_string], dpi = 100, facecolor = 'w', edgecolor = 'k')
    #fig, ax = plt.subplots()
    dict = counters[list(counters)[0]][stats_string]
    plt.title(stats_string)
    if (not multiple):
        width = 0.4
        plt.bar(range(len(dict)), [tuple[1] for tuple in sorted(dict.items())], width = width, align = 'center')
        plt.xticks(range(len(dict)), sorted(dict.keys()))
        """ Sort on keys """
    else:
        length = len(languages)
        for l in range(num_levels):
            length *= len(dict)
            dict = dict[list(dict)[0]]
        indent = (length - 1) / 2
        
        # Generate flattened list of all leaf-level frequency data with recursive dictionary structure as label
        data_list = []
        for language in languages:
            queue = [(language, item) for item in sorted(counters[language][stats_string].items())]
            for level in range(num_levels):
                current_length = len(queue)
                for j in range(current_length):
                    element = queue.pop(0)
                    items = sorted(element[1][1].items())
                    for item in items:
                        queue.append((element[0] + '/' + element[1][0], (item[0], item[1])))
            data_list += queue

        # Regroup list
        all_x_values = {}
        processed_list = [('', [])]
        for element in data_list:
            all_x_values[element[1][0]] = 1
            if (element[0] == processed_list[-1][0]):
                processed_list[-1][1].append(element[1])
            else:
                processed_list.append((element[0], [element[1]]))
        processed_list = processed_list[1:]

        # Syncronize x-values by padding
        all_x_values = sorted(list(all_x_values))
        num_x_values = len(all_x_values)
        #if () # TODO: typeof int -> pad extra

        for element in processed_list:
            for i, x in enumerate(all_x_values):
                if (len(element[1]) <= i or element[1][i][0] != x):
                    element[1].insert(i, (x, 0))
        #print(processed_list)
        
        # Make bar plot of the data
        x_array = range(num_x_values)
        prop_iter = iter(plt.rcParams['axes.prop_cycle'])
        plt.xticks(range(len(dict)), sorted(dict.keys()))
        width = 0.75/ len(processed_list)
        for i, element in enumerate(processed_list):
            while True:
                try:
                    plt.bar([x + width * (i - indent) for x in x_array], [tuple[1] for tuple in element[1]], width = width, align = 'center', color = next(prop_iter)['color'])
                except StopIteration:
                    prop_iter = iter(plt.rcParams['axes.prop_cycle'])
                    continue;
                break;
                
        plt.legend([element[0] for element in processed_list])

    plt.savefig(stats_string)


print(counters['qwerty']['hand_length_freq'])

figure_num = 0
plot_bar(figure_num, 'char_freq'); figure_num += 1
plot_bar(figure_num, 'word_length_freq'); figure_num += 1
plot_bar(figure_num, 'hand_freq', multiple = True); figure_num += 1
plot_bar(figure_num, 'finger_freq', multiple = True); figure_num += 1
plot_bar(figure_num, 'hand_length_freq', multiple = True, num_levels = 1); figure_num += 1
plot_bar(figure_num, 'finger_length_freq', multiple = True, num_levels = 1); figure_num += 1
plot_bar(figure_num, 'rolls', multiple = True, num_levels = 1)
