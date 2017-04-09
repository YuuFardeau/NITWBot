from pathlib import Path
import logging


def init(character_type="mae"):

    global __INGAMECHARACTERS__
    global __CHARACTERMAPPING__
    global __CHARACTERHEAD__
    global __CHARACTERCOLOUR__
    global __NEWLINECHARACTER__
    global __NEWLINEPOINTS__
    global __NEWFORCEDLINEPOINTS__

    # Tracks where new lines can go sensibly: i.e after punctuation or a space
    __NEWLINEPOINTS__ = []

    # Tracks where new lines are forced
    __NEWFORCEDLINEPOINTS__ = []



    __CHARACTERMAPPING__ =  {b'A': 'A', b'\'': "APOSTROPHE", b'*': 'ASTERISK', b'B': 'B', b'C': 'C', b':' : 'COLON',  b',': 'COMMA', b'D': 'D',
                            b'-': 'DASH', b'$': 'DOLLAR', b'E': 'E', b'8': 'EIGHT',b'!': 'EXCLAMATION', b'F': 'F', b'5': 'FIVE', b'4': 'FOUR',
                            b'G': 'G', b'H': 'H', b'I': 'I', b'J': 'J', b'K': 'K', b'L': 'L', b'M': 'M', b'N': 'N', b'9': 'NINE', b'O': 'O',
                            b'1': 'ONE', b'P': 'P', b'%' : 'PERCENT', b'.' : 'PERIOD', b'Q': 'Q', b'?': 'QUESTION', b'"' : 'QUOTE',
                            b'R': 'R', b'S': 'S', b';': 'SEMICOLON', b'7': 'SEVEN', b'6': 'SIX', b'T': 'T', b'3': 'THREE', b'2': 'TWO',
                            b'U': 'U', b'V': 'V', b'W': 'W', b'X': 'X', b'Y': 'Y', b'Z': 'Z', b'0': 'ZERO', b' ': 'SPACE'}

    __INGAMECHARACTERS__ = {'gregg': 'gregg', 'mae': 'standard', 'bea': 'bea', 'lori': 'lori', 'coffinwolf': 'coffinwolf', 'germ': 'germ', 'angus': 'angus',
                            'adina': 'standard', 'selmers': 'standard', 'jackie': 'standard', 'pumpkinhead': 'standard', 'garbo': 'standard', 'molly': 'standard',
                            'malloy': 'standard', 'dad': 'standard', 'mom': 'standard', 'cole': 'standard', 'deer': 'standard', 'sharkle': 'standard'}

    __NEWLINECHARACTER__ = [b' ', b'!', b'?', b',']

    if character_type in __INGAMECHARACTERS__:
        __CHARACTERHEAD__ = character_type
        __CHARACTERCOLOUR__ = __INGAMECHARACTERS__[character_type]
        return True
    else:
        return None
     #
    #  __ACCENTCHARACTERMAPPING__ = { b'\\xc0': 'A', b'\\xc1': 'A', b'\\xc2': 'A', b'\\xc3': 'A', b'\\xc4': 'A', b'\\xc5': 'A',
    #                                 b'\\xc7': 'C',b'\\xc8': 'E',b'\\xc9': 'E',b'\\xca': 'E',b'\\xcb': 'E',b'\\xcc': 'I',b'\\xcd': 'I',
    #                                 b'\\xce': 'I',b'\\xcf': 'I',b'\\xd0': 'D',b'\\xd1': 'N',b'\\xd2': 'O',b'\\xd3': 'O',b'\\xd4': 'O',
    #                                 b'\\xd5': 'O',b'\\xd6': 'O'}
     #
     #
    #  __CHARACTERMAPPING__.update(__ACCENTCHARACTERMAPPING__)
def get_newlinepoints():

    return __NEWLINEPOINTS__

def get_newforcedlinepoints():

    return __NEWFORCEDLINEPOINTS__

def print_char(c,MESSAGE_LENGTH,easteregg, fontvariant=1):
    if (len(c) == 1): # Standard character
        if c == '¬':
            if easteregg == True:
                return 'nitw-text-stitch/assets/heads/' + __CHARACTERHEAD__ + '_easter.png'
            else:
                return 'nitw-text-stitch/assets/heads/' + __CHARACTERHEAD__ + '.png'

        if c in __NEWLINECHARACTER__:
            __NEWLINEPOINTS__.append(MESSAGE_LENGTH)

        if c in __CHARACTERMAPPING__:
            return 'nitw-text-stitch/assets/' + __CHARACTERCOLOUR__ + '_dialogue/' + 'Dialogue_standard_1_' + __CHARACTERMAPPING__[c] + str(fontvariant) + '.png'
        else:
            logging.info("Unrecognised Character: " + str(c))
            return None
    # New Line
    elif (c.decode("utf-8") == "\\n"):
        __NEWFORCEDLINEPOINTS__.append(MESSAGE_LENGTH)
        return 'nitw-text-stitch/assets/' + __CHARACTERCOLOUR__ + '_dialogue/' + 'Dialogue_standard_1_' + 'SPACE' + str(fontvariant) + '.png'
    else:
        parsed_c = c.decode("utf-8")[2:].lstrip('0')
        logging.info("Parsed Emoji:" + str(parsed_c))
        filepath = Path('nitw-text-stitch/assets/emojis/' + parsed_c + '.png')
        if filepath.is_file():
            return 'nitw-text-stitch/assets/emojis/' + parsed_c + '.png'
        else:
            logging.info("Unrecognised Emoji: " + str(c))
            return None
