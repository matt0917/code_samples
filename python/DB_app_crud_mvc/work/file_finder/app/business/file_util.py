#===============================================================================
# Utility module for supporting file-search
#===============================================================================
import fnmatch
import os


def get_files_by_type( baseDir, fileType = None, recursive = True ):
    '''
    Get all files with a specific type
    :param baseDir:(str)
    :param [fileType]:(str)
    :param [recursive]:(bool) default:True
    :return fileList: list of files
    '''
    fileList = []
    fileType = fileType if fileType else "*"
    for dirpath, dirs, files in os.walk( baseDir ):
        for fileName in fnmatch.filter( files, '*.%s' % fileType ):
            fileList.append( os.path.join( dirpath, fileName ) )

    return fileList


if __name__ == '__main__':
    baseDir = os.path.join( os.path.dirname( __file__ ), '..', '..', 'files' )
    fileType = 'png'
    fileList = get_files_by_type( baseDir, fileType )
    for f in fileList:
        print ( f )
    print ( '%d files found' % len( fileList ) )
