from PIL import Image
from random import randint

import base4

# load an image and return a copy
def load_image(filename):
    try:
        origional = Image.open(filename, 'r')
        image = origional.copy()
    except FileNotFoundError:
        print('File not found.')
        image = None
    except:
        print('Unknown error opening image.')
        image = None
    return image

# save an image
def save_image(image, filename):
    ext = str(filename.split('.')[-1].upper())
    if ext == 'JPG':
        ext = 'JPEG'
    try:
        image.save(filename, ext)
        return True
    except:
        print('Unknown error saving image.')
        return False

# get the next 2 pixels of an image
def next_pixel_pair(image):
    return [colour for colour in next(image)[:3] + next(image)[:3]]

# encode a string in an image and return the encoded image
def encode_image(data, image):
    if isinstance(data, str):
        data = base4.encode(data)

    if isinstance(image, str):
        image = load_image(image)
    
    width = image.size[0]
    x, y = 0, 0
    for encoded_pixel in encode_pixels(data, image):
        image.putpixel((x, y), encoded_pixel)
        if x == width - 1:
            x, y = 0, y + 1
        else:
            x += 1
    return image

# formats the end nibble of encoded pixels to indicate encoded data end
def format_end_nibble(data_index, data_length, pixel_pair):
    if data_index == data_length - 1:
        if pixel_pair[-1] % 2 != 0:
            pixel_pair[-1] -= 1
        if pixel_pair[4] % 2 != 0:
            pixel_pair[4] -= 1
    else:
        if pixel_pair[-1] % 2 != 0:
            pixel_pair[-1] -= 1
        if pixel_pair[4] % 2 == 0:
            pixel_pair[4] += 1

# spread modulo to prevent anomalous lack of pixel data with certain modulus
spread_offset = {3:1, 6:-1}
def spread_modulo(index, pixel_pair):
    do_spread = randint(0, 1)
    modulo = pixel_pair[index] % 10
    if do_spread:
        pixel_pair[index] += spread_offset.get(modulo, 0)

# encode a 4 digit base 4 word in 2 pixels and yield each pixel as a tuple
def encode_pixels(data, image):
    image = iter(image.getdata())
    
    for i in range(len(data)):
        p_pair = next_pixel_pair(image)

        for j in range(5):
            if j < 4:
                encode = data[i][j]
                current = p_pair[j] % 10
            
                if current < 5:
                    p_pair[j] -= (current - encode)
                else:
                    p_pair[j] += (6 + encode - current)
                spread_modulo(j, p_pair)
            elif j == 4:
                format_end_nibble(i, len(data), p_pair)

        yield tuple(p_pair[:3])
        yield tuple(p_pair[3:])

# decode an image file containing encoded data
base4_mapping = {0:0, 5:0, 6:0, 1:1, 7:1, 2:2, 8:2, 3:3, 4:3, 9:3}
def decode_image(image):
    if isinstance(image, str):
        image = load_image(image)
    image = iter(image.getdata())

    base4_encoded = []

    while True:
        b4_word = []
        p_pair = next_pixel_pair(image)

        for i in range(4):
            digit = base4_mapping[p_pair[i] % 10]
            b4_word.append(digit)
        base4_encoded.append(b4_word)

        if p_pair[4] % 2 == p_pair[-1] % 2:
            decoded = base4.decode(base4_encoded)
            return decoded
