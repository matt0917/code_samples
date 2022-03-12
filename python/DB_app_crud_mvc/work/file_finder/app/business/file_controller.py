#===============================================================================
# file view module
# Author: Matthew JS Park
# usage: receiving gui request, find files and returns typed_file object list
#===============================================================================
import os

from file_finder.app.entities import ( png_file, jpg_file, gif_file )

import file_util as fUtil


class FileController( object ):
    '''
    FileController class
    includes:
    file searching handling
    file submitting handling
    '''
    FILE_TYPE_MAP = {
        '*': None,
        None: None,
        'png': png_file.PngFile,
        'jpg': jpg_file.JpgFile,
        'jpeg': jpg_file.JpgFile,
        'gif': gif_file.GifFile,
        }

    def __init__( self, fileType ):
        '''
        constructor
        '''
        self.fileDir = os.path.join( os.path.dirname( __file__ ), '..', '..', 'files' )
        self.fileType = fileType
        self._fileObjects = list()
        self._fileCount = None

    @property
    def fileObjects( self ):
        '''
        returns file objects
        '''
        return self._fileObjects

    @property
    def fileCount( self ):
        '''
        returns the typed-file count
        '''
        if not self._fileCount:
            self._fileCount = len( self.fileObjects )
        return self._fileCount

    def search_fileType( self ):
        '''
        search a type of files
        '''
        fileMod = self.FILE_TYPE_MAP[self.fileType]
        fileList = fUtil.get_files_by_type( self.fileDir, self.fileType )
        if not fileMod:
            fileList = sorted( fileList, key = lambda x: os.path.splitext( x )[1] )
        for filePath in fileList:
            fObj = None
            if not fileMod:
                ext = filePath.rsplit( '.' )[-1].lower()
                fileMod = self.FILE_TYPE_MAP[ext]
            fObj = fileMod( filePath )
            self._fileObjects.append( fObj )
        return self._fileObjects


if __name__ == '__main__':
    fileType = None
    controller = FileController( fileType )
    controller.search_fileType()
    for each in controller.fileObjects:
        print ( repr( each ) )
