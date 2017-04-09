from PIL import Image
from PIL import ImageDraw
import os

container_padding = 25
chord_padding = 5
mouthposition = 20

im = Image.open("new.jpg")

width, height = im.size

text_im = Image.new('RGB', (width + container_padding + container_padding, height + container_padding + container_padding), 'orange')
text_im.paste(im, (container_padding, container_padding))

imagewidth, imageheight = text_im.size

container_im = Image.new('RGBA', (imagewidth + container_padding + container_padding, imageheight + container_padding + container_padding),'purple')
container_im.paste(text_im, (container_padding, container_padding))

draw = ImageDraw.Draw(container_im)
#  top chord
draw.chord([container_padding, container_padding - chord_padding,
            container_padding + imagewidth, container_padding + chord_padding],180,0, 'red')

# bottom chord
draw.chord([container_padding, container_padding + imageheight - chord_padding,
            container_padding + imagewidth, container_padding + imageheight + chord_padding],0,180, 'green')

# Left chord
draw.chord([container_padding - chord_padding, container_padding,
            container_padding + chord_padding, container_padding + imageheight], 90, 270, 'blue')

# Right chord
draw.chord([container_padding + imagewidth - chord_padding, container_padding,
            container_padding + imagewidth + chord_padding, container_padding + imageheight], 270, 90, 'yellow')

containerwidth, containerheight = container_im.size

final_im = Image.new('RGBA', (containerwidth + 60, containerheight), 'pink')
final_im.paste(container_im, (60,0))

# Speech Line
finalwidth, finalheight = final_im.size

final_draw = ImageDraw.Draw(final_im)
final_draw.polygon ([ (0,finalheight - mouthposition), (60 + container_padding, finalheight - 28), (60 + container_padding, finalheight-85)], 'brown', 'brown' )

final_im.show()
final_im.save("test.png")
