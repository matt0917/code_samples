#!/usr/bin/main.py

#===============================================================================
# Author: Matthew Joonseo Park
# Date: Sept 23, 2021
# Description: Department tool Collections main GUI module
#===============================================================================


import maya.cmds as cmds

from rigkit.rigPipeline.qt import common_window
from widgets import common_widget, project_widget

from ..gui import QtCore

reload(common_widget)
reload(project_widget)


class DeptToolsWin( common_window.CommonWindow ):
    '''
    Blend shape checker main window
    '''
    OBJECT_NAME = 'DeptToolsWIN'
    WINDOW_NAME = 'Rigging Tool Collections'
    
    WIDTH = 340
    
    
    def __init__(self, parent=None):
        '''
        
        @param parent:
        '''
        super(DeptToolsWin, self).__init__(parent)
        self.setObjectName(self.OBJECT_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.help_url = "https://wildbrain-studios.atlassian.net/wiki/spaces/viewspacesummary.action?key=3DRIG"
        
        self.tab_widget = self.add_tabWidget(80, 8, (255, 210, 0), "w", "v", 1)
        self.main_layout = self.add_vLayout()
        self.main_layout.setContentsMargins(4, 2, 4, 2)
        self.main_layout.setSpacing(1)
        
        self._set_layout()
        self._set_prefs()
        self._set_action()
        
        
    def _set_layout(self):
        self.setMinimumWidth(self.WIDTH)
        # tabs
        commonWidget_name = "Global"
        commonWidget = common_widget.CommonWidget(self)
        self.tab_widget.insertTab(0, commonWidget, commonWidget_name)
        
        projectWidget_name = project_widget.ProjectWidget.get_cur_proj( ).upper()
        projectWidget = project_widget.ProjectWidget(self)
        self.tab_widget.insertTab(1, projectWidget, projectWidget_name)
        
        # add widgets
        self.main_layout.addWidget(self.tab_widget)
        self.main_widget.setLayout(self.main_layout)
        
    
    def _set_prefs(self):
        pass
        
    def _set_action(self):        
        pass
    
    
    def select_node(self, widget, pre=None, cur=None):
        cur_items = widget.selectedItems()
        nodes_to_sel = []
        if cur_items:
            for item in cur_items:
                node = item.text()
                if not node in nodes_to_sel:
                    nodes_to_sel.append(node)
            cmds.select(nodes_to_sel, r=1)

        
    def closeEvent(self, event):
        super(self.__class__, self).closeEvent( event )
        
        
    def showEvent(self, event):
        super(self.__class__, self).showEvent( event )





def openUI(parent=None):
    """
    Open the UI.
    """
    if cmds.window(DeptToolsWin.OBJECT_NAME, exists=True):
        cmds.deleteUI(DeptToolsWin.OBJECT_NAME)
    ui = DeptToolsWin(parent)
    ui.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
