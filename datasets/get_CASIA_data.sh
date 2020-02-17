#!/bin/bash
# Download CASIA HWDB1.1tst (Chinese hand-written characters dataset)
mkdir CASIA_data
cd CASIA_data
wget  "http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1tst_gnt.zip"
unzip HWDB1.1tst_gnt.zip -d ./gnt_files

# Convert gnt files to npy files
cd ..
python gnt2npy.py
rm -rf ./CASIA_data/gnt_files