#!/bin/bash
# To train with different font, add the font file to datasets/
# and change the filename below to the filename of the file.
python get_font.py --store_dir trainA --font_filename FZJingLei.ttf
python get_font.py --store_dir trainB --font_filename MaShanZheng-Regular.ttf