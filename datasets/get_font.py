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

def gen_dataset(filename, store_dir, size=128):
    font = ImageFont.truetype(filename, size)
    char_list = get_char_list()
    os.mkdir(store_dir)
    os.chdir(store_dir)
    print('Generating font dataset...')
    for i, ch in enumerate(char_list):
        int_unicode = int(ch, 16)
        img = create_char_img(chr(int_unicode), font, size)
        img.save(f'font{int_unicode}.bmp')
    print('Complete.')
    os.chdir('..')

    
parser = argparse.ArgumentParser(description='Construct font datasets')
parser.add_argument('--store_dir', dest='store_dir', required=True, help='directory to store the images')
parser.add_argument('--font_filename', dest='filename', required=True, help='filename of the font file')

args = parser.parse_args()

if __name__ == '__main__':
    gen_dataset(args.filename, args.store_dir)