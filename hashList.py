# hashList.py
# Includes a hashlist implementation for Images

from PIL import Image

class ImageHashList:
    def __init__(self, hashing_func, list_size, input_list=None):
        ''' Creates a HashList for PIL Images.
            Keys are stored as tuples containing color mode, Image object, and times retrieved.'''
        self.hash_function = hashing_func
        self.list_size = list_size
        self.hashlist = ([] for x in range(list_size))
        if input_list != None:
            for item in input_list:
                self.hashlist[self.hash_function(item[0])].append((item[0], item[1], 0))                      
                
    def getImages(self, key):
        ''' Returns a list of all images at hash of hashlist using a color tuple as a key. ''' 
        assert type(key) == tuple and len(key) == 3
        assert 0 <= max(key) <= 256
        return self.hashlist[self.hash_function(key)]

    def addImage(self, item):
        '''Adds an item to the hashlist at the hash. Takes a tuple containing the color and Image. '''
        assert type(item) == tuple and len(item) == 2
        assert 0 <= max(item[0]) <= 256
        assert type(item[1]) == Image
        self.hashlist[self.hash_function(item[0])].append((item[0], item[1], 0))
        
    def resetCounts(self):
        ''' Resets the access count of each item in the hashlist. '''
        for section_list in self.hashlist:
            for tup in section_list:
                tup[2] = 0

        
