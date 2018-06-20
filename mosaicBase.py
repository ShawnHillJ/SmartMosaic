# mosaicBase.py
# Holds the MosaicBase class, which creates the photo mosaic.

from PIL import Image, ImageChops
from random import randint
from imageReader import *
from hashList import ImageHashList

class MosaicBase:
    ''' This class does the basic operation of loading in an iterative full of Image
    objects at the specified resolution. When the images are loaded in, generateCollage
    can be called to arrange the images into a collage.'''
    
    def __init__(self, source, imagelist, out_width=100,
                 out_height=100, sam_width=10, sam_height=10, color_bit_depth=256):
        assert type(source) == str
        assert type(imagelist) == list
        assert (type(imagelist[0]) == str)
        assert out_width > 0 and out_height > 0
        self.debugfloat = None
        self.result = None
        self.sourceImage = source
        self.scaledSource = None
        self.sampleImagesNamelist = imagelist
        self.sampleImages = None
        self.sampleWidth, self.sampleHeight = sam_width, sam_height
        self.outputWidth, self.outputHeight = out_width, out_height
        self.colorQuality = color_bit_depth
        self.samplesLoaded = False
        self.x_offset = ((self.sourceImage.width / s_width) % 1) * s_width // 2
        self.y_offset = ((self.sourceImage.height / s_height) % 1) * s_height // 2
        self.x_count, self.y_count = (self.outputWidth  // self.sampleWidth),\
                                     (self.outputHeight // self.sampleHeight)
        
    def loadImageSource(self, source):
        '''Overrides the current source (root) image for the mosaic.'''
        self.sourceImage = source

    def loadImages(self, imageList):
        '''Loads in a sequence of images into the collage object.'''
        self.sampleImagesNamelist = imageList
        self.samplesLoaded = False

    def _scale_images(self):
        ''' Loads in the images for sampleImages. '''
        if not self.samplesLoaded:
            self.sampleImages = getImagesFromDirList(self.sampleImagesNamelist,
                                self.sampleScale, self.sampleScale, self.colorQuality)
            self.samplesLoaded = True
        
    def _scale_source(self):
        ''' Scales the source image for the output.'''
        temp = Image.open(self.sourceImage)
        self.scaledSource = temp.resize((self.outputWidth, self.outputHeight))

    def _split_source_evenly(self):
        '''Splits up the source image into segments and returns a list of those segments.
           Segments are closest to the whole size and are center-oriented.'''
        segment_list = [[] for i in range(x)]
        for x in range(x_count):
            for y in range(y_count):
#                print((x * s_width + x_offset, y * s_height + y_offset,
#                                   (x + 1) * s_width + x_offset, (y + 1) * s_height + y_offset))
                segment_list[x].append(img.crop((x * s_width + x_offset, y * s_height + y_offset,
                                   (x + 1) * s_width + x_offset, (y + 1) * s_height + y_offset)))
        return segment_list

    def _get_mode_color(self, img):
        '''Returns the Mode color value of an Image object.'''
        colorCount = img.getcolors()
        colorCount.sort()
        return colorCount[len(colorCount) - 1][1]

    def exportImages(self, output_dir):
        ''' Exports the scaled sample images into the specified directory.'''
        if not self.samplesLoaded:
            self._scale_images()
        counter = '0'
        for img_object in self.sampleImages:
            img_object.save(output_dir + '\\' + counter.zfill(4) + '.jpg')
        
    def generateOverlayMosaic(self, output, blend_factor):
        ''' Generates a mosaic using the simple overlay method.
        Outputs the image as a file with the name given as
        an argument.'''
        self._scale_images()
        self._scale_source()
        
        offset = self.sampleScale
        width, height = self.outputWidth, self.outputHeight
        self.debug_float = 0.0
        mosaic_img = Image.new("RGBA", (width, height))
        for x in range(self.x_count):
            print(self.debug_float)
            for y in range(self.y_count):
                mosaic_img.paste(self.sampleImages[randint(0, len(self.sampleImages) - 1)],
                                 ((x * offset) + self.x_offset, (y * offset) + self.y_offset))
                self.debug_float = (y + (x * (self.x_count))) / ((self.x_count) ** 2)
        
        output_image = Image.blend(self.scaledSource, mosaic_img, blend_factor)
        output_image.putalpha(1)
        self.result = output_image

    def generateTintedPhotoMosaic(self):
        '''Generates a mosaic using the sample images as color pieces for the mosaic.
           This method tints each photo to the mode of the color at the section it
           replaces in the source photo at random.'''
        self._scale_images()
        self._scale_source()

        self.debug_float = 0.0
        mosaic_img = Image.new("RGBA", (self.outputWidth, self.outputHeight))

        sourceSections = self._split_source_evenly();

        for x in range(self.x_count):
            print(self.debug_float)
            for y in range(self.y_count):
                current_color = _get_mode_color(sourceSections[y + (x * self.x_count)])
                img_insert = ImageChops.multiply(self.sampleImages[randint(0, len(self.sampleImages) - 1)],\
                                 Image.new("RGBA", (self.outputWidth, self.outputHeight), current_color))
                mosaic_img.paste(img_insert, ((x * offset) + self.x_offset, (y * offset) + self.y_offset))

        self.result = mosaic_img

    def generateSmartTintedPhotoMosaic(self):
        '''Generates a mosaic using the sample images as color pieces for the mosaic.
           This method attempts to find the closest relatives from the samples and
           creates a pallette using those. This method is not guaranteed to be
           evenly distributed. If a close relative does not exist, a random image is
           chosen and tinted. '''

        self._scale_images()
        self._scale_source()
        
        self.debug_float = 0.0
        mosaic_img = Image.new("RGBA", (self.outputWidth, self.outputHeight))

        sourceSections = self._split_source_evenly();
        sourceSectionsFlat = [item for sublist in sourceSections for item in sublist]
        sourceColorImagePairs = zip((self._get_mode_color(img) for img in sourceSectionsFlat), sourceSectionsFlat)

        sampleMap = zip((self._get_mode_color(img) for img in self.sampleImages), self.sampleImages)
        sampleHash = ImageHashList(lambda tup: ((tup[0] // 16) * 256) + ((tup[1] // 16) * 16) + (tup[2] // 16),\
                                   self.colorQuality, sampleMap)

        for x in range(self.x_count):
            print(self.debug_float)
            for y in range(self.y_count):
                current_color = sourceColorImagePairs[(x * self.x_count) + y][0]
                current_img_list = sampleHash.getImages(current_color)
                
                if len(current_img_list) == 0:
                    img_insert = ImageChops.multiply(self.sampleImages[randint(0, len(self.sampleImages) - 1)],\
                                 Image.new("RGBA", (self.outputWidth, self.outputHeight), current_color))
                    mosaic_img.paste(img_insert, ((x * offset) + self.x_offset, (y * offset) + self.y_offset))

                else:
                    level_min = current_img_list[0][2]
                    current_choice = current_img_list[0]
                    for entry in current_img_list:
                        if level_min > entry[2]:
                            level_min = entry[2]
                            current_choice = entry

                    mosaic_img.paste(current_choice[1], ((x * offset) + self.x_offset, (y * offset) + self.y_offset))

        self.result = mosaic_img

    def generateBlendedOverlayWithSmartTintMosaic(self, output, blend_factor):
        '''Generates a mosaic that is a blend of the Smart Tint with an overlay of
           the source image.'''
        pass

    def outputResult(self, output):
       ''' Outputs the result to a file. '''
       self.result.save(output)

    def getResult(self):
       ''' Returns the result image, None if not generated. '''
       return self.result
    
    
        
#testing area
#images = getAllNamesFromDir('C:\\Users\\OWNER\\Pictures\\flat_colors')
#base = MosaicBase(r'C:\Users\OWNER\Pictures\harold.png', images, 300, 300, 30)
#base.generateOverlayMosaic(r'..\testing.png', 0.4)
