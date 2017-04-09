from PIL import Image, ImageChops, ImageOps, ImageDraw, ImagePalette
import sys
from pprint import pprint

def create_image(sentence_a, animated, filename, headfiles, newlinepoints, forcednewlinepoints):

    kerning_spacing = 5
    ends_padding = 10
    left_padding = 30
    image_directory = 'images/'
    soft_line_limit = 850
    hard_line_limit = 1200
    current_line_length = 0
    # # is character for displaying heads



    if animated=="yes": # This is animated
        frames = []
        # for position,frame in enumerate(sentence_a):
        #     images = list(map(Image.open, frame))
        #     widths, heights = zip(*(i.size for i in images))
        #     total_width = sum(widths)
        #     max_height = max(heights)
        #     kerning_total = (len(images) * kerning_spacing)
        #
        #     new_im = Image.new('RGBA', (total_width + kerning_total + ends_padding + ends_padding, max_height))
        #
        #     x_offset = 0
        #     for p,im in enumerate(images):
        #         print (p)
        #         if (p in newlinepoints):
        #             print ("new line opportunity")
        #         new_im.paste(im, (x_offset + ends_padding,0))
        #         x_offset += im.width + kerning_spacing
        #
        #
        #     new_im = remove_transparency(new_im)
        #     new_im = add_speechbubble(new_im, 'black')
        #     new_im = remove_transparency(new_im, (0,255,0))
        #     new_im = new_im.convert('P', colors=255, dither=Image.NONE)
        #     palette = new_im.getpalette()
        #
        #     for i in range(0, len(palette), 3):
        #         index = palette[i:i + 3]
        #         if index == [0,255,0]:
        #             transparency_index =  (int(i / 3))
        #             # print (index)
        #     # print (new_palette)
        #     # new_im.quantize(colors=256, method=2, kmeans = 0, palette = None)
        #
        #
        #     frames.append(new_im)
        #
        #
        # im = frames[0]
        #
        # im.save(image_directory + filename + '.gif', save_all=True, duration=250, loop=999, append_images = frames, transparency=transparency_index)
        #
        #
        # return (image_directory + filename + '.gif')

    else:  # This is a still frame

        images = list(map(Image.open, sentence_a))
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        kerning_total = (len(images) * kerning_spacing)
        new_im = Image.new('RGBA', (total_width + kerning_total + ends_padding + ends_padding, max_height))

        x_offset = 0
        y_offset = 0
        line_max_width = 0
        line_limit = 5
        no_lines = 1
        for p,im in enumerate(images):
            current_line_length+=im.width + kerning_spacing
            new_im.paste(im, (x_offset + ends_padding,y_offset))
            x_offset += im.width + kerning_spacing
            # print (current_line_length)
            if (no_lines > line_limit):

                return (False, 'Message has too many lines: Limit is 5. Consider removing forced newlines or shortening your message')

            if (( ( p in newlinepoints) and (current_line_length > soft_line_limit) and (p+1 not in newlinepoints) ) or (current_line_length > hard_line_limit) or (p in forcednewlinepoints)):

                if (p + 1< len(images)): # If not last character
                # NEW LINE - We need to create new image, and paste
                    if (x_offset + ends_padding + ends_padding > line_max_width):

                        line_max_width = x_offset + ends_padding + ends_padding

                    current_line_length = 0
                    y_offset += max_height
                    resized_im = Image.new('RGBA', (total_width + kerning_total + ends_padding + ends_padding, max_height + y_offset))
                    resized_im.paste(new_im)
                    new_im = resized_im
                    x_offset = 0
                    no_lines += 1
        if (x_offset + ends_padding + ends_padding > line_max_width):
            line_max_width = x_offset + ends_padding + ends_padding


        new_im = new_im.crop((0,0, line_max_width,y_offset + max_height))
        #
        #
        new_im = remove_transparency(new_im)
        #
        new_im = add_speechbubble(new_im,headfiles[0])

        textwidth, textheight = new_im.size

        head_im = Image.open(headfiles[0])
        # head_im = remove_transparency(head_im)
        headwidth, headheight = head_im.size
        final_im = Image.new('RGBA', (left_padding + textwidth + headwidth, textheight))
        final_im.paste(head_im, (left_padding,textheight-headheight))
        final_im.paste(new_im,(left_padding + headwidth,0))

        final_im.save(image_directory + filename + '.png')
        return (True, image_directory + filename + '.png')


def add_speechbubble(im, headfile, color=(0,0,0)):


    container_padding = 25
    chord_padding = 20
    width,height = im.size

    if (height <= 64):
        chord_padding = 10

    mouthheight_dict = {'jackie': 32, 'angus': 35, 'mae': 30, 'bea': 60, 'lori': 55, 'coffinwolf': 50, 'germ': 45, 'pumpkinhead': 40,
                        'adina': 40, 'selmers': 25, 'garbo': 70, 'molly': 40, 'malloy': 65, 'dad': 40, 'mom': 40, 'cole': 40,
                        'deer': 42, 'sharkle': 80, 'gregg': 45}
    mouthpadding_dict = {'lori': 10}
    mouthposition = 20
    mouthpadding = 0

    for key in mouthheight_dict.keys():

        if key in headfile:
            mouthposition = mouthheight_dict[key]

    for key in mouthpadding_dict.keys():

        if key in headfile:
            mouthpadding = mouthpadding_dict[key]

    text_im = Image.new('RGB', (width + container_padding + container_padding, height + container_padding + container_padding), 'black')
    text_im.paste(im, (container_padding, container_padding))

    imagewidth, imageheight = text_im.size

    container_im = Image.new('RGBA', (imagewidth + container_padding + container_padding, imageheight + container_padding + container_padding), None)
    container_im.paste(text_im, (container_padding, container_padding))

    draw = ImageDraw.Draw(container_im)
    #  top chord
    draw.chord([container_padding, container_padding - chord_padding,
                container_padding + imagewidth, container_padding + chord_padding],180,0, 'black')

    # bottom chord
    draw.chord([container_padding, container_padding + imageheight - chord_padding,
                container_padding + imagewidth, container_padding + imageheight + chord_padding],0,180, 'black')

    # Left chord
    draw.chord([container_padding - chord_padding, container_padding,
                container_padding + chord_padding, container_padding + imageheight], 90, 270, 'black')

    # Right chord
    draw.chord([container_padding + imagewidth - chord_padding, container_padding,
                container_padding + imagewidth + chord_padding, container_padding + imageheight], 270, 90, 'black')

    containerwidth, containerheight = container_im.size

    final_im = Image.new('RGBA', (containerwidth + 60, containerheight), None)
    final_im.paste(container_im, (60,0))

    # Speech Line
    finalwidth, finalheight = final_im.size

    final_draw = ImageDraw.Draw(final_im)
    final_draw.polygon ([ (0,finalheight - mouthposition), (60 + container_padding, finalheight - 28), (60 + container_padding, finalheight-85)], 'black', 'black' )

    #Speech Line

    #
    #

    #
    # final_draw = ImageDraw.Draw(final_im)
    # final_draw.polygon([ (0,height + mouthposition), (90,height +20), (120, height+65) ], color, color)


    return final_im



#  Function from stackoverflow
def remove_transparency(im, bg_colour=(0, 0, 0)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im
