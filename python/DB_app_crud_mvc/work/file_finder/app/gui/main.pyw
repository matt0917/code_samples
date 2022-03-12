# !/usr/bin/python
"""
File Finder Main Window
Author: Matthew JS Park
Date: 02/18/2022
Usage: File Finder GUI to provide following args to biz to insert attributes to a simple file entity :
- select various file extensions in a comboBox
- list of files found from searching a file format by pressing the 'search' button
- Simply submit all files in the list widget to a DB table by pressing the 'submit' button
"""

from functools import partial
import os
import sys

from PySide.QtCore import Qt
from PySide.QtGui import ( QApplication, QDialog, QIcon, QVBoxLayout, QHBoxLayout )

from common import base_window
from common.base_widgets import ( ComboBox, Label, ListWidget, PushButton )
from file_finder.app.business import file_controller
from file_finder.app.data import file_repo


class FileFinderWin( base_window.BaseWindow ):
    '''
    File Finder Main Window
    '''

    TITLE = "File Finder"
    OBJ_NAME = "MainWin"
    WIDTH = 810
    HEIGHT = 470
    WIDTH_B = 150
    FONT_SIZE_B = 20
    LIST_SIDE_MARGIN = 35
    RESULT_TEXT = 'Found Files: {0:d}'
    SUBMITTED_TEXT = 'Submitted {0:d}-files to DB!'

    WIN_ICON_NAME = 'file_finder_32.png'
    ICON_DIR = os.path.join( os.path.dirname( __file__ ), 'icons' )
    WIN_ICON_PATH = os.path.normpath( os.path.join( ICON_DIR, WIN_ICON_NAME ) )

    FILE_TYPES = ['png', 'jpg', 'gif']

    def __init__( self, parent = None ):
        '''
        window constructor
        :param parent: (QWidget), (QObject)
        '''
        self.win_icon = QIcon( self.WIN_ICON_PATH )
        super( FileFinderWin, self ).__init__( parent, self.win_icon )

        self.controller = file_controller.FileController
        self.repo = file_repo.FileRepo

    def create_widgets( self ):
        '''
        Create widgets
        '''
        super( self.__class__, self ).create_widgets()
        self.main_vLayout = QVBoxLayout()
        self.combo_hLayout = QHBoxLayout()
        self.search_hLayout = QHBoxLayout()
        self.result_hLayout = QHBoxLayout()
        self.fileList_vLayout = QVBoxLayout()
        self.bottom_hLayout = QHBoxLayout()

        self.main_widget = QDialog()
        self.main_widget.setMinimumSize( self.WIDTH, self.HEIGHT )
        # widget components in ordered from top to bottom
        self.top_spacer = self.vSpacer()
        self.fileType_label = Label( text = "File Type" )
        # combo box
        self.combo_lspacer = self.hSpacer()
        self.file_combo = ComboBox( items = self.FILE_TYPES )
        self.combo_rspacer = self.hSpacer()
        # search btn
        self.search_lspacer = self.hSpacer()
        self.search_btn = PushButton( text = 'Search' )
        self.search_rspacer = self.hSpacer()
        # result label
        self.result_lspacer = self.hSpacer()
        self.result_text = Label( text = self.RESULT_TEXT.format( 0 ) )
        self.result_rspacer = self.hSpacer()
        # file list widget
        self.file_listWidget = ListWidget()
        # submit btn
        self.submit_lspacer = self.hSpacer()
        self.submit_btn = PushButton( text = 'Submit' )

        self.set_pref()

    def set_pref( self ):
        '''
        set preference of widgets
        '''
        self.top_spacer.changeSize( 10, 10 )
        self.fileType_label.align_hcenter()
        self.file_combo.setMinimumSize( self.WIDTH_B, 32 )
        self.result_text.setMinimumHeight( 40 )
        self.result_text.align_bottom()
        self.fileList_vLayout.setContentsMargins( self.LIST_SIDE_MARGIN, 0, self.LIST_SIDE_MARGIN, 0 )
        self.file_listWidget.setMinimumHeight( 200 )
        # buttns' preferences
        for btn in [self.search_btn, self.submit_btn]:
            btn.setMinimumSize( self.WIDTH_B, 50 )
            btn.set_fnt_size( self.FONT_SIZE_B )
            btn.set_fnt_weight( PushButton.BOLD )
        self.submit_btn.setDisabled( 1 )

    def set_layout( self ):
        '''
        Set layout of widgets
        '''
        self.main_vLayout.addItem( self.top_spacer )
        self.main_vLayout.addWidget( self.fileType_label )
        self.main_vLayout.addLayout( self.combo_hLayout )
        self.main_vLayout.addLayout( self.search_hLayout )
        self.main_vLayout.addLayout( self.result_hLayout )
        self.main_vLayout.addLayout( self.fileList_vLayout )

        self.combo_hLayout.addItem( self.combo_lspacer )
        self.combo_hLayout.addWidget( self.file_combo )
        self.combo_hLayout.addItem( self.combo_rspacer )

        self.search_hLayout.addItem( self.search_lspacer )
        self.search_hLayout.addWidget( self.search_btn )
        self.search_hLayout.addItem( self.search_rspacer )

        self.result_hLayout.addItem( self.result_lspacer )
        self.result_hLayout.addWidget( self.result_text )
        self.result_hLayout.addItem( self.result_rspacer )

        self.fileList_vLayout.addWidget( self.file_listWidget )
        self.fileList_vLayout.addLayout( self.bottom_hLayout )

        self.bottom_hLayout.addItem( self.submit_lspacer )
        self.bottom_hLayout.addWidget( self.submit_btn )

        self.main_widget.setLayout( self.main_vLayout )

        self.setCentralWidget( self.main_widget )

    def set_action( self ):
        self.search_btn.clicked.connect( partial( self.search_files, self.file_combo ) )
        self.submit_btn.clicked.connect( self.submit_files )

    # actions
    def update_result_text( self, new_text ):
        '''
        update file found result count

        :param newCount:(int) new count
        '''
        self.result_text.setText( new_text )

    def search_files( self, widget ):
        '''
        search files and instantiate file objects
        :param widget:(QWidget) reference widget
        '''
        self.file_listWidget.clear()
        fileType = widget.currentText()
        controller = self.controller( fileType )
        fileObjects = controller.search_fileType()
        for fObj in fileObjects:
            self.file_listWidget.add_item( fObj.filePath, data = fObj, alignment = 4 )
        self.update_result_text( self.RESULT_TEXT.format( controller.fileCount ) )
        self.submit_btn.setDisabled( 0 )

    def submit_files( self ):
        '''
        submit found files on the list
        '''
        fileCount = self.file_listWidget.count()
        data = []
        for i in range( fileCount ):
            curItem = self.file_listWidget.item( i )
            data.append( curItem.data( 1 ) )
        self.repo = file_repo.FileRepo( data )
        try:
            self.repo.add_file_data()
        except:
            print ( 'Data is already submitted. You need to search files again in order to submit the DB' )
            return
        # fetching data back to the list widget
        self.file_listWidget.clear()
        fetched_data = self.repo.get_file_data_by_column( self.repo.FILEPATH )
        for fd in fetched_data:
            fd = os.path.normpath( fd[0] )
            self.file_listWidget.add_item( fd , alignment = 4 , color = Qt.GlobalColor.green )
        self.update_result_text( self.SUBMITTED_TEXT.format( fileCount ) )
        print ( 'File submission to DB has succeeded!' )

    def showEvent( self, event = None ):
        self._center()

    def closeEvent( self, event = None ):
        self.repo.cur.close()
        self.repo.CONN.close()

    def _center( self ):
        super( self.__class__, self )._center()


if __name__ == '__main__':
    # create file table
    file_repo.FileRepo.create_file_table()
    # main gui
    QApplication.setDesktopSettingsAware( True )
    app = QApplication( sys.argv )
    main_win = FileFinderWin()
    main_win.show()
    app.exec_()
    # Delete found_files.db
    if os.path.isfile( file_repo.FileRepo.CONN_STRING ):
        os.remove( file_repo.FileRepo.CONN_STRING )
