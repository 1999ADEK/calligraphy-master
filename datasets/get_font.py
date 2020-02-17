import os
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pickle

def get_char_list():
    with open('char_list.pk', 'rb') as f:
        l = pickle.load(f)
        return l

def create_char_img(ch, font, size, x_offset=0, y_offset=0):
    img = Image.new("L", (size, size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, 0, font=font)
    return img

def gen_dataset(filename, size=128):
    font = ImageFont.truetype(filename, size)
    char_list = get_char_list()
    os.chdir('./trainB/')
    print('Generating font dataset...')
    for i, ch in enumerate(char_list):
        int_unicode = int(ch, 16)
        img = create_char_img(chr(int_unicode), font, size)
        img = np.array(img.getdata()).reshape((size, size)).astype('uint8')
        np.save(f'font{i:04}', (img, int_unicode))
    print('Complete.')
    os.chdir('..')

    
parser = argparse.ArgumentParser(description='Construct font datasets')
parser.add_argument('--font_filename', dest='filename', required=True, help='filename of the font file')

args = parser.parse_args()

if __name__ == '__main__':
    gen_dataset(args.filename)