#!/bin/bash
import re

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

from mayaPipeline import MayaNode
    
import rig_utils as rutils


scriptUtil = OpenMaya.MScriptUtil()


class DeformerWeight(object):
    """
    """
    STRING_TYPE = "String"
    COMPONENT_TYPE = "Component"
    DAG_TYPE = "DagNode"
    COMP_TYPE = "Components"
    SELECTIONTYPE = None
    POS_X = "x"
    NEG_X = "-x"
    POS_Y = "y"
    NEG_Y = "-y"
    POS_Z = "z"
    NEG_Z = "-z"
    MIRROR_AXIS = POS_X
    MIRROR_X_POINT = OpenMaya.MPoint(-1.0, 1.0, 1.0)
    MIRROR_Y_POINT = OpenMaya.MPoint(1.0, -1.0, 1.0)
    MIRROR_Z_POINT = OpenMaya.MPoint(1.0, 1.0, -1.0)
    NUM_REGEX = re.compile("\[[0-9]*")
    
    def __init__(self, node, deformer):
        self.srcWObjList = []
        self.node = node
        self.nodeObj = OpenMaya.MObject()
        self.defNode = deformer
        self.weightList = []
        self.weightSet = None
        self.weightSetFn = OpenMaya.MFnSet()
        self.defWeightPairList = []
        self.defMembersName = None
        self.defMembersObj = OpenMaya.MObject()
        self.defMembersList = OpenMaya.MSelectionList()
        self.defMemberObjsList = []
        self.defMembersIndex = []
        self.collectInfo()
        
        #applying components in mirrored position status
        self.__useMirroredPos = True
        self.__mirrorAxis = self.POS_X
        

    @property
    def useMirroredPos(self):
        return self.__useMirroredPos
    
    @useMirroredPos.setter
    def useMirroredPos(self, status):
        self.__useMirroredPos = status
        
    @property
    def mirrorAxis(self):
        return self.__mirrorAxis
    
    @mirrorAxis.setter
    def mirrorAxis(self, axis):
        self.__mirrorAxis = axis
        
    @property
    def defObj(self):
        return rutils.getDependObj(self.defNode)
    
    @property
    def ndPath(self):
        return rutils.getDagpath(self.node)
    
    @property
    def compIters(self):
        return self.getSelections(self.node, returnType=DeformerWeight.COMPONENT_TYPE)
    
    @property
    def deformers(self):
        return DeformerWeight.getDeformers(self.node)
    
    @property
    def averageWeight(self):
        totalWeights = 0.0
        numWeights = len(self.defWeightPairList)
        for i, idx, w in self.defWeightPairList:
            totalWeights += w
        av_weight = totalWeights / numWeights
        return av_weight
    
    @property
    def outputGeometries(self):
        defGeoFilter = OpenMayaAnim.MFnGeometryFilter(self.defObj)
        outputGeoArray = OpenMaya.MObjectArray()
        defGeoFilter.getOutputGeometry(outputGeoArray)
        return outputGeoArray
    
    @property
    def transNode(self):
        fn = OpenMaya.MFnDagNode(self.ndPath)
        parentFn = OpenMaya.MFnDagNode(fn.parent(0))
        return parentFn.partialPathName()
    
        
    def collectInfo(self):
        self.getDeformerMembers()
        self.getDeformerWeights()
        
    def getOutputGeoIdx(self):
        outputGeoList = self.outputGeometries
        idx = 0
        for i in range(outputGeoList.length()):
            outputGeoFn = OpenMaya.MFnDagNode(outputGeoList[i])
            if outputGeoFn.fullPathName() == self.ndPath.fullPathName():
                idx = i
        return idx
        
    def getDeformerMembers(self):
        """
        """
        weightFilter = OpenMayaAnim.MFnGeometryFilter(self.defObj)
        self.weightSet = weightFilter.deformerSet()
        self.weightSetFn = OpenMaya.MFnSet(self.weightSet)
        self.weightSetFn.getMembers(self.defMembersList, True)
        memberNames = []
        self.defMembersList.getSelectionStrings(memberNames)
        self.defMembersName = cmds.ls(memberNames, fl=1)
        for member in self.defMembersName:
#             print member
            match = self.NUM_REGEX.search(member)
            if match:
                matched = match.group(0)
                matched = int(matched.replace(matched[0], ""))
                self.defMembersIndex.append(matched)
        
        iterMember = OpenMaya.MItSelectionList(self.defMembersList)
        while not iterMember.isDone():
            curPath = OpenMaya.MDagPath()
            curObj = OpenMaya.MObject()
            iterMember.getDagPath(curPath, curObj)
            self.defMemberObjsList.append(curObj)
            iterMember.next()

    def getDeformerWeights(self):   
        """
        """
        defFn = OpenMaya.MFnDependencyNode(self.defObj)
        weightListPlug = defFn.findPlug("weightList", True)
        childIdx = self.getOutputGeoIdx()
        try:
            ith_weightsPlug = weightListPlug.elementByPhysicalIndex(childIdx)
            plugWeights = ith_weightsPlug.child(0)
            numWeights = plugWeights.numElements()
            j=0
            for j in range(numWeights):
                weightPlug = plugWeights.elementByPhysicalIndex(j)
                idx = weightPlug.logicalIndex()
                value = weightPlug.asDouble()
    #                 print idx, " : " , value
                weight_pair = [idx, value]
                self.defWeightPairList.append(weight_pair)
            self.weightList.append([ith_weightsPlug, self.defWeightPairList])
        except Exception as e:
            print e 
                
    def setDeformerWeights(self, srcObj=None):   
        """
        """
        if not srcObj:
            print "No source object is defined. Aborted"
            return False
        defFn = OpenMaya.MFnDependencyNode(self.defObj)
        if not srcObj.defWeightPairList:
            print "No weighting is applied for the deformer: %s"%(defFn.name())
            return False
        weightListPlug = defFn.findPlug("weightList", True)
        # remove the weight attribute if it's existed
        childIdx = self.getOutputGeoIdx()
        ith_weightsPlug = weightListPlug.elementByLogicalIndex(childIdx)
        srcWListNum = len(srcObj.weightList)
        isSameObjs = self.ndPath == srcObj.ndPath
        i = 0
        for idx in range(srcWListNum):
            #retrieve source weight info
            src_ithPlug = srcObj.weightList[idx][0]
            src_weightInfo = srcObj.weightList[idx][1]
            src_weightIdxList = srcObj.weightList[idx][1][0]
            plugWeights = ith_weightsPlug.child(0)
            
            if not isSameObjs:
                # put every verts to weightlist due to no way to post deleting array element in maya damn!
                geoIter = OpenMaya.MItGeometry(self.ndPath, OpenMaya.MObject())
                while not geoIter.isDone():
                    g_idx = geoIter.index()
                    weightPlug = plugWeights.elementByLogicalIndex(g_idx)
                    # reset the plug
                    weightPlug.setDouble(1.0)
                    geoIter.next()
            
            # apply new weights
            if srcObj.SELECTIONTYPE == DeformerWeight.DAG_TYPE:
#                 print "Not Comp"
                for s_idx, value in src_weightInfo:
                    weightPlug = plugWeights.elementByLogicalIndex(s_idx)
                    # reset the plug
                    weightPlug.setMObject(OpenMaya.MObject())
                    # set the value
                    try:
                        weightPlug.setDouble(value)
                    except Exception as e:
                        print e
            else:
#                 print "Comp"
                for geoIter in self.compIters:
                    while not geoIter.isDone():
                        t_idx = geoIter.index()
                        weightPlug = plugWeights.elementByLogicalIndex(t_idx)
                        # reset the plug
                        weightPlug.setMObject(OpenMaya.MObject())
                        # set the value
                        try:
                            for s_geoIter in srcObj.compIters:
                                while not s_geoIter.isDone():
                                    c_idx = s_geoIter.index()
                                    for s_idx, value in src_weightInfo: 
                                        if s_idx != c_idx:
                                            continue
#                                         print s_idx, c_idx, t_idx, value, '#'
                                        weightPlug.setDouble(value)
                                    s_geoIter.next()
                        except Exception as e:
                            print e
                        geoIter.next()
        return True
    
    def copyWeights(self, option=1):
        """
        copy weights from src objs 
        @param option: 0 = copy using component idx, 1= copy weight by component world position
        """
        status = False
        if option == 0:
            status = self.copyMemberListInIdx()
            if not status:
                print "Copying memberList using component has been Failed. Aborted"
                return status
            status = self.copyWeightsInIdx()
        elif option == 1:
            status = self.copyMemberListInPos()
            if not status:
                print "Copying memberList using component position has been Failed. Aborted"
                return status
#             status = self.copyWeightsInPos()      
        return status
    
    def copyWeightsInPos(self):
        """
        
        """
        status = False
        for srcObj in self.srcWObjList:
            status = self.setDeformerWeights(srcObj)
        return status
    
    def copyMemberListInPos(self):
        """
        
        """
        shapeName = self.ndPath.partialPathName()
        for srcObj in self.srcWObjList:
            srcDefMembersIdx = srcObj.defMembersIndex
            for targetIter in self.compIters:
                delMemberList = []
                targetIter.reset()
                while not targetIter.isDone():
                    curIdx = targetIter.index()
                    if not curIdx in srcDefMembersIdx and curIdx in self.defMembersIndex:
                        curItem = targetIter.currentItem()
                        print curIdx
                        delMemberList.append(curItem)
                    targetIter.next()
                # remove none members from the curremt member set
                for targetVert in delMemberList:
                    if self.weightSetFn.isMember(self.ndPath, targetVert):
                        self.weightSetFn.removeMember(self.ndPath, targetVert)
                        
            pointArray = OpenMaya.MPointArray()
            vertIdSet = set()
            for srcIter in srcObj.compIters:
                srcIter.reset()
                while not srcIter.isDone():
                    curPoint = srcIter.position(OpenMaya.MSpace.kWorld)
                    curIdx = srcIter.index()
#                     print curIdx, srcDefMembersIdx, '#'
                    if curIdx in srcDefMembersIdx:
                        if self.useMirroredPos:
                            if curPoint.x > 0.0:
                                if self.mirrorAxis == self.POS_X or self.mirrorAxis == self.NEG_X:
                                    curPoint = OpenMaya.MPoint(-curPoint.x, curPoint.y, curPoint.z)
                                elif self.mirrorAxis == self.POS_Y or self.mirrorAxis == self.NEG_Y:
                                    curPoint = OpenMaya.MPoint(curPoint.x, -curPoint.y, curPoint.z)
                                else:
                                    curPoint = OpenMaya.MPoint(curPoint.x, curPoint.y, -curPoint.z)
                        pointArray.append(curPoint)
                    else:
                        delMemberList.append(object)
                    srcIter.next()
            arrayNum = pointArray.length()
            if arrayNum != 0:
                for i in range(arrayNum):
                     vertId, closestPos = self.getClosestPnt(pointArray[i])
                     vertIdSet |= vertId

            newMemberList = OpenMaya.MSelectionList()
            newMembers = []
            for vert in vertIdSet:
                vertName = self.transNode + ".vtx[%d]"%vert
                newMemberList.add(vertName)
                newMembers.append(vertName)
            if newMemberList.length() > 0:
                self.weightSetFn.addMembers(newMemberList)
            cmds.select(newMembers, r=1)

    
    def getClosestPnt(self, srcPnt):
        """
    
        """
        geoFn = OpenMaya.MFnMesh(self.ndPath)
        closestPnt = OpenMaya.MPoint()
        space = OpenMaya.MSpace.kWorld
    
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        idPtr = util.asIntPtr()
        geoFn.getClosestPoint(srcPnt, closestPnt, space, idPtr, OpenMaya.MFnMesh.autoUniformGridParams())
        idx = OpenMaya.MScriptUtil(idPtr).asInt()
        vertIdArray = OpenMaya.MIntArray()
        geoFn.getPolygonVertices(idx, vertIdArray)
        srcVec = OpenMaya.MVector(srcPnt)
        firstVertPoint = OpenMaya.MPoint()
        geoFn.getPoint(vertIdArray[0], firstVertPoint, OpenMaya.MSpace.kWorld)
        firstVertVec = OpenMaya.MVector(firstVertPoint)
        distance = (srcVec - firstVertVec).length()
        closestVertId = vertIdArray[0]
        vertIdx = 1
        for vertIdx in range(vertIdArray.length()-1):
            vertPoint = OpenMaya.MPoint()
            geoFn.getPoint(vertIdx, vertPoint, OpenMaya.MSpace.kWorld)
            vertVec = OpenMaya.MVector(vertPoint)
            distVec = (srcVec - vertVec).length()
            if distVec < distance:
                distance = distVec
                closestVertId = vertIdx
            
        return set([closestVertId]), closestPnt
    
    
    def getClosestPnt1(self, srcPnt):
        """
        
        @param srcPnt:
        """
        if self.nodeObj.hasFn(OpenMaya.MFn.kMesh):
            geoIntersector = OpenMaya.MMeshIntersector
            matrix = self.ndPath.inclusiveMatrix()
            geoIntersector.create(self.nodeObj, matrix)
            point = OpenMaya.MPoint()
            pointInfo = OpenMaya.MPointOnMesh()
            geoIntersector.getClosestPoint(point, pointInfo)
            
            
    
    def copyWeightsInIdx(self):
        """
        
        """
        status = False
        for srcObj in self.srcWObjList:
            status = self.setDeformerWeights(srcObj)
        return status
    
    def copyMemberListInIdx(self):
        """
        
        """
        for srcObj in self.srcWObjList:
            srcDefMembersIdx = srcObj.defMembersIndex
            for targetIter in self.compIters:
                targetIter.reset()
                newMemberList = OpenMaya.MSelectionList()
                delMemberList = []
                while not targetIter.isDone():
                    idx = targetIter.index()
                    curItem = targetIter.currentItem()
                    if not idx in srcDefMembersIdx and curItem in self.defMemberObjsList:
                        delMemberList.append(curItem)
                    if idx in srcDefMembersIdx and not curItem in self.defMemberObjsList:
                        newMemberList.add(self.ndPath, curItem)
                    targetIter.next()
                # remove none members from the curremt member set
                for vert in delMemberList:
                    if self.weightSetFn.isMember(self.ndPath, vert):
                        self.weightSetFn.removeMember(self.ndPath, vert)
                # add new memebers
                if newMemberList.isEmpty(): 
                    return True
                self.weightSetFn.addMembers(newMemberList)
        return True
    
    @classmethod
    def getSelections(cls, selNd=None, dagOnly=False, returnType="String"):
        """
        return selections
        ordered selections is True
        
        @param selNd(str): Optional user defined node
        @param dagOnly(str): return only dagNode(shape node)
        @param returnType(enum): String to return name of selections, Component to return as components of the node
        """
        selList = OpenMaya.MSelectionList()
        if not selNd:
            OpenMaya.MGlobal.getActiveSelectionList(selList, True)
        else:
            selList.add(selNd)
        selNum = selList.length()
        if selNum == 0:
            print "Nothing selected"
            return
        selIter = OpenMaya.MItSelectionList(selList)
        nameArray = []
        selIter.getStrings(nameArray)
        finalSelList = []
        nodeObj = OpenMaya.MObject()
        while not selIter.isDone():
            selIter.reset()
            selIter.getDependNode(nodeObj)
            if nodeObj.hasFn(OpenMaya.MFn.kDagNode):
                if not nodeObj.hasFn(OpenMaya.MFn.kGeometric) and not nodeObj.hasFn(OpenMaya.MFn.kTransform):
                    print ("Invalid Type : Dag node but nothing able to be weighted. %s"%nodeObj.apiTypeStr())
                else:
                    ndFn = OpenMaya.MFnDagNode(nodeObj)
                    ndPath = OpenMaya.MDagPath()
                    components = OpenMaya.MObject()
                    selIter.getDagPath(ndPath, components)
                    if components.isNull():
                        if nodeObj.hasFn(OpenMaya.MFn.kTransform):
                            num = scriptUtil.asUintPtr()
                            ndPath.numberOfShapesDirectlyBelow(num)
                            numShapes = scriptUtil.getUint(num)
                            if not numShapes:
                                print("Invalid Type : No Shape node found.")
                                return
                            ndPath.extendToShape()
                        if dagOnly:
                            if not ndPath in finalSelList:
                                finalSelList.append(ndPath)
                                selIter.next()
                        nodeObj = ndPath.node()
                        ndFn = OpenMaya.MFnDagNode(nodeObj)
                        ndPath, components = rutils.getDagPath(ndFn.fullPathName())
                    
                    compIter = OpenMaya.MItGeometry(ndPath, components)
                    if components.apiTypeStr() == "kInvalid":
                        cls.SELECTIONTYPE = DeformerWeight.DAG_TYPE
                        ndSel = OpenMaya.MSelectionList()
                        ndSel.add(ndPath.fullPathName())
                        shapeNameArray = []
                        ndSel.getSelectionStrings(shapeNameArray)
                        if returnType == DeformerWeight.COMPONENT_TYPE:
                            finalSelList.append(compIter)
                        else:
                            finalSelList.extend(shapeNameArray)
                    else:
                        cls.SELECTIONTYPE = DeformerWeight.COMP_TYPE
                        if returnType == DeformerWeight.COMPONENT_TYPE:
                            finalSelList.append(compIter)
                        else:
                            finalSelList.extend(nameArray)
            else:
                print("Invalid Type : Must be dag node")
                return
            selIter.next()
#         print finalSelList
        return finalSelList
                
    @staticmethod
    def getDeformers(node):
        """
        @param node: node to evaluate with
        """
        return [deformer for deformer in DeformerWeight._getDeformers(node)]
    
    @staticmethod
    def _getDeformers(node, returnType="String"):
        """        
        @param node: node to evaluate with
        @param returnType: String to return as name of deformers where as object to return as MObject
        """
        ndObj = rutils.getDependObj(node)
        nTypes = [OpenMaya.MFn.kFFD, OpenMaya.MFn.kClusterFilter, OpenMaya.MFn.kJointCluster, OpenMaya.MFn.kBlendShape,
                 OpenMaya.MFn.kWire, OpenMaya.MFn.kDeltaMush, OpenMaya.MFn.kWrapFilter, OpenMaya.MFn.kShrinkWrapFilter]
        direction = OpenMaya.MItDependencyGraph.kUpstream
        traversal = OpenMaya.MItDependencyGraph.kDepthFirst
        iterator = OpenMaya.MItDependencyGraph(ndObj, OpenMaya.MFn.kInvalid, direction, traversal)
        weighted_types = [OpenMaya.MFn.kSurface]
        weighted_direction = OpenMaya.MItDependencyGraph.kDownstream
        for nType in nTypes:
            iterator.resetTo(ndObj, nType, direction, traversal)
            while not iterator.isDone():
                obj = iterator.currentItem()
                weightedGeos = [geoObj for geoObj in iterConnections(ndObj, weighted_types, weighted_direction)]
                # skip the deformer node not associated with the current ndObj(surface)
                if not ndObj in weightedGeos:
                    iterator.next()
                if returnType == "String":
                    objFn = OpenMaya.MFnDependencyNode(obj)
                    yield objFn.name()
                else:
                    yield obj
                iterator.next()
        

def iterConnections(ndObj=None, types=[], direction=OpenMaya.MItDependencyGraph.kDownstream, 
                    traversal = OpenMaya.MItDependencyGraph.kDepthFirst,returnType=DeformerWeight.COMPONENT_TYPE):
    """
    @param ndObj:(MObject) object to evaluate with
    @param types:(MFn)
    @param direction: direction of connections
    @param traversal: kBreadthFirst or kDepthFirst
    @param returnType:(str) "String" to return as string type, Others will return as MObject
    """
    """
    """
    iterator = OpenMaya.MItDependencyGraph(ndObj, OpenMaya.MFn.kInvalid, direction, traversal)
    for nType in types:
        iterator.resetTo(ndObj, nType, direction, traversal)
        while not iterator.isDone():
            obj = iterator.currentItem()
            if returnType == "String":
                objFn = OpenMaya.MFnDependencyNode(obj)
                yield objFn.name()
            else:
                yield obj
            iterator.next()
            
            
def barycentricInterp(vecA, vecB, vecC, vecP):
    '''
    Calculates barycentricInterpolation of a point in a triangle.

    :param vecA - OpenMaya.MVector of a vertex point.
    :param vecB - OpenMaya.MVector of a vertex point.
    :param vecC - OpenMaya.MVector of a vertex point.
    :param vecP - OpenMaya.MVector of a point to be interpolated.

    Returns list of 3 floats representing weight values per each point.
    '''
    v0 = vecB - vecA
    v1 = vecC - vecA
    v2 = vecP - vecA

    d00 = v0 * v0
    d01 = v0 * v1
    d11 = v1 * v1
    d20 = v2 * v0
    d21 = v2 * v1
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return [u, v, w]    