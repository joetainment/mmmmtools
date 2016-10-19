import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import math,sys,os
from pymel.all import *

class ModelerMirrorer(object):
    __instance = None

    @classmethod
    def clearInstance(cls):
      cls.__instance = None

    @classmethod
    def getExistingInstance(cls):
      return cls.__instance 

    @classmethod
    def getInstance(cls):
      if not cls.__instance is None:
          return cls.__instance
      else:
          cls.__instance = ModelerMirrorer( makeUi=False )
          return cls.__instance

    def __init__(self, makeUi = True, parentWidget=None):
        if makeUi==True:
            self.makeUi(parentWidget=parentWidget)
            
    def makeUi(self, parentWidget=None):
        self.ui = ModelerMirrorerUi( self, parentWidget=parentWidget )
        return self.ui
            
    def makeStartShape( self, meshType="cube", segments3d=[2,2,2], smooth=False ):
        if meshType == 'cube':
            startShapeList = pm.polyCube( sx=segments3d[0], sy=segments3d[1],sz=segments3d[2] )
            startShapeSelectionList = pm.ls(selection=True)
            self.deleteNegativeSide( selectionToFilter = startShapeSelectionList )
        
    def deleteNegativeSide( self, selectionToFilter = None ):
        if selectionToFilter == None:
            selectionToFilter = pm.ls(selection=True)
        ## Bail early if we have no selected things to operate on!
        if len(selectionToFilter) == 0:
            return

        pm.mel.eval( 'PolySelectConvert 3;')
        verts = pm.ls(selection=True, flatten=True)
        vertsToDelete= []
        for vert in verts:
            x,y,z = pm.pointPosition( vert )
            if x < -0.0000000001:
                print( "For vert at:"+str(x)   )
                vertsToDelete.append( vert )
        try:
            ## fv and tf mean fromVertex, toFace
            facesToDelete = pm.polyListComponentConversion( vertsToDelete, fv=True, tf=True)
            faceToDelete = pm.ls(facesToDelete, flatten=True)
            pm.delete( facesToDelete )
            pm.select( selectionToFilter )
        except:
            print("Minor exception. No faces are on negative side to delete.")
        
        #print( facesToDelete )
        #for face in facesToDelete:
        #    pm.delete( face )
                
        
        
    def mirrorSelection(self):
        #try:
            nobjs = pm.instance()
            gr = pm.group(em=True, n = "Mirrored")
            for nobj in nobjs:
                pm.parent( nobj, gr )  ### **** Fix this later to use pymel
            pm.scale( gr, -1,1,1 )
        #except:
            #print( "Unable to instance and mirror selection.  Please make sure that only objects,and not components, are selected.")
    def flattenToXZero(self):
        pm.scale( [0,1,1], pivot=[0,0,0], scaleYZ = False )
    def mirrorGeometry( self ):
        pm.polyMirrorFace(
            ws=1, direction=1, mergeMode=1, ch=1,
            mergeThreshold=0.000001, pivot=[0,0,0]
        )


class ModelerMirrorerUi(object):
    def __init__(self, parentRef=None, parentWidget=None):
        self.parentRef = parentRef
        self.buttons = []
        self.layoutsR = []
        
        if parentWidget==None:
            parentWidget = self.widgets['parentWidget'] = pm.window(
                sizeable = True, title = "Mirrorer", titleBar=True,
                resizeToFitChildren=True,
            )
        else:
            self.widgets['parentWidget'] = parentWidget        
        
        with parentWidget:
            self.layoutC = pm.columnLayout( )
            with self.layoutC:
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    self.makeStartShapeUi = pm.button ( label = 'Make Starting Shape',
                                command = lambda xc: self.parentRef.makeStartShape(),width = 200 )
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    self.deleteNegativeSideUi = pm.button ( label = 'Delete Negative Side',
                                command = lambda xc: self.parentRef.deleteNegativeSide(),width = 200 )
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    self.mirrorSelectionUi = pm.button ( label = 'Mirror As Instance',
                                command = lambda xc: self.parentRef.mirrorSelection(),width = 200 )
                    
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:    
                    self.mirrorSelectionUi = pm.button ( label = 'Flatten to zero on X axis',
                                command = lambda xc: self.parentRef.flattenToXZero(),width = 200 )
        
        
                row = pm.rowLayout( numberOfColumns=3 )
                self.layoutsR.append( row )
                with row:
                    self.mirrorSelectionUi = pm.button ( label = 'Mirror Geometry (Baked/Frozen)',
                                command = lambda xc: self.parentRef.mirrorGeometry( ),width = 200 )
        
            
        # Show Window
        if type( parentWidget ) == pm.core.windows.window:
            win = parentWidget
            pm.showWindow(win)
            win.setWidth(300)
            win.setHeight(200)        
        
    
pass