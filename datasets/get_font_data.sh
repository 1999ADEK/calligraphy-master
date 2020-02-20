#!/bin/bash
# To train with different font, add the font file to datasets/
# and change the filename below to the filename of the file.
python get_font.py --store_dir trainA --font_style handwritten --img_size 128
python get_font.py --store_dir trainB --font_style calligraphy --img_size 128