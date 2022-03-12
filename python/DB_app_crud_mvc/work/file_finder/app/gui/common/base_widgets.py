#===============================================================================
# Base Widget
# Matthew JS Park
#===============================================================================

from PySide.QtCore import Qt
from PySide.QtGui import ( QComboBox, QLabel, QTextBrowser, QTextEdit,
                          QPushButton, QListWidget, QListWidgetItem, QBrush )


class BaseWidget( object ):
    '''
    My BaseWidget class
    '''
    DEF_COLOR = "f0f0f0"
    DEF_SIZE = 12
    NORMAL = "normal"
    BOLD = "bold"
    WEIGHT_MAP = {
        0: NORMAL,
        1: BOLD
    }
    c = ';'
    styles = []

    def set_color( self, color = None ):
        if not color:
            color = self.DEF_COLOR
        self.styles.append( "color:#{}".format( color ) )
        self.setStyleSheet( self.c.join( self.styles ) )

    def set_bg_color( self, color = None ):
        if not color:
            color = self.DEF_COLOR
        self.styles.append( "background-color:#{}".format( color ) )
        self.setStyleSheet( self.c.join( self.styles ) )

    def set_fnt_size( self, size = None ):
        if not size:
            size = self.DEF_SIZE
        self.styles.append( "font-size:{}px".format( size ) )
        self.setStyleSheet( self.c.join( self.styles ) )

    def set_fnt_weight( self, weight = None ):
        if not weight:
            weight = self.WEIGHT_MAP[0]
        self.styles.append( "font-weight:{}".format( weight ) )
        self.setStyleSheet( self.c.join( self.styles ) )


class ComboBox( QComboBox, BaseWidget ):

    def __init__( self, parent = None, items = None ):
        super( ComboBox, self ).__init__( parent )
        self.items = items
        if items is not None:
            if not hasattr( items, '__iter__' ):
                self.items = [items]
        if self.items:
            self.addItems( self.items )


class Label ( QLabel, BaseWidget ):

    def __init__( self, parent = None, text = None ):
        super( Label, self ).__init__( parent )

        self.setText( text )

    def align_left( self ):
        self.setAlignment( Qt.AlignLeft )

    def align_right( self ):
        self.setAlignment( Qt.AlignRight )

    def align_hcenter( self ):
        self.setAlignment( Qt.AlignHCenter )

    def align_justify( self ):
        self.setAlignment( Qt.AlignJustify )

    def align_top( self ):
        self.setAlignment( Qt.AlignTop )

    def align_bottom( self ):
        self.setAlignment( Qt.AlignBottom )

    def align_vcenter( self ):
        self.setAlignment( Qt.AlignVCenter )


class TextBrowser( QTextBrowser, BaseWidget ):

    def __init__( self, parent = None, text = None ):
        super( TextBrowser, self ).__init__( parent )

        self.setText( text )


class TextEdit( QTextEdit, BaseWidget ):

    def __init__( self, parent = None, text = None, readOnly = False ):
        super( TextEdit, self ).__init__( parent )

        self.setText( text )
        self.setReadOnly( readOnly )


class PushButton( QPushButton, BaseWidget ):

    def __init__( self, parent = None, text = None ):
        super( PushButton, self ).__init__( parent )

        self.setText( text )


class ListWidget( QListWidget, BaseWidget ):

    def __init__( self, parent = None, itemTextList = [] ):
        super( ListWidget, self ).__init__( parent )
        if itemTextList:
            self.insert_items( itemTextList )

    def add_item( self, itemText, toolTip = None, data = None, alignment = 0, color = None ):
        '''
        Add QList widget item
        :param itemText:(str) item name
        :param [toolTip]:(str) optional item tip
        :param [data]:(map) optional item data to store
        :param [alignment]:(int) text alignment value
        :param [color]:(str) text color style
        '''
        newItem = QListWidgetItem()
        newItem.setText( itemText )
        newItem.setTextAlignment( alignment )
        if color:
            newItem.setForeground( QBrush( color ) )
        if data:
            newItem.setData( 1, data )
        if toolTip:
            newItem.setToolTip( toolTip )
        self.addItem( newItem )

    def add_items( self, itemTextList = None ):
        '''
        Insert a textList at once
        :param itemTextList: (list of string) text list to add to the widget
        '''
        for itemText in itemTextList:
            self.add_item( itemText )


if __name__ == '__main__':
    pass
