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
        if (finger_new != finger_current):
            dict_increment(language, 'finger_length_freq', finger_current, finger_length)
            finger_length = 1
        elif (previous_char != char):
            """ Avoid multiple counting for repeated characters """
            finger_length += 1

        # Hands stats
        dict_increment(language, 'hand_freq', hand_new)
        if (hand_new != hand_current):
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
    print('============' + language + '=============')
    for stats in counters[language]:
        print(stats)
        print(counters[language][stats])
        print()
    print('===============================')

"""
same_finger_count = 0
for i in finger_length_freq:
    for j in finger_length_freq[i]:
        if j > 1:
            same_finger_count += finger_length_freq[i][j]
print(same_finger_count)
"""


