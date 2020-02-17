import os
import numpy as np
from PIL import Image

# Helper function from https://github.com/integeruser/CASIA-HWDB1.1-cnn/blob/master/src/utils.py
def read_gnt_in_directory(gnt_dirpath):
    def samples(f):
        header_size = 10

        # read samples from f until no bytes remaining
        while True:
            header = np.fromfile(f, dtype='uint8', count=header_size)
            if not header.size: break

            sample_size = header[0] + (header[1]<<8) + (header[2]<<16) + (header[3]<<24)
            tagcode = header[5] + (header[4]<<8)
            width = header[6] + (header[7]<<8)
            height = header[8] + (header[9]<<8)
            assert header_size + width*height == sample_size

            img = np.fromfile(f, dtype='uint8', count=width*height).reshape((height, width))
            yield img, tagcode

    for file_name in os.listdir(gnt_dirpath):
        if file_name.endswith('.gnt'):
            file_path = os.path.join(gnt_dirpath, file_name)
            with open(file_path, 'rb') as f:
                for img, tagcode in samples(f):
                    yield img, tagcode
                    
def gnt2npy(gnt_dirpath):
    print('Converting gnt files to npy files...')
    os.chdir('./trainA/')
    for i, (img_array, tagcode) in enumerate(read_gnt_in_directory(gnt_dirpath)):
        img = Image.fromarray(img_array)
        img.save(f'hw{tagcode}.bmp')
    print(f'Complete. Get {i} files in total.')
    os.chdir('..')
    
if __name__ == '__main__':
    gnt2npy('./gnt_files/')