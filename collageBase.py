#basic collage class

from PIL import Image
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
        
        return

    def loadImageSource(self, source):
        '''Overrides the current source (root) image for the mosaic.'''
        self.sourceImage = source

    def loadImages(self, imageList):
        '''Loads in a sequence of images into the collage object.'''
        self.sampleImagesNamelist = imageList

    def _scale_images(self):
        ''' Loads in the images for sampleImages. '''
        self.sampleImages = imageReader.getImagesFromDirList(self.sampleImagesNamelist,
                            self.sampleScale, self.sampleScale, self.colorQuality)
        
    def _scale_source(self):
        ''' Scales the source image for the output.
        '''
        temp = Image.open(self.sourceImage)
        self.scaledSource = temp.resize((self.outputWidth, self.outputHeight))

    def generateOverlayMosaic(self, output):
        ''' Generates a mosaic using the simple overlay method.
        Outputs the image as a file with the name given as
        an argument.

        still in-progress
        '''
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
                mosaic_img.paste(self.sampleImages[(y + (x * (width//offset))) % len(self.sampleImages)], (x * offset, y * offset))
                self.debug_float = (y + (x * (width//offset))) / ((width//offset) * (height//offset))

        print(self.scaledSource.size, mosaic_img.size)
        print(self.scaledSource.mode, mosaic_img.mode)
        
        output_image = Image.blend(self.scaledSource, mosaic_img, 0.3)
        output_image.save(output)

        
    # make new image: PIL.Image.new(mode, size, color=0)
        
#testing area
#images = imageReader.getAllNamesFromDir('C:\\Users\\OWNER\\Pictures\\flat_colors')
#base = MosaicBase(r'C:\Users\OWNER\Pictures\harold.png', images, 300, 300, 30)
#base.generateOverlayMosaic(r'..\testing.png')
