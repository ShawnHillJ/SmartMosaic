from PIL import Image
import os

def getAllNamesFromDir(directory):
    '''Returns a tuple of all the filepaths of the files in the directory.'''
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
        new_img = item.quantize(num_of_colors)
        scaledlist.append(new_img.resize((new_width, new_height)))
    del imagelist
    return scaledlist

def getModeColor(img):
    '''Returns the Mode color value of an Image object.'''
    colorCount = img.getcolors()
    colorCount.sort()
    return colorCount[len(colorCount) - 1][1]


#debugging area
#im = Image.open("test.jpg")
#im.show()
'''
dir_list = getAllNamesFromDir(r'C:\Users\Devastator\Pictures\testing_series')
print(dir_list, '\n\n')

img_list = getImagesFromDirList(dir_list, 50, 50, 256)
output = test_combine(img_list, 1000, 1000, 50)
output.show()
'''
