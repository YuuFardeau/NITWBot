import os, sys
import DictMapping
import TextStitch
import re

def create(raw_input, character_type="mae", animated="no", message_id="buffer"):

    easteregg = False
    no_frames = 1
    no_head_frames = 1
    if animated == "yes":
        no_frames = 3
        no_head_frames = 12

    # special rule for pumpkinhead

    if character_type.lower() == "pumpkinhead":
        iter = (len(raw_input) // 25) + 1
        raw_input = ""
        for i in range (0,iter):
            raw_input += "*mmf*"


    # Special rule for gregg

    elif character_type.lower() == "gregg":
        if "cup" in raw_input.lower() or "cups" in raw_input.lower():
            easteregg = True

    # Special rule for bea

    elif character_type.lower() == "bea":
        if "real" in raw_input.lower():
            easteregg = True

    if (DictMapping.init(character_type) is True):

        frames=[]
        headfiles =[]

        raw_input = re.sub(r'\<\:.*?\>', '', raw_input)
        for x in range(1, no_head_frames + 1):
                headbuffer = DictMapping.print_char('¬',0,easteregg,x) # Prints character head
                if headbuffer:  headfiles.append(headbuffer)

        for x in range(1,no_frames + 1):
            sentence = []
            message_length = 0

            for p, c in enumerate(raw_input.upper()):
                c = c.encode('unicode-escape')

                buffer = DictMapping.print_char(c,message_length,easteregg,x)
                if buffer and (buffer is not None):
                    sentence.append(buffer)
                    message_length+=1
            if animated== "yes":
                frames.append(sentence)

        newlinepoints = DictMapping.get_newlinepoints()
        forcednewlinepoints = DictMapping.get_newforcedlinepoints()
        if sentence:
            if animated =="yes": sentence = frames

            final_response = TextStitch.create_image(sentence, animated, message_id, headfiles, newlinepoints, forcednewlinepoints)
            if final_response[0] == True:
                return {'status': True, 'image': final_response[1]}
            else:
                return {'status': False, 'error': final_response[1]}
        else:
            return {'status': False, 'error': 'No Characters Recognised'}
    else:
        return {'status': False}
