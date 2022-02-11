import os, sys
from functools import partial

from maya import cmds, mel

from base_gui import getMainWindow, loadUiType
from base_gui.baseWidget import BaseWindow
from base_gui.Qt import QtCore, QtGui, QtWidgets

from utilities.msg import MSG
from utilities.decorators import undoable
import space_switcher as space_switcher
reload(space_switcher)

# UI file paths
UI_ROOT = os.path.join( os.path.dirname( __file__ ), 'ui' )
MAIN_UI = os.path.join( UI_ROOT, 'space_switcher.ui' )


FORM, BASE = loadUiType(MAIN_UI)

class SpaceSwitcherWindow(BaseWindow):

    WINDOW_NAME = 'SpaceSwitcherWindow'

    def __init__(self, parent=None):
        if parent is None:
            parent = getMainWindow()
        super(SpaceSwitcherWindow, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(self.WINDOW_NAME)
        self.widget = getSpaceSwitcherWidget(self)
        self.setWidget(self.widget, 'Space Switcher')
        self.setMinimumSize(460, 680)


    def closeEvent(self, event):
        super(self.__class__, self).closeEvent(event)
        self.widget.closeEvent(event)


    def showEvent(self, event):
        super(self.__class__, self).showEvent(event)


class SpaceSwitcherWidget(FORM, BASE):
    '''
    parcon_radio
    oricon_radio
    pntcon_radio
    driver_list
    driver_btn
    passenger_list
    passenger_btn
    switcher_list
    switcher_btn
    sub_switcher_list
    sub_switcher_btn
    shared_name_list
    attr_name_line
    enum_name_textedit
    enum_name_btn
    create_btn
    '''
    
    ROOTS_VAR = ['Root', 'World', 'Base']
    PARCON = 'parentConstraint'
    ORICON = 'orientConstraint'
    PNTCON = 'pointConstraint'
    WIDGET_NAME = 'SpaceSwitcher_main_widget'
    SHAREDNAME_TEXT = 'No sharedCTRL found.Type a new Name.'
    NOSEL_MSG = '''
    Nothing is selected.
    Select node for {0}, and Try Again.
    Aborted.
    '''

    # optionVars
    opt_drivers = 'drivers'
    opt_passenger = 'passenger'
    opt_mainCtrl = 'mainCtrl'
    opt_subCtrls = 'subCtrl'
    opt_rigName = 'rigName'
    opt_sharedCtrl = 'sharedCtrl'
    opt_attr_base = 'attrBaseName'
    opt_attr_name = 'attrName'
    opt_enums = 'enums'
    
    def __init__(self, parent=None):
        if parent is None:
            parent = getMainWindow()
        super(SpaceSwitcherWidget, self).__init__(parent)
        self.setObjectName(self.WIDGET_NAME)
        self.setupUi(self)
        self.setWindowTitle('Space Switch Creator')
        
        if not cmds.optionVar(exists=self.opt_drivers):
            cmds.optionVar(sv=(self.opt_drivers, "[]"))
        if not cmds.optionVar(exists=self.opt_passenger):
            cmds.optionVar(sv=(self.opt_passenger, "[]"))
        if not cmds.optionVar(exists=self.opt_mainCtrl):
            cmds.optionVar(sv=(self.opt_mainCtrl, "[]"))
        if not cmds.optionVar(exists=self.opt_subCtrls):
            cmds.optionVar(sv=(self.opt_subCtrls, "[]"))
        if not cmds.optionVar(exists=self.opt_rigName):
            cmds.optionVar(sv=(self.opt_rigName, ""))
        if not cmds.optionVar(exists=self.opt_sharedCtrl):
            cmds.optionVar(sv=(self.opt_sharedCtrl, "[]"))
        if not cmds.optionVar(exists=self.opt_attr_base):
            cmds.optionVar(sv=(self.opt_attr_base, ""))
        if not cmds.optionVar(exists=self.opt_attr_name):
            cmds.optionVar(sv=(self.opt_attr_name, ""))
        if not cmds.optionVar(exists=self.opt_enums):
            cmds.optionVar(sv=(self.opt_enums, ""))
            
            
        self.set_prefs()
        self.set_action()
            
        
    def set_prefs(self):
        #optionVar 
        drivers = eval(self._getVar(self.opt_drivers))
        self.driver_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.driver_list.addItems(drivers)
        passenger = eval(self._getVar(self.opt_passenger))
        self.passenger_list.addItems(passenger)
        switcher = eval(self._getVar(self.opt_mainCtrl))
        self.switcher_list.addItems(switcher)
        sub_switcher = eval(self._getVar(self.opt_subCtrls))
        self.sub_switcher_list.addItems(sub_switcher)
        self.base_rig_line.setText(self._getVar(self.opt_rigName))
        shared_ctrl = eval(self._getVar(self.opt_sharedCtrl))
        self.shared_name_list.addItems(shared_ctrl)
        self.attr_name_line.setText(self._getVar(self.opt_attr_base))
        enums = self._getVar(self.opt_enums)
        self.enum_name_textedit.setText(enums)
        
        self.driver_list.itemSelectionChanged.connect(partial(self.select_node, self.driver_list))
        self.passenger_list.itemSelectionChanged.connect(partial(self.select_node, self.passenger_list))
        self.switcher_list.itemSelectionChanged.connect(partial(self.select_node, self.switcher_list))
        self.sub_switcher_list.itemSelectionChanged.connect(partial(self.select_node, self.sub_switcher_list))
        self.shared_name_list.itemSelectionChanged.connect(partial(self.select_node, self.shared_name_list))
    
    def set_action(self):
        driver_func = self.update_enums
        switcher_func = self.update_shared_ctrl
        
        self.driver_btn.clicked.connect(partial(self.load_baseList, self.driver_list, 'Driver', driver_func))
        self.passenger_btn.clicked.connect(partial(self.load_baseList, self.passenger_list, 'Passenger'))
        self.switcher_btn.clicked.connect(partial(self.load_baseList, self.switcher_list, 'CTRL to add switch attr', switcher_func))
        self.sub_switcher_btn.clicked.connect(partial(self.load_baseList, self.sub_switcher_list, 'SUBCTRL to add switch attr'))
        self.enum_name_btn.clicked.connect(partial(self.load_base, self.enum_name_textedit))
        self.attr_name_line.textChanged.connect(self.update_attr_name)
        self.create_btn.clicked.connect(self.create_switcher)
        self.update_attr_name()
        
    @property
    def selections(self):
        return cmds.ls(sl=1)
    
    @property
    def _const(self):
        if self.parcon_radio.isChecked():
            return self.PARCON
        elif self.oricon_radio.isChecked():
            return self.ORICON
        elif self.pntcon_radio.isChecked():
            return self.PNTCON


    def closeEvent(self, event):
        cmds.optionVar(sv=(self.opt_drivers, '%s'%self.get_baseList(self.driver_list)))
        cmds.optionVar(sv=(self.opt_passenger, '%s'%self.get_baseList(self.passenger_list)))
        cmds.optionVar(sv=(self.opt_rigName, self.get_textLine(self.base_rig_line)))
        cmds.optionVar(sv=(self.opt_attr_name, self.attr_name_label.text()))
        cmds.optionVar(sv=(self.opt_mainCtrl, '%s'%self.get_baseList(self.switcher_list)))
        cmds.optionVar(sv=(self.opt_subCtrls, '%s'%self.get_baseList(self.sub_switcher_list)))
        cmds.optionVar(sv=(self.opt_sharedCtrl, '%s'%self.get_baseList(self.shared_name_list)))
        cmds.optionVar(sv=(self.opt_attr_base, self.get_textLine(self.attr_name_line)))
        cmds.optionVar(sv=(self.opt_attr_name, self.attr_name_label.text()))
        cmds.optionVar(sv=(self.opt_enums, '%s'%self.get_textEdit(self.enum_name_textedit)))
        

    @undoable
    def load_base(self, widget, context=""):
        '''
        '''
        widget.clear()
        items = self.selections
        if not items:
            self.showMessage(self.NOSEL_MSG.format(context))
            return
        item = items[0]
        widget.setText(item)
        
        return item
        
    @undoable
    def load_baseList(self, widget, context="", widget_func=None):
        widget.clear()
        items = self.selections
        if not items:
            self.showMessage(self.NOSEL_MSG.format(context))
        widget.addItems(items)
        if widget_func:
            widget_func()
        
        return items
    
    
    def get_baseList(self, widget):
        '''
        return the list items in text
        '''
        items = []
        for index in xrange(widget.count()):
             item = widget.item(index).text()
             items.append(item)
             
        return items
        
        
    def update_enums(self):
        '''
        '''
        self.enum_name_textedit.clear()
        items = []
        for index in xrange(self.driver_list.count()):
             item = self.driver_list.item(index)
             items.append(item)
        if not items:
            return
        
        enum_name = ''
        for item in items:
            item_name = item.text()
            name = item_name.rsplit('_', 1)[0].title()
            first = name[0].upper()
            name = name.replace(name[0], first)
            name = 'World' if name in self.ROOTS_VAR else name
            if not enum_name:
                enum_name = name
                continue
            enum_name = '%s\n%s'%(enum_name, name)

        self.enum_name_textedit.setText(enum_name)
            
    
    def update_shared_ctrl(self):
        '''
        '''
        self.shared_name_list.clear()
        items = []
        for index in xrange(self.switcher_list.count()):
             item = self.switcher_list.item(index)
             items.append(item)
        if not items:
            return
        shared_ctrl = '%sShared_CTRL'%items[0].text().rsplit('_', 1)[0]
        # check if main switcher already has shared_ctrl
        main_switcher = self.get_baseList(self.switcher_list)
        if main_switcher:
            main_switcher = main_switcher[0]
            cur_shared_ctrl = space_switcher.get_shared_ctrl(main_switcher)
            if cur_shared_ctrl:
                shared_ctrl = cur_shared_ctrl
        self.shared_name_list.addItem(shared_ctrl)
        
        
    @undoable 
    def select_node(self, widget, prev=None, cur=None):
        '''
        '''
        cur_items = widget.selectedItems()
        nodes_to_sel = []
        if not cur_items:
            cmds.select(cl=1)
            return 
        for item in cur_items:
            node = item.text()
            if not node in nodes_to_sel and cmds.objExists(node):
                nodes_to_sel.append(node)
        cmds.select(nodes_to_sel, r=1)
        
        return nodes_to_sel
    
    
    def update_attr_name(self):
        '''
        '''
        baseAttrName = self.attr_name_line.text()
        if not baseAttrName:
            self.attr_fullname_label.setText('{baseName}Parent')
            return
        first = baseAttrName[0].lower()
        baseAttrName = baseAttrName.replace(baseAttrName[0], first)
        attrName = '%sParent'%(baseAttrName)
        self.attr_fullname_label.setText(attrName)


    def get_textEdit(self, text_widget, splitlines=False):
        '''
        get the each line of texts from textEdit
        '''
        lines = text_widget.toPlainText()
        if lines:
            lines.replace(" ", "")
            if splitlines:
                lines = lines.split('\n')

        return lines
    
    
    def get_textLine(self, text_widget):
        '''
        get the each line of texts from textEdit
        '''
        line = text_widget.text()
        if line:
            line.replace(" ", "")
            
        return line

    
    def _getVar(self, opt_var=None):
        '''
        '''
        return cmds.optionVar(q=opt_var)
    

    @undoable
    def create_switcher(self):
        msg = '''
        Missing Item for : "{}"
        '''
        msg1 = '''
        In GUI, but item not existed in the scene : "{}"
        '''
        data = SwitcherData()
        data.constraintType = self._const
        data.driverNodes = self.get_baseList(self.driver_list)
        data.passengerNode = self.get_baseList(self.passenger_list)
        data.baseRigName = self.get_textLine(self.base_rig_line)
        data.mainCtrl = self.get_baseList(self.switcher_list)
        data.subCtrls = self.get_baseList(self.sub_switcher_list)
        data.sharedCtrl = self.get_baseList(self.shared_name_list)
        data.switchAttr = self.attr_fullname_label.text()
        data.switchEnums = self.get_textEdit(self.enum_name_textedit, True)

        data.get_missed()

        if data.missed_items['missed']:
            for item in data.missed_items['missed']:
                sys.stdout.write(msg.format(item))
            return
        if data.missed_items['no_existed']:
            for item in data.missed_items['no_existed']:
                sys.stdout.write(msg1.format(item))
            return
        else:
            #===================================================================
            # for attr in data.__dict__:
            #     print attr, getattr(data, attr)
            #===================================================================
            print '++ Data is valid. Setting Switcher'
            s_switcher = space_switcher.SpaceSwitcher(data)
            s_switcher.create()


    def showMessage(self, msg, color='yellow', time=1200, fade=1):
        MSG.showMessage(msg=msg, col=color, time=time, fade=fade)

    
    

class SwitcherData(object):
    '''
    data class
    '''
    PARCON = SpaceSwitcherWidget.PARCON
    ORICON = SpaceSwitcherWidget.ORICON
    PNTCON = SpaceSwitcherWidget.PNTCON
    
    def __init__(self):
        self.constraintType = self.PARCON
        self.driverNodes = []
        self.passengerNode = []
        self.mainCtrl = None
        self.subCtrls = []
        self.sharedCtrl = None
        self.switchAttr = ""
        self.switchEnums = []
        
        self.missed_items = {
            'missed':[],
            'no_existed':[]
            }

    def validate(self, nodes):
        if not nodes:
            return
        result = space_switcher.areExist(nodes)
        existed = result[0]
        missed_items = result[1]
        if not existed:
            self.missed_items['no_existed'].append(missed_items)
        
    def get_missed(self):
        if not self.driverNodes:
            self.missed_items['missed'].append('Drivers')
        self.validate(self.driverNodes)
        
        if not self.passengerNode:
            self.missed_items['missed'].append('Passenger')
        self.validate(self.passengerNode)
        
        if not self.baseRigName:
            self.missed_items['missed'].append('BaseRigName')

        if not self.mainCtrl:
            self.missed_items['missed'].append('Main Switch CTRL')
        self.validate(self.mainCtrl)
            
        self.validate(self.subCtrls)
            
        if not self.sharedCtrl:
            self.missed_items['missed'].append('SharedCTRL')
            
        if not self.switchAttr:
            self.missed_items['missed'].append('Switch Attribute Name')
            
        if not self.switchEnums:
            self.missed_items['missed'].append('Attribute enum values')



def openUI(parent=None):
    if cmds.window(SpaceSwitcherWindow.WINDOW_NAME, exists=True):
        cmds.deleteUI(SpaceSwitcherWindow.WINDOW_NAME)
    ui = SpaceSwitcherWindow(parent)
    ui.show()
    return ui


def getSpaceSwitcherWidget(parent=None):
    if cmds.window(SpaceSwitcherWidget.WIDGET_NAME, exists=True):
        cmds.deleteUI(SpaceSwitcherWidget.WINDOW_NAME)
    ui = SpaceSwitcherWidget(parent)
    return ui