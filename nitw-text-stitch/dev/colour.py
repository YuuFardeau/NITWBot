from PIL import Image
from math import floor
import os
imagedir = '../assets/standard_dialogue/'
editdir = '../assets/coffinwolf_dialogue/'


R_VALUE = 57;
G_VALUE = 125;
B_VALUE = 156;

for imagefile in os.listdir(imagedir):

    img = Image.open(imagedir + str(imagefile) )
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    blackCanvas =[]
    for item in datas:
        blackCanvas.append((0,0,0,255))
        if item[0] > 10 and item[1] > 10 and item[2] > 10:
            transparency_ratio = (255 / item[3])

            newData.append((floor(item[0] - (255-R_VALUE)), floor(item[1] - (255-G_VALUE)), floor(item[2] - (255-B_VALUE)), 255))
        else:
            newData.append(item)
    img.putdata(blackCanvas)
    img.putdata(newData)
    img.save(editdir + str(imagefile),"PNG")
