"""
Viewer - Module containing functionality relating to 
    viewing objects, viewport controls, camerea, etc
"""

import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya
import maya.OpenMaya as om

import traceback, math, random


#try
#    reload(SelectorVolumeSelect)
#except
#    try
#        import SelectorVolumeSelect
#    except
#        print( traceback.format_exc() )



class Viewer(object):
    def __init__(self, parentRef):
        self.parent = parentRef
        self.mmmm = self.parent
        self.mmmm.commander.addCommand( 'Viewer/Hello', self.hello )
    def hello(self):
        om.MGlobal.displayInfo( "Hello From Viewer!")
        