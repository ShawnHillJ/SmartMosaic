# imageReader.py
# Holds functions important to reading in files from stored memory.

from PIL import Image
import os

def getAllNamesFromDir(directory):
    '''Returns a tuple of all the filepaths of the compatible pictures in the directory.'''
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            files.append(directory + r'\\' + filename)
    return files

def getImagesFromDirList(filelist, new_width, new_height, num_of_colors):
    '''Returns an Image list of the filelist, scaled to the new sizes.'''
    imagelist = []
    for filename in filelist:
        imagelist.append(Image.open(filename))

    scaledlist = []
    for item in imagelist:
        #new_img = item.quantize(num_of_colors)
        scaledlist.append(new_img.resize((new_width, new_height)))

    return scaledlist
