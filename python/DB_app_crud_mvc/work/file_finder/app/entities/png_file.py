#===============================================================================
# PNG file class
# Author: Matthew JS Park
#===============================================================================

import base_file


class PngFile( base_file.BaseFile ):
    '''
    JPG file class
    '''

    def __init__( self, path ):
        '''
        png file constructor
        :param path:(str) png file path
        '''
        super( PngFile, self ).__init__( path )
