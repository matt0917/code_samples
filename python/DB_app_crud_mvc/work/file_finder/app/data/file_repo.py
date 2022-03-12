#===============================================================================
# This is the module handling sql database's DDL and DML.
# Module is using Sqlite3 python API to access SQLite engine
# Author: Matthew JS Park
# Usage: excute DDL, DML
#===============================================================================
import os

import sqlite3

import file_finder

from file_finder.app.business.validation import Validation


class FileRepo( object ):
    '''
    File Repository class
    Execute DDL and DML with data validation
    '''

    CONN_STRING = os.path.normpath( os.path.join( file_finder.__path__[0], 'found_files.db' ) )
    MEM = ':memory:'
    OPTION_MAP = {
        0: CONN_STRING,
        1: MEM,
        }
    OPTION = 0
    CONN = sqlite3.connect( OPTION_MAP[OPTION] )

    TABLE_NAME = "ImageFiles"

    cur = CONN.cursor()

    # attributes
    FILENAME = 'file_name'
    FILEPATH = 'file_path'
    FILETYPE = 'file_type'

    def __init__( self, fileObjects = [] ):
        '''
        constructor
        :param fileObject: file object
        '''
        self._fileObjects = fileObjects

    def __new__( cls, node, *args, **kwargs ):
        if cls.__name__ == node.__class__.__name__:
            return node
        return object.__new__( cls, node, *args, **kwargs )

    @property
    def fileObjects( self ):
        return self._fileObjects

    @classmethod
    def create_file_table( cls ):
        create_string = """
                        CREATE TABLE {0} (
                         {1} text,
                         {2} text,
                         {3} text
                        )""".format( cls.TABLE_NAME, cls.FILENAME, cls.FILEPATH, cls.FILETYPE )
        with cls.CONN:
            cls.cur.execute( create_string )

    def add_file_data( self ):
        '''
        Insert file data
        :param fileObject:
        '''
        validation_result = Validation( self.fileObjects ).validation_map
        invalidObjects = validation_result['invalid_object']
        invalid = validation_result['invalid']
        if invalid:
            print ( 'There is invalid file data found to add to the database!' )
            print ( 'Invalid file count: {0}'.format( invalid ) )
            print ( ' Invalid file list: ' )
            for fObj in invalidObjects:
                print ( fObj.filePath )
            return invalidObjects
        query = """
                INSERT INTO {0} VALUES(
                :{1},
                :{2},
                :{3}
                )""".format( self.TABLE_NAME, self.FILENAME, self.FILEPATH, self.FILETYPE )
        with self.CONN:
            for vObj in validation_result['valid_object']:
                self.cur.execute( query, {self.FILENAME: vObj.name,
                                          self.FILEPATH:vObj.filePath,
                                          self.FILETYPE:vObj.fileType} )

    @classmethod
    def get_all_file_data( cls ):
        '''
        Get File data from the database
        '''
        query = """
                SELECT *
                FROM {0}
                """.format( cls.TABLE_NAME )
        cls.cur.execute( query )
        return cls.cur.fetchall()

    @classmethod
    def get_file_data_by_type( cls, fileType ):
        '''
        Get file data by file type
        :param cls:
        '''
        query = """
                SELECT *
                FROM {0}
                WHERE {1}=:fileType
                """.format( cls.TABLE_NAME, cls.FILETYPE )
        cls.cur.execute( query, {'fileType': fileType} )
        return cls.cur.fetchall()

    @classmethod
    def get_file_data_by_column( cls, column ):
        '''
        Get file data by file type
        :param cls:
        '''
        query = """
                SELECT DISTINCT {2}
                FROM {0}
                """.format( cls.TABLE_NAME, cls.FILETYPE, column )
        cls.cur.execute( query )
        return cls.cur.fetchall()

    @classmethod
    def test_run( cls ):
        from file_finder.app.entities.png_file import PngFile
        pngObj = [PngFile( 'C:/work/file_finder/files/101_001_001/test001.png' ),
                  PngFile( 'C:/work/file_finder/files/101_001_001/test002.png' ),
                  PngFile( 'C:/work/file_finder/files/101_001_001/test003.png' ),
                  PngFile( 'C:/work/file_finder/files/101_001_001/test004.png' )]
        repo = cls( pngObj )
        repo.create_file_table()
        repo.add_file_data()

        data = repo.get_all_file_data()
        for d in data:
            print ( d )
        print ( '\n\r' )
        data1 = repo.get_file_data_by_type( 'png' )
        for d in data1:
            print ( d )


if __name__ == '__main__':

    FileRepo.test_run()

