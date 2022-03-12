#===============================================================================
# PNG file class
# Author: Matthew JS Park
#===============================================================================

import base_file


class JpgFile( base_file.BaseFile ):
    '''
    JPG file class
    '''

    def __init__( self, path ):
        '''
        jpg file constructor
        :param path:(str) jpg file path
        '''
        super( JpgFile, self ).__init__( path )

