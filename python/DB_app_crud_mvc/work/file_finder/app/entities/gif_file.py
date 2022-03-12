#===============================================================================
# PNG file class
# Author: Matthew JS Park
#===============================================================================

import base_file


class GifFile( base_file.BaseFile ):
    '''
    GIF file class
    '''

    def __init__( self, path ):
        '''
        gif file constructor
        :param path:(str) gif file path
        '''
        super( GifFile, self ).__init__( path )
