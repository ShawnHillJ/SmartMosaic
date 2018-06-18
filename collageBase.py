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

    
    
    def __init__(self, source, imagetuple):
        assert type(source) == str
        assert type(imagetuple) == tuple
        assert type(imagetuple[0]) == 

        self.sourceImage = source
        self.scaledSource = None
        self.sampleImagesNamelist = imagelist
        self.sampleImages = None
        
        return

    def loadImageSource(self, source):
    '''Overrides the current source (root) image for the mosaic.'''
    

    def loadImages(self, imageList):
    '''Loads in a sequence of images into the collage object.'''
        self.sampleImages = imageList
        return
        
    def generateMosaic(self, outputName)
    ''' Generates a collage and outputs the image as a file
        with the name given as an argument.'''

        
    ''' make new image: PIL.Image.new(mode, size, color=0)
        
