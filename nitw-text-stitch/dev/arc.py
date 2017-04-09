from PIL import Image
from PIL import ImageDraw
import os
imagedir = 'speech/'

frames =[]

def add_speechbubble(im):

    padding_size = 25
    chord_spacing = 20
    width,height = im.size

    text_im = Image.new('RGBA', (width + 40, height + 40), 'black')
    text_im.paste(im, (20,20))

    textwidth, textheight = text_im.size
    container_im = Image.new('RGBA', (textwidth + chord_spacing + padding_size * 2, textheight + chord_spacing + padding_size * 2), 'red')
    # img.show(container_im)
    draw = ImageDraw.Draw(container_im)

    container_im.paste(text_im, (padding_size, padding_size))

    # Left Chord
    draw.chord(  [(padding_size - chord_spacing + 5, padding_size - chord_spacing),(5  + textheight + padding_size - chord_spacing,textheight + padding_size + chord_spacing)],135,225, 'yellow' )

    # Right Chord
    draw.chord(   [( textwidth  - chord_spacing  + padding_size - 65 , padding_size - chord_spacing),(padding_size + textwidth + chord_spacing -5 , padding_size  + textheight + chord_spacing)],315,45, 'orange' )

    # Top Chord
    draw.chord( [(padding_size , padding_size - chord_spacing + 10),(padding_size+ textwidth, padding_size + 10) ],180,0 ,'green' )

    # Bottom Chord
    draw.chord( [(padding_size , padding_size - chord_spacing + textheight + 10),(padding_size  + textwidth, padding_size + textheight + 10) ],0,180, 'black' )

    #Speech Line

    containerwidth, containerheight = container_im.size

    final_im = Image.new('RGBA', (containerwidth + 60, containerheight), 'red')
    final_im.paste(container_im, (60,0))

    final_draw = ImageDraw.Draw(final_im)
    final_draw.polygon([ (0,0), (85,50), (85,25) ], 'black', 'black')


    return final_im

for imagefile in os.listdir(imagedir):
    img = Image.open(imagedir + str(imagefile) )
    new_img = add_speechbubble(img)
    new_img.show()
