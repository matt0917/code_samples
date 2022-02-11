import os, sys
import re
import json

from maya import cmds, mel

from mayaNode import MayaNode
from nodes.constraint import Constraint

from rigPipeline.rigs.rig_18.baseRig import BaseRig

import rig_utils as rutils



class SpaceSwitcher():
    '''
    SpaceSwitcher class
    '''
    # Node marker attributes
    CONDITION_ATTR = 'spaceSwitchCondition'
    CONSTRAINT_ATTR = 'spaceSwitchConstraint'
    SWITCH_DATA_ATTR = 'spaceSwitchData'

    # JSON data keys
    DATA_RIG = 'rig'
    DATA_ATTR = 'attr'
    
    # contraint types
    PARCON = 'parentConstraint'
    ORICON = 'orientConstraint'
    PNTCON = 'pointConstraint'
    CONST = {
        PARCON : 'PARCON',
        ORICON : 'ORICON',
        PNTCON : 'PNTCON'
        }
    CONDITION = 'COND'
    
    def __init__(self, data):
        '''
        data.constraintType
        data.driverNodes
        data.passengerNode
        data.mainCtrl
        data.subCtrls
        data.sharedCtrl
        data.switchAttr
        data.switchEnums
        '''
        self.constraint = data.constraintType
        self.driverNodes = data.driverNodes
        self.passengerNode = data.passengerNode
        self.mainCtrl = data.mainCtrl[0]
        self.subCtrls = data.subCtrls
        self.sharedCtrl = data.sharedCtrl[0]
        self.switchAttr = data.switchAttr
        self.prefix = data.switchAttr.replace('Parent', '')
        self.rig_name = data.baseRigName
        self.enums = data.switchEnums
        
        self.prebuild()

    def create(self):
        '''
        create switcher
        '''
        # Normalize the other input and fill in the blanks
        spaces = [MayaNode(node) for node in self.driverNodes]
        passengers = [MayaNode(node) for node in self.passengerNode]
        space_names = self.enums
        default_space_name = space_names[0]
        prefix = self.prefix

        switch_attr = self.switchAttr
        switch_data = {}
        switch_data[prefix] = {}
        switch_data[prefix][self.DATA_ATTR] = switch_attr
        switch_data[prefix][self.DATA_RIG] = self.rig_name
        dataStr = json.dumps(switch_data)

        self.sharedCtrl.setAttr(switch_attr, space_names, attrType='enum', force=True, k=1)
        self.sharedCtrl.setAttr(self.SWITCH_DATA_ATTR, dataStr, attrType='string',
                            force=True)
        
        translate = 'none' if self.constraint!=self.ORICON else ['x','y','z']
        rotate    = 'none' if self.constraint!=self.PNTCON else ['x','y','z']

        blend_attrs = []
        for index, space_name in enumerate(space_names):
            def_val = 1.0 if space_name == default_space_name else 0.0
            blend_attr_name = self._create_blend_attr_name(switch_attr, space_name)
            blend_attrs.append(blend_attr_name)
            self.sharedCtrl.setAttr(blend_attr_name, def_val, force=True,
                                minValue=0, maxValue=1, defaultValue=def_val)
            self.sharedCtrl.hideAttr(blend_attr_name)
            cond = self._build_condition(prefix, switch_attr, index, blend_attr_name, 
                                         space_name, self.rig_name)
            
        # Create the constraints (one per driven node)
        for index, node in enumerate(passengers):
            name = '{}SpaceSwitch{}{}_{}'.format(self.rig_name, prefix, index,
                                    self.CONST[self.PARCON])
            con = self._build_parent_constraint(name, spaces, node,
                                                translate, rotate)
            # Connect the blend attrs to drive the target weights
            target_attrs = con.getTargetAttrs()
            for i, blend_attr in enumerate(blend_attrs):
                self.sharedCtrl.connectAttr(blend_attr, con, target_attrs[i])

        # If there is only one space, hide the switch attribute
        if len(spaces) <= 1:
            self.sharedCtrl.hideAttr(switch_attr)
        
        self.set_sub_ctrls()

    
    def set_sub_ctrls(self):
        if self.subCtrls:
            connectSharedCtrl(self.sharedCtrl, self.subCtrls)
    

    def _build_condition(self, prefix, attr, index, blend_attr_name, space_name, rig_name):
        '''

        '''
        cond = MayaNode.create('condition')
        cond.rename('{}{}{}_{}'.format(prefix, space_name, rig_name, self.CONDITION))
        self.sharedCtrl.connectAttr(attr, cond, 'firstTerm')
        cond.setAttr('secondTerm', index)
        cond.setAttr('colorIfTrue', [1,1,1])
        cond.setAttr('colorIfFalse', [0,0,0])
        cond.setAttr(self.CONDITION_ATTR, blend_attr_name,
                     attrType='string', force=True )
        cond.connectAttr('outColorR', self.sharedCtrl, blend_attr_name)
        
        return cond


    def _build_parent_constraint(self, name, spaces, driven, translate,
                                 rotate):
        '''

        '''
        if rotate == 'none':
            driven.unlockAttr('rotate')
        if translate == 'none':
            driven.unlockAttr('translate')
        con = Constraint(cmds.parentConstraint(spaces, driven,
                                               maintainOffset=True,
                                               skipRotate=rotate,
                                               skipTranslate=translate,
                                               )[0])
        con.rename(name)
        con.setInterpolationType(con.SHORTEST)
        con.setAttr(self.CONSTRAINT_ATTR, True, attrType='bool', force=True)
        return con


    def _create_blend_attr_name(self, attr, space_name):
        '''
        '''
        return '{}_{}'.format(attr, space_name)


    def prebuild(self):
        if not isExist(self.sharedCtrl):
            self.sharedCtrl = createSharedCtrl(self.mainCtrl, self.sharedCtrl)
        else:
            shared_name = '%s|%s'%(self.mainCtrl, self.sharedCtrl)
            if cmds.objExists(self.sharedCtrl):
                shared_name = self.sharedCtrl
            self.sharedCtrl = MayaNode(shared_name)


def connectSharedCtrl(shared, targets ):
    '''
    Given a shared node, an instance of it is parented under each of the
    target transforms provided. (These would normally be control curves)
    '''
    curParents = [ node for node in cmds.listRelatives( shared, allParents=True, fullPath=True ) or [] ]
    for target in targets:
        if target in curParents:
            continue
        inst = MayaNode(cmds.instance(shared)[0])
        newShape = inst.getShape()
        newShape.setParent(target, shape=True, relative=True )
        cmds.delete( inst )
            
            
def createSharedCtrl(parents, name ):
    # Make sure we have an iterable thing to play with
    if not isinstance( parents, ( list, tuple ) ):
        parents = [ parents ]
    # Generate the new shape node
    sharedTrans = MayaNode(cmds.spaceLocator()[0])
    sharedNode = sharedTrans.getShape()
    sharedNode.rename( name )
    sharedNode.setAttr('visibility', 0)
    sharedNode.lockAttr('visibility')
    cmds.parent(sharedNode, parents[0], s=1, r=1)
    cmds.delete(sharedTrans)
    
    subAttr = 'subControls'
    if not sharedNode.hasAttr(subAttr):
        sharedNode.setAttr(subAttr, "OFF:ON", attrType='enum', force=1, k=1)
        sharedNode.setAttr(subAttr, 0)

    BaseRig.lockAndHideAttrs(sharedNode, keepAttrs=[subAttr])
    
    return sharedNode


def get_shared_ctrl(ctrl=None):
    '''
    Get the connected shared_CTRL to the ctrl 
    and return
    Args: ctrl(str)
    '''
    shared = None
    if not ctrl:
        print 'No ctrl has been defined'
        return
    if hasattr(ctrl, "__iter__"):
        print 'only valid for single ctrl'
        return
    ctrl = MayaNode(ctrl)
    shapes = ctrl.getShapes()
    if not shapes:
        return shared
    for shape in shapes:
        if isSharedCtrl(shape):
            shared = shape.name
            
    return shared
        

def isSharedCtrl(node=None):
    if not node:
        node = cmds.ls(sl=1)[0]
    if not node:
        return
    shape = MayaNode(node)
    shared_exp = re.compile('Shared_CTRL')
    if shape.nodeType == 'locator' and shared_exp.search(shape.name):
        return True
    else:
        return False


def areExist(nodes=None):
    '''
    return (True, None) or (False, missed_items)
    '''
    return rutils.areExist(nodes)


def isExist(node=None):
    '''
    return True, False
    '''
    return rutils.isExist(node)