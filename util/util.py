"""This module contains simple helper functions """
from __future__ import print_function
import torch
import numpy as np
from PIL import Image
import os


def tensor2im(input_image, imtype=np.uint8):
    """"Converts a Tensor array into a numpy image array.

    Parameters:
        input_image (tensor) --  the input image tensor array
        imtype (type)        --  the desired type of the converted numpy array
    """
    if not isinstance(input_image, np.ndarray):
        if isinstance(input_image, torch.Tensor):  # get the data from a variable
            image_tensor = input_image.data
        else:
            return input_image
        image_numpy = image_tensor[0].cpu().float().numpy()  # convert it into a numpy array
        if image_numpy.shape[0] == 1:  # grayscale to RGB
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0  # post-processing: tranpose and scaling
    else:  # if it is a numpy array, do nothing
        image_numpy = input_image
    return image_numpy.astype(imtype)


def diagnose_network(net, name='network'):
    """Calculate and print the mean of average absolute(gradients)

    Parameters:
        net (torch network) -- Torch network
        name (str) -- the name of the network
    """
    mean = 0.0
    count = 0
    for param in net.parameters():
        if param.grad is not None:
            mean += torch.mean(torch.abs(param.grad.data))
            count += 1
    if count > 0:
        mean = mean / count
    print(name)
    print(mean)


def save_image(image_numpy, image_path, aspect_ratio=1.0):
    """Save a numpy image to the disk

    Parameters:
        image_numpy (numpy array) -- input numpy array
        image_path (str)          -- the path of the image
    """

    image_pil = Image.fromarray(image_numpy)
    h, w, _ = image_numpy.shape

    if aspect_ratio > 1.0:
        image_pil = image_pil.resize((h, int(w * aspect_ratio)), Image.BICUBIC)
    if aspect_ratio < 1.0:
        image_pil = image_pil.resize((int(h / aspect_ratio), w), Image.BICUBIC)
    image_pil.save(image_path)


def print_numpy(x, val=True, shp=False):
    """Print the mean, min, max, median, std, and size of a numpy array

    Parameters:
        val (bool) -- if print the values of the numpy array
        shp (bool) -- if print the shape of the numpy array
    """
    x = x.astype(np.float64)
    if shp:
        print('shape,', x.shape)
    if val:
        x = x.flatten()
        print('mean = %3.3f, min = %3.3f, max = %3.3f, median = %3.3f, std=%3.3f' % (
            np.mean(x), np.min(x), np.max(x), np.median(x), np.std(x)))


def mkdirs(paths):
    """create empty directories if they don't exist

    Parameters:
        paths (str list) -- a list of directory paths
    """
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir(path):
    """create a single empty directory if it didn't exist

    Parameters:
        path (str) -- a single directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)

def split_img(imagepath, m, n, order='horizontal'):
    """split an image into m * n images
    
    Parameters:
        imagepath (str) -- filepath of the image
        m (int)         -- split the image into m parts horizontally
        n (int)         -- split the image into n parts vertically
        order (str)     -- split the image from left to right, top to bottom ('horizontal')
                                           from top to bottom, right to left ('vertical')
    """
    img = Image.open(imagepath)
    w, h = img.size
    new_w = w // m
    new_h = h // n
    if order == 'horizontal':
        for y in range(n):
            for x in range(m):
                yield img.crop((x*new_w, y*new_h, (x+1)*new_w, (y+1)*new_h))
    elif order == 'vertical':
        for x in reversed(range(m)):
            for y in range(n):
                yield img.crop((x*new_w, y*new_h, (x+1)*new_w, (y+1)*new_h))
    else:
        raise Exception(f'Expect order to be horizontal or vertical. Get {order} instead.')
    
        
            

def split_and_save(imagepath, outputpath, m, n, size, order='horizontal'):
    """split an image an save to desired directory
    
    Parameters:
        imagepath (str)  -- filepath of the image
        outputpath (str) -- directory to which the splitted images are saved
        m (int)          -- split the image into m parts horizontally
        n (int)          -- split the image into n parts vertically
        size (tuple (int, int)) -- size of splitted images
        order (str)      -- split the image from left to right, top to bottom ('horizontal')
                                            from top to bottom, left to right ('vertical')
    """
    image_name = os.path.splitext(os.path.basename(imagepath))[0]
    mkdir(outputpath)
    for i, img in enumerate(split_img(imagepath, m, n, order)):
        img.resize(size).save(os.path.join(outputpath, f'{image_name}{i:03}.png'))
        
def get_img(filepath, isFake=True):
    """yield an image from the given directory
    
    Parameters:
        filepath (str) -- filepath of the directory
        isFake (bool)  -- combine real or fake images in the directory (isFake == True then combine fake images)
    """
    string = 'fake' if isFake else 'real'
    for imagefile in os.listdir(filepath):
        if string in imagefile:
            yield Image.open(os.path.join(filepath, imagefile))

def combine_and_save(imagepath, outputpath, m, n, size=128, order='horizontal', isFake=True):
    """combine images in the given directory and save
    
    Parameters:
        imagepath (str)  -- filepath of the images directory
        outputpath (str) -- directory to which the combined image is saved
        m (int)          -- max number of images to combined horizontally
        n (int)          -- max number of images to combined vertically
        size (tuple (int, int)) -- size of images to combined
        order (str)      -- combine the images from left to right, top to bottom ('horizontal')
                                               from top to bottom, right to left ('vertical')
        isFake (bool)    -- combine real or fake images in the directory (isFake == True then combine fake images)
    """
    new_img = Image.new('L', (size*m, size*n), 255)
    if order == 'horizontal':
        for i, img in enumerate(get_img(imagepath, isFake)):
            new_img.paste(img, ((i%m) * size, (i//m) * size))
    elif order == 'vertical':
        for i, img in enumerate(get_img(imagepath, isFake)):
            new_img.paste(img, ((m - i//n - 1) * size, (i%n) * size))
    else:
        raise Exception(f'Expect order to be horizontal or vertical. Get {order} instead.')
    
    mkdir(outputpath)
    new_img.save(os.path.join(outputpath, 'combined.png'))