#===============================================================================
# #!/usr/bin/env python
#===============================================================================

import os, re
import cPickle as pickle
import json
import logging
from collections import OrderedDict

from maya import cmds



class ToolData( object ):
    '''
    ToolData
    '''
    PKL_TYPE = "data"
    JSON_TYPE = "json"
    SERIALIZE = True


    @classmethod
    def load_data(cls, file_path=None):
        '''
        load data method
        '''
        missing_msg = "[Failure]: No data found"
        data = None
        
        if cls.SERIALIZE:
            file_path = ".".join([file_path, cls.PKL_TYPE])
            if not cls.data_exist(file_path):
                print missing_msg
                return
            with open(file_path, "rb") as dataHandle:
                data = pickle.load(dataHandle)
        else:
            file_path = ".".join([file_path, cls.JSON_TYPE])
            if not cls.data_exist(file_path):
                print missing_msg
                return
            with open(file_path, "r") as dataHandle:
                data = json.load(dataHandle, object_pairs_hook=OrderedDict)
                
        return data
            
            
    @classmethod
    def data_exist(cls, file_path):
        return os.path.isfile(file_path)
    
    
    
    
    



