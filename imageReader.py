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

def splitImageEvenly(img, s_width, s_height):
    '''Splits up an image into segments and returns a list of those segments.
       Segments are closest to the whole size and are center-oriented.'''
    assert s_width > 0 and s_height > 0
    x_offset = ((img.width / s_width) % 1) * s_width // 2
    y_offset = ((img.height / s_height) % 1) * s_height // 2
    x_count, y_count = (img.width // s_width), (img.height // s_height)
    assert x_count > 0 and y_count > 0

    print("x_count =", x_count, "y_count =", y_count)

    segment_list = []
    for x in range(x_count):
        for y in range(y_count):
            print((x * s_width + x_offset, y * s_height + y_offset,
                               (x + 1) * s_width + x_offset, (y + 1) * s_height + y_offset))
            segment_list.append(img.crop((x * s_width + x_offset, y * s_height + y_offset,
                               (x + 1) * s_width + x_offset, (y + 1) * s_height + y_offset)))
    return segment_list


#debugging area
im = Image.open("test.jpg")
im.show()

seg_list_test = splitImageEvenly(im, 50, 50)
for entry in seg_list_test:
    entry.show()

#dir_list = getAllNamesFromDir(r'C:\Users\Devastator\Pictures\testing_series')
#print(dir_list, '\n\n')

#img_list = getImagesFromDirList(dir_list, 50, 50, 256)
#output = test_combine(img_list, 1000, 1000, 50)
#output.show()
