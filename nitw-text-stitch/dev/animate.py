from PIL import Image
import os
imagedir = 'animated/'

frames =[]

for imagefile in os.listdir(imagedir):

    img = Image.open(imagedir + str(imagefile) )
    frames.append(img)


im = frames[0]
im.save('test.gif', save_all=True, duration=250, append_images = frames)
