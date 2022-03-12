#===============================================================================
# business logic: file data input validation
# Author: Matthew JS Park
# Usage: assesment file object and returns back repo validation result
#===============================================================================


class Validation( object ):
    '''
    file object validation class
    '''

    def __init__( self, fileObjects ):
        '''
        constructor
        :param fileObject: file objects
        '''
        if not hasattr( fileObjects, '__iter__' ):
            fileObjects = [fileObjects]
        self.fileObjects = fileObjects
        self.invalidObjects = []
        self.validObjects = []
        self.invalid_count = 0

        self.validation()

    @property
    def validation_map( self ):
        validationMap = {
            'invalid': self.invalid_count,
            'valid_object': self.validObjects,
            'invalid_object': self.invalidObjects,
            }
        return validationMap

    def validation( self ):
        '''
        method validating file objects
        '''
        for vObj in self.fileObjects:
            i_count = 0
            i_count += 0 if isinstance( vObj.name, str ) else 1
            i_count += 0 if isinstance( vObj.filePath, str ) else 1
            i_count += 0 if isinstance( vObj.fileType, str ) else 1
            if i_count:
                self.invalidObjects.append( vObj )
                self.invalid_count += 1
            else:
                self.validObjects.append( vObj )

