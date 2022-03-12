#===============================================================================
# Base file class
# Author: Matthew JS Park
#===============================================================================

import os


class BaseFile( object ):
    '''
    Base file class
    '''
    FILE_NAME = 'file name'
    FILE_TYPE = 'file type'
    FILE_PATH = 'file path'

    def __init__( self, filePath ):
        '''
        file constructor
        :param path:(str) file path
        '''
        super( BaseFile, self ).__init__()
        self._filePath = filePath

    def __repr__( self ):
        return '%s' % ( self.fileMap )

    def __str__( self ):
        return '(%s)%s.%s' % ( self.__class__.__name__, self.name, self.fileType )

    @property
    def filePath( self ):
        return os.path.normpath( os.path.normcase( self._filePath ) )

    @property
    def fileName( self ):
        return os.path.basename( self.filePath )

    @property
    def name( self ):
        return self.fileName.rsplit( '.' )[0]

    @property
    def fileType( self ):
        return self.fileName.rsplit( '.' )[-1]

    @property
    def fileMap( self ):
        return {
            self.FILE_NAME:self.name,
            self.FILE_TYPE:self.fileType,
            self.FILE_PATH:self.filePath,
        }

    def get_dirname( self ):
        return os.path.dirname( self.filePath )

