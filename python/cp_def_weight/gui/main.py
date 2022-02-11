# Standard Libraries
import os
import pkgutil
import sys
from functools import partial

# Third Party Libraries
from maya import OpenMaya
from maya import cmds
from maya import mel

# GUI Libraries
from base_gui import getMainWindow, loadUiType
from base_gui.baseWidget import BaseWindow
from base_gui.Qt import QtCore, QtWidgets

from .. import deformer_weight as dw
reload(dw)

# UI file paths
ROOT = os.path.dirname(os.path.dirname( __file__ ) )
UI_ROOT = os.path.join(ROOT, 'ui')
MAIN_UI = os.path.join( UI_ROOT, 'main.ui')

FORM, BASE = loadUiType(MAIN_UI)

#===============================================================================
# Main
#===============================================================================
class DeformerWeightWin(BaseWindow):
    '''
    '''
    WINDOW_NAME = 'DeformerWeightWIN'

    def __init__(self, parent=None):
        '''

        '''
        if parent is None:
            parent = getMainWindow()
        super(DeformerWeightWin, self).__init__(parent=parent, styleColor='blue')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(self.WINDOW_NAME)
        self.deformerWeightWidget = getDeformerWeightWidget(self)
        self.setWidget(self.deformerWeightWidget, self.deformerWeightWidget.WIDGET_NAME, self.WINDOW_NAME)
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.ui.titleLabel.setStyleSheet("font:75 10pt \"Courier New\"; color: #70c6e2;background:none;")
        self.setGeometry(0,0,250,500)
        self.ui.optionsButton.setFixedSize(24, 24)
        self.ui.optionsButton.setIconSize(QtCore.QSize(16, 16))
        self.ui.betaFrame.setIconSize(QtCore.QSize(16, 16))
        self.ui.devFrame.setIconSize(QtCore.QSize(16, 16))
        self.ui.gridLayout.setHorizontalSpacing(1)
        self.ui.gridLayout.setVerticalSpacing(0)
        self.ui.titleFrame.setFixedHeight(30)

        #Var
        self.events = []
        
        
    def closeEvent(self, event):
        if self.events:
            for each in self.events:
                OpenMaya.MMessage.removeCallback(each)
        super(self.__class__, self).closeEvent(event)


    def showEvent(self, event):
        if not cmds.help(q=1, pm=True):cmds.help(pm=True) # turn on tooltip over the buttons
        self._center()
        super(self.__class__, self).showEvent(event)


    def _center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/1.05, (screen.height()-size.height())/2)


    def _createSelChangeEvent(self):
        event = self.deformerWeightWidget.createSelEvent()
        self.events.append(event)
        


class DeformerWeightWidget(FORM, BASE):
    '''
    DeformerWeightWidget:
    main.ui items:
    self.loadSrc_btn
    self.loadTarget_btn
    self.src_list
    self.target_list
    self.srcDef_list
    self.targetDef_list
    self.copy_btn
    '''
    WIDGET_NAME = 'Deformer Weight V1.0'
    CAL_METHOD_LIST = ["index", "position"]
    
    def __init__(self, parent=None):
        '''
        main widget
        '''
        super(DeformerWeightWidget, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName(self.WIDGET_NAME)
        self.realtimeRatio_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        
        self.set_pref()
        self.set_func()
        
    @property
    def useMirror(self):
        state = self.mirror_chbox.checkState()
        if state == QtCore.Qt.Checked:
            return True
        elif state == QtCore.Qt.Unchecked:
            return False
        
    @property
    def mirrorAxis(self):
        selAxis = self.mirror_combo.currentText().lower()
        return selAxis
    
    @property
    def calculateMethod(self):
        """
        0: index 1:position
        """
        return self.calculate_combo.currentIndex()
    
    def showEvent(self, event):
        self.on_loadSrc_btn()
        self.on_selItem([self.src_list, self.srcDef_list])
        
    def set_pref(self):
        self.src_list.itemDoubleClicked.connect(partial(self.select_node, self.src_list))
        self.target_list.itemDoubleClicked.connect(partial(self.select_node, self.target_list))
        self.srcDef_list.itemDoubleClicked.connect(partial(self.select_node, self.srcDef_list))
        self.targetDef_list.itemDoubleClicked.connect(partial(self.select_node, self.targetDef_list))
        self.calculate_combo.addItems(self.CAL_METHOD_LIST)
    
    def set_func(self):
        self.loadSrc_btn.clicked.connect(self.on_loadSrc_btn)
        self.loadTarget_btn.clicked.connect(self.on_loadTarget_btn)
        self.src_list.itemSelectionChanged.connect(partial(self.on_selItem, [self.src_list, self.srcDef_list]))
        self.target_list.itemSelectionChanged.connect(partial(self.on_selItem, [self.target_list, self.targetDef_list]))
        self.copy_btn.clicked.connect(self.on_copy_btn)
    
    def on_copy_btn(self):
        if self.src_list.count() == 0 or self.srcDef_list.count() == 0:
            return
        srcList = self.src_list.selectedItems()
        srcDef = self.srcDef_list.selectedItems()
        if not srcList:
            print "No source node selected. Aborted"
            return
        if not srcDef:
            print "No source deformer selected. Aborted"
            return
        if self.target_list.count() == 0:
            return
        targetList = self.target_list.selectedItems()
        targetDefNum = self.targetDef_list.count()
        if not targetList:
            print "No target node selected. Aborted"
            return
        srcWObjList = []
        targetDef = None
        for node in srcList:
            srcDef = srcDef[0].text()
            node = node.text()
            srcWObj = dw.DeformerWeight(node, srcDef)
            srcWObj.useMirroredPos = self.useMirror
            srcWObj.mirrorAxis = self.mirrorAxis
#             print srcWObj.weightList
            srcWObjList.append(srcWObj)
            targetDef = srcWObj.defNode
        for node in targetList:
            node = node.text()
            if targetDefNum != 0:
                targetDef = self.targetDef_list.selectedItems()
                if not targetDef:
                    print "No target deformer selected to copy source deformer weights for. %s is applied"%srcDef
                    targetDef = srcDef
                else:
                    targetDef = targetDef[0].text()
            # copy weight
            targetWObj = dw.DeformerWeight(node, targetDef)
            targetWObj.useMirroredPos = self.useMirror
            targetWObj.mirrorAxis = self.mirrorAxis
            targetWObj.srcWObjList = srcWObjList
            targetWObj.copyWeights(option=self.calculateMethod)
            
    def on_selItem(self, widgets=None):
        node_list = widgets[0]
        nodeDef_list = widgets[1]
        nodeDef_list.clear()
        curItems = node_list.selectedItems()
        if not curItems:
            nodeDef_list.clear()
            return
        curDeformers = set()
        for curItem in curItems:
            curDeformers.update(set(dw.DeformerWeight.getDeformers(curItem.text())))
        nodeDef_list.addItems(list(curDeformers))
    
    def on_loadSrc_btn(self):
        self.src_list.clear()
        selList = dw.DeformerWeight.getSelections()
        if selList:
            self.src_list.addItems(selList)
            self.src_list.setCurrentRow(0)
            
    def on_loadTarget_btn(self):
        self.target_list.clear()
        selList = dw.DeformerWeight.getSelections()
        if selList:
            self.target_list.addItems(selList)
            self.target_list.setCurrentRow(0)
            
    def createSelEvent(self):
        event = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.onSelChanged)
        return event

    def onSelChanged(self, _n=None):
        widgets = [self.src_list, self.target_list, self.srcDef_list, self.targetDef_list]
        selList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selList)
        if selList.length() == 0:
            for widget in widgets:
                widget.clearSelection()
            return
        for widget in widgets:
            widget.clearSelection()
            for idx in range(selList.length()):
                obj = OpenMaya.MObject()
                selList.getDependNode(idx, obj)
                if not obj.hasFn(OpenMaya.MFn.kTransform):
                    continue
                objFn = OpenMaya.MFnDagNode(obj)
                name = objFn.partialPathName()
                item = widget.findItems(name, QtCore.Qt.MatchExactly)
                if not item:
                    continue
                widget.setCurrentRow(widget.row(item[0]))
                item[0].setSelected(True)

    def select_node(self, widget, _n=None):
        main_win = DeformerWeightWin.WINDOW_NAME
        cur_win = QtWidgets.QApplication.activeWindow().objectName()
        if cur_win != main_win:
            return 
        cur_items = widget.selectedItems()
        nodes_to_sel = []
        if cur_items:
            for item in cur_items:
                node = item.text()
                if not node in nodes_to_sel:
                    nodes_to_sel.append(node)
            cmds.select(nodes_to_sel, r=1)
        else:
            cmds.undoInfo(state=True)
            return




def openUI(parent=None):
    if cmds.window(DeformerWeightWin.WINDOW_NAME, exists=True):
        cmds.deleteUI(DeformerWeightWin.WINDOW_NAME)
    ui = DeformerWeightWin(parent)
    ui.show()
    return ui


def getDeformerWeightWidget(parent=None):
    if cmds.window(DeformerWeightWidget.WIDGET_NAME, exists=True):
        cmds.deleteUI(DeformerWeightWidget.WIDGET_NAME)
    ui = DeformerWeightWidget(parent)
    return ui