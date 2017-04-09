from PIL import Image, ImageChops, ImageOps
import sys, os

imagedir = '../assets/dialogue/'
trimmeddir = '../assets/trimmed_dialogue/'

def remove_alpha(im):
    im=im.convert('RGBA') # Convert this to RGBA if possible
    canvas = Image.new('RGBA', im.size, (0,0,0,255)) # Empty canvas colour (r,g,b,a)
    canvas.paste(im, mask=im) # Paste the image onto the canvas, using it's alpha channel as mask
    return canvas

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))

    diff = ImageChops.difference(im, bg)

    diff = ImageChops.add(diff, diff, 2.0, -100)
    print (diff)
    bbox = diff.getbbox()
    bboxmod = bbox
    bboxmod = (bbox[0], 0, bbox[2], 64)
    # bbox = (20,,,59)
    print (bboxmod)
    print (type(bboxmod))
    if bboxmod:
        return im.crop(bboxmod)

for imagefile in os.listdir(imagedir):

    image = Image.open(imagedir + str(imagefile) )
    print (imagefile)
    image = remove_alpha(image)
    editimage = trim(image)
    editimage.save(trimmeddir + str(imagefile))
