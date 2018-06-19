#basic collage class

from PIL import Image

class MosaicBase:
''' This class does the basic operation of
    loading in an iterative full of Image
    objects at the specified resolution.
    When the images are loaded in, generateCollage
    can be called to arrange the images into a
    collage.

    "/source_images"
    
'''

    
    
    def __init__(self, source, imagelist, out_width=100, out_height=100, sam_size=10):
        assert type(source) == str
        assert type(imagelist) == list
        assert type(imagetuple[0]) == str

        self.debug_float = 0.0
        self.sourceImage = source
        self.scaledSource = None
        self.sampleImagesNamelist = imagelist
        self.sampleImages = None
        self.sampleScale = sam_size
        self.outputWidth, self.outputHeight = out_width, out_height
        
        return

    def loadImageSource(self, source):
    '''Overrides the current source (root) image for the mosaic.'''
        self.sourceImage = source

    def loadImages(self, imageList):
    '''Loads in a sequence of images into the collage object.'''
        self.sampleImagesNamelist = imageList
        
    def generateOverlayMosaic(self, output)
    ''' Generates a mosaic using the simple overlay method.
        Outputs the image as a file with the name given as
        an argument.

        still in-progress
    '''
        offset = self.sampleScale
        width, height = self.outputWidth, self.outputHeight
        self.debug_float = 0.0
        out_image = Image.new("RGB", (width, height))
        print(len(self.sampleImages))
        for x in range(width // offset):
            print(debug_float)
            for y in range(height // offset):
                out_image.paste(self.sampleImages[(y + (x * (width//offset))) % len(self.sampleImages)], (x * offset, y * offset))
                self.debug_float = (y + (x * (width//offset))) / ((width//offset) * (height//offset))

       out_image.convert(mode="RGBa")

       overlay = Image.new("RGBa")

       out_image.convert(mode="RGB")
       out_image.save(output)

        
    # make new image: PIL.Image.new(mode, size, color=0)
        
