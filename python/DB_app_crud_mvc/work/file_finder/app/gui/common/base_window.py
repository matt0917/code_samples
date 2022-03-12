"""
Base window
Author: Matthew JS Park
Date: 02/18/2022
Usage: Base Window as template style cascades to sub-class widgets
"""

import os

from PySide.QtGui import ( QMainWindow, QDesktopWidget,
                          QSpacerItem, QSizePolicy )


class BaseWindow( QMainWindow ):
    '''
    File Finder Main Window
    '''

    TITLE = "Base Window"
    OBJ_NAME = "BASE WIN"
    WIDTH = 300
    HEIGHT = 300
    STYLE_NAME = "default_style"

    S_PATH = os.path.abspath( os.path.join( __file__, '..', '..', 'styles' ) )

    def __init__( self, parent = None, icon = None ):
        '''
        Base window
        '''
        super( BaseWindow, self ).__init__( parent )
        self.setWindowTitle( self.TITLE )
        self.setObjectName( self.OBJ_NAME )
        self.win_icon = icon

        self.create_widgets()
        self.set_layout()
        self.set_action()
        self._set_style( self.STYLE_NAME, self )

    def create_widgets( self ):
        '''
        base widget setup
        '''
        if self.win_icon:
            self.setWindowIcon( self.win_icon )

    def set_layout( self ):
        '''
        set layout virtual
        '''
        raise NotImplementedError( self.__class__.__name__ + ".set_layout" )

    def set_actions( self ):
        '''
        set action virtual
        '''
        raise NotImplementedError( self.__class__.__name__ + ".set_actions" )

    def showEvent( self, event ):
        self._center()

    def _center( self ):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move( ( screen.width() - size.width() ) / 2,
                  ( screen.height() - size.height() ) / 2 )

    def _set_style( self, style_name, widget ):
        '''
        set widget style to cascade to all other widgets
        :param style_name: name of the style file
        :param [widget] widget to override style.
        '''
        sFile = "%s.qss" % ( style_name )
        sPath = os.path.abspath( os.path.join( self.S_PATH, sFile ) )
        with open( sPath, "r" ) as f:
            widget.setStyleSheet( f.read() )

    def vSpacer( self, w = 16, h = 16 ):
        '''
        add vertical spacer
        :param w: width
        :param h: height
        '''
        vSpacer = QSpacerItem( 
            w, h, QSizePolicy.Minimum, QSizePolicy.Expanding )
        return vSpacer

    def hSpacer( self, w = 16, h = 16 ):
        '''
        add horizontal spacer
        :param w: width
        :param h: height
        '''
        hSpacer = QSpacerItem( 
            w, h, QSizePolicy.Expanding, QSizePolicy.Minimum )
        return hSpacer
