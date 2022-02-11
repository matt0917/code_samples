#!/usr/bin/main.py

#===============================================================================
# Author: Matthew Joonseo Park
# Date: Sept 29, 2021
# Description: project tools
#===============================================================================
import re
import os, sys
import pkgutil

from rigkit.rigPipeline.qt import getMainWindow
from rigkit.rigPipeline.qt import common_window

from ...gui import QtWidgets
from ...gui.widgets import ToolData
from ...dept_tools.proj_tools import *


class ProjectWidget( QtWidgets.QWidget ):
    '''
    Project Widget
    '''
    
    MOD_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "dept_tools/proj_tools" ))
    
    OBJECT_NAME = 'Project_Tool_Widget'
    WIN_TITLE = "Project Rigging Tools"
    
    DEFAULT_PROJ = "default"
        
    def __init__(self, parent=None):
        '''
        
        @param parent:
        '''
        if parent == None:
            parent = getMainWindow()
        super(ProjectWidget, self).__init__(parent)
        
        file_basename = "project_tool_list"
        self.data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data/projects", 
                                                  self.project, file_basename))
        
        self.setObjectName(self.OBJECT_NAME)
        self.setWindowTitle(self.WIN_TITLE)
        self.setContentsMargins(0, 0, 0, 0)
                
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 1, 0, 1)
        self.main_layout.setSpacing(1)
        
        self.spacer = QtWidgets.QSpacerItem(1, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        toolModules = [mod for _, mod, _ in pkgutil.iter_modules([self.MOD_PATH])]
        ToolData.SERIALIZE = True
        toolData = self._get_data()
        if not toolData:
            idx = self.data_path.rfind(self.project)
            self.data_path = self.data_path[:idx] + self.DEFAULT_PROJ + self.data_path[idx + len(self.project):]
            toolData = self._get_data()
        project_modules = toolData.keys()
        
        self.toolWidgets = []
        for mod in toolModules:
            # filtering modules we want for the project only
            if not mod in project_modules:
                continue
            ToolWidget.btn_text = toolData[mod]["text"]
            ToolWidget.help_url = toolData[mod]["url"]
            ToolWidget.tool_tip = toolData[mod]["toolTip"]
            modWidget = ToolWidget(eval(mod))
            self.toolWidgets.append(modWidget)
        self._set_layout()
        self._set_prefs()
        self._set_action()

        
    @property
    def project(self):
        '''
        current project
        '''
        return self.get_cur_proj()


    @classmethod
    def get_cur_proj(cls):
        project = None
        try:
            from rigkit.rigPipeline.interface import _getProject
            project = _getProject()
        except:
            print("Unable to determine current project. Set DEFAULT.")
        if not project:
            project = cls.DEFAULT_PROJ
        regex = re.compile("[0-9]+", re.I)
        matched = regex.search(project)
        if matched:
            project = project.replace(matched.group(), "")
        return project.upper()
        
    
    def _get_data(self):    
        return ToolData.load_data(self.data_path)
    
        
    def _set_layout(self):
        # add widgets
        for widget in self.toolWidgets:
            self.main_layout.addLayout(widget.main_layout)
        self.main_layout.addItem(self.spacer)
        self.setLayout(self.main_layout)
        
    
    def _set_prefs(self):
        pass
        
        
    def _set_action(self):        
        pass
    
    

#===============================================================================
# ToolWidget
#===============================================================================

class ToolWidget( common_window.CommonWindow ):
    '''
    ToolWidget
    '''
    ICON_PATH = os.path.join( os.path.dirname( __file__ ),'..', '..', 'gui/icons' )
    help_icon = "help_purple_32"
    
    help_url = "https://wildbrain-studios.atlassian.net/wiki/spaces/viewspacesummary.action?key=3DRIG"
    help_tip = "Wiki Page"
    
    tool_tip = ""
    btn_text = ""
    
    def __init__(self, toolModule, parent=None):
        '''
        constructor
        '''
        super(ToolWidget, self).__init__(parent)
        
        
        self.main_layout, self.tool_btn = \
        self.add_helpBtn_combo_hLayout(self.btn_text, self.help_url, self.tool_tip, self.help_icon, self.help_tip)
        
        self.toolModule = toolModule 
        
        self.set_action()
        
        
    def set_action(self):
        self.tool_btn.clicked.connect(self.on_tool_btn)
        
        
    def on_tool_btn(self):
        self.toolModule.openUI()


























































if __name__ == "__main__":
    ui = ProjectWidget(None)
    ui.exec_()
    sys.exit()
    
    
    
    
    
    
    
    
    
    






