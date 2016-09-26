import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import math,sys,os
from pymel.all import *

class ModelerAligner(object):
    def __init__(self, makeUi = True):
        if makeUi==True:
            self.ui = ModelerAlignerUi( self )
        else:
            print("This tool is only available with a UI.")
          
        
class ModelerAlignerUi(object):
    def __init__(self, parentRef=None):
        self.parentRef = parentRef
        self.buttons = []
        self.layoutsR = []
        self.window = pm.window( sizeable = False, title = "Vertex Aligner", titleBar=True, resizeToFitChildren=True)
        with self.window:
            self.layoutC = pm.columnLayout( )
            with self.layoutC:
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    btn_xMax = pm.button ( label = ' To X Maximum',
                                command = lambda xc: self.Align_Vertices("x","max"),width = 100 )
                    btn_xMid = pm.button ( label = ' To X Middle',
                                command = lambda xc: self.Align_Vertices("x","mid"),width = 100  )
                    btn_xMin = pm.button ( label = ' To X Minimum',
                                command = lambda xc: self.Align_Vertices("x","min"),width = 100  )                    
                    self.buttons.append( btn_xMax)
                    self.buttons.append( btn_xMid)
                    self.buttons.append( btn_xMin)
                    
                    
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:    
                    btn_yMax = pm.button ( label = ' To Y Maximum',
                                command = lambda xc: self.Align_Vertices("y","max"),width = 100  )
                    btn_yMid = pm.button ( label = ' To Y Middle',
                                command = lambda xc: self.Align_Vertices("y","mid"),width = 100  )
                    btn_yMin = pm.button ( label = ' To Y Minimum',
                                command = lambda xc: self.Align_Vertices("y","min"),width = 100  )       
                    self.buttons.append( btn_yMax)
                    self.buttons.append( btn_yMid)
                    self.buttons.append( btn_yMin)    
        
        
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    btn_zMax = pm.button ( label = ' To Z Maximum',
                                command = lambda xc: self.Align_Vertices("z","max"),width = 100 )
                    btn_zMid = pm.button ( label = ' To Z Middle',
                                command = lambda xc: self.Align_Vertices("z","mid"),width = 100  )
                    btn_zMin = pm.button ( label = ' To Z Minimum',
                                command = lambda xc: self.Align_Vertices("z","min"),width = 100  )                    
                    self.buttons.append( btn_zMax)
                    self.buttons.append( btn_zMid)
                    self.buttons.append( btn_zMin)
            
        
        # Show Window
        pm.showWindow(self.window)
        self.window.setWidth(300)
        self.window.setHeight(300)
    
    def Align_Vertices(self, axes, position):
        import math, sys, os
        import maya.cmds as cmds
        import maya.mel as mel
        self.axes = axes
        self.pos = position  
            
        #make list of selected verts
        selectedItems = (cmds.ls (flatten=True, selection=True))
        selectedItems = cmds.ls(selectedItems,flatten=True)
        originalSelection = selectedItems
        selectedItems = (cmds.polyListComponentConversion( selectedItems, tv=True) )
        selectedItems = cmds.ls(selectedItems,flatten=True)
        print(selectedItems)
        # Set all max/mins/mids to zero.
        # COULD CHANGE TO VECTORS LATER
        xMax, yMax, zMax = 0,0,0
        xMid, yMid, zMid = 0,0,0
        xMin, yMin, zMin = 0,0,0
        
        #Loop through the selected vertices to find the current positions, and the extreme positions
        for i, vert in enumerate(selectedItems):
          xTemp,yTemp,zTemp = cmds.pointPosition(vert)
        
          # If the first iteration, set the max/mins/mids to the first vertex values
          if (i==0):
            xMax = xMin = xMid = xTemp
            yMax = yMin = yMid = yTemp
            zMax = zMin = zMid = zTemp
        
          # Check the current vertice's value against the extremes.
          if (xTemp < xMin):
            xMin = xTemp
          if (yTemp < yMin):
            yMin = yTemp
          if (zTemp < zMin):
            zMin = zTemp
          if (xTemp > xMax):
            xMax = xTemp
          if (yTemp > yMax):
            yMax = yTemp
          if (zTemp > zMax):
            zMax = zTemp
        #Calculate the middle values for the group
        xMid = (xMax+xMin)/2
        yMid = (yMax+yMin)/2
        zMid = (zMax+zMin)/2
        """
        # Debug, print the extreme values
        #print ("Maximums")
        #print(xMax,yMax,zMax)
        #print ("Middles")
        #print(xMid,yMid,zMid)
        #print ("Minimums")
        #print(xMin,yMin,zMin)
        """
        pm.undoInfo( openChunk = True)
        # Now  Loop again and set vertices to new position
        for i, vert in enumerate(selectedItems):
          xTemp,yTemp,zTemp = cmds.pointPosition(vert)
          # Set the desired dimension of the vertex to the desired extreme    
          if (self.axes == "x"):
            if(self.pos == "max"):
              cmds.move(xMax,yTemp,zTemp,vert)
            elif(self.pos == "mid"):
              print(xMid)
              cmds.move(xMid,yTemp,zTemp,vert)
            elif(self.pos == "min"):
              cmds.move(xMin,yTemp,zTemp,vert)
          elif (self.axes == "y"):
            if(self.pos == "max"):
              cmds.move(xTemp,yMax,zTemp,vert)
            elif(self.pos == "mid"):
              cmds.move(xTemp,yMid,zTemp,vert)
            elif(self.pos == "min"):
              cmds.move(xTemp,yMin,zTemp,vert)
          elif (self.axes == "z"):
            if(self.pos == "max"):
              cmds.move(xTemp,yTemp,zMax,vert)
            elif(self.pos == "mid"):
              cmds.move(xTemp,yTemp,zMid,vert)
            elif(self.pos == "min"):
              cmds.move(xTemp,yTemp,zMin,vert)
        pm.undoInfo( closeChunk = True)
        cmds.select(originalSelection)