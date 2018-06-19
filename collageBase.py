#basic collage class

from PIL import Image
from random import randint
import imageReader

class MosaicBase:
    ''' This class does the basic operation of
    loading in an iterative full of Image
    objects at the specified resolution.
    When the images are loaded in, generateCollage
    can be called to arrange the images into a
    collage.

    "/source_images"'''
    
    def __init__(self, source, imagelist, out_width=100,
                 out_height=100, sam_size=10, colors=256):
        assert type(source) == str
        assert type(imagelist) == list
        assert (type(imagelist[0]) == str)
        self.debugfloat = None
        self.sourceImage = source
        self.scaledSource = None
        self.sampleImagesNamelist = imagelist
        self.sampleImages = None
        self.sampleScale = sam_size
        self.outputWidth, self.outputHeight = out_width, out_height
        self.colorQuality = colors
        self.samplesLoaded = False
        
        return

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
            self.sampleImages = imageReader.getImagesFromDirList(self.sampleImagesNamelist,
                                self.sampleScale, self.sampleScale, self.colorQuality)
            self.samplesLoaded = True
        
    def _scale_source(self):
        ''' Scales the source image for the output.'''
        temp = Image.open(self.sourceImage)
        self.scaledSource = temp.resize((self.outputWidth, self.outputHeight))

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
        print(len(self.sampleImages))
        for x in range(width // offset):
            print(self.debug_float)
            for y in range(height // offset):
                mosaic_img.paste(self.sampleImages[randint(0, len(self.sampleImages) - 1)], (x * offset, y * offset))
                self.debug_float = (y + (x * (width//offset))) / ((width//offset) * (height//offset))

        print(self.scaledSource.size, mosaic_img.size)
        print(self.scaledSource.mode, mosaic_img.mode)
        
        output_image = Image.blend(self.scaledSource, mosaic_img, blend_factor)
        output_image.save(output)

    def generateTintedPhotoMosaic(self, output):
        '''Generates a mosaic using the sample images as color pieces for the mosaic.
           This method tints each photo to the mode of the color at the section it
           replaces in the source photo at random.'''
        pass

    def generateSmartTintedPhotoMosaic(self, output):
        '''Generates a mosaic using the sample images as color pieces for the mosaic.
           This method attempts to find the closest relatives from the samples and
           creates a pallette using those. This method is not guaranteed to be
           evenly distributed.'''
        pass

    def generateBlendedOverlayWithSmartTintMosaic(self, output, blend_factor):
        '''Generates a mosaic that is a blend of the Smart Tint with an overlay of
           the source image.'''
        pass
    
    
        
#testing area
images = imageReader.getAllNamesFromDir('C:\\Users\\OWNER\\Pictures\\flat_colors')
base = MosaicBase(r'C:\Users\OWNER\Pictures\harold.png', images, 300, 300, 30)
base.generateOverlayMosaic(r'..\testing.png', 0.4)
