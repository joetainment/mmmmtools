import math, sys, os, traceback

import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm
import maya.OpenMaya as OpenMaya



class ModelerMrClean(object):
    def __init__(self):
        pass

    def getFaceCenter(self, precision):

        faceCenter = []

        selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selection)
        iter = OpenMaya.MItSelectionList (selection, OpenMaya.MFn.kMeshPolygonComponent)

        while not iter.isDone():
            #status = OpenMaya.MStatus
            dagPath = OpenMaya.MDagPath()
            component = OpenMaya.MObject()

            iter.getDagPath(dagPath, component)

            polyIter = OpenMaya.MItMeshPolygon(dagPath, component)

            while not polyIter.isDone():

                i = 0
                i = polyIter.index()
                #faceInfo = [0]
                #faceInfo[0] = ("The center point of face %s is:" %i)
                #faceCenter+=faceInfo

                center = OpenMaya.MPoint
                center = polyIter.center(OpenMaya.MSpace.kWorld)
                #print( "center is: " + str(center) )
                point = [0.0,0.0,0.0]
                
                point[0] = round( center.x, precision ) 
                point[1] = round( center.y, precision )
                point[2] = round( center.z, precision )
                faceCenter = point
                
                polyIter.next()
                
            iter.next()
            
        return str(faceCenter)
        
    def deleteFacesInSamePlace( self, faces_list, precision, tolerance ):
        faces = faces_list[:]
        face_center_dict = {}
        faces_to_delete = []
            
        for face in faces:
            pm.select( face )
            face_center = self.getFaceCenter( precision )
            if face_center in face_center_dict.keys():
                faces_to_delete.append( face )
                print( "marking face for deletion: " + str( face)   )
            else:
                face_center_dict[ face_center ] = face
        pm.delete( faces_to_delete )
        
    def mostlySafeCleanup(self, precision, tolerance):
        objs = pm.ls(selection=True)

        for obj in objs:
            pm.select( obj )
            ## Now the individual object is selected we Convert to faces
            pm.mel.eval("""ConvertSelectionToFaces;""")
            ## Now the faces are all selected
            ## Get the face selection
            faces = pm.ls( selection=True, flatten=True )
            self.deleteFacesInSamePlace( faces, precision, tolerance )
            pm.select( obj )
            pm.mel.eval("""ConvertSelectionToVertices;""")
            pm.polyMergeVertex(  alwaysMergeTwoVertices=False, distance = tolerance, worldSpace=True )
            pm.select( obj )
            pm.mel.eval("""ConvertSelectionToEdges;""") 
            pm.polySewEdge( worldSpace = True, texture = True, tolerance = tolerance )
            pm.select( obj )
            pm.mel.eval("""ConformPolygonNormals;""")  #pm.polyNormal( normalMode = 2 )
        ## Restore the original selection
        pm.select(  objs  )  


class ModelerMrCleanUi(object):  
    def __init__(self, makeUi = True ):
        self.mrClean = ModelerMrClean()
        if makeUi == True:
            self.makeUi()
            
    def makeUi( self ):
        self.win = pm.window(title="Mr Clean")
        self.win.show()
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.win.setWidth( 400 )
                self.win.setHeight( 200 )

                self.precisionText = pm.text(
                "Precision:\n Accuracy of face check, higher is more precise \n" + 
                "but will allow smaller errors.\n" +
                "It's like the opposite of merge distance tolerance." )                                
                self.precision = pm.intField(  )
                self.precision.setValue( 2 )
                
                self.toleranceText = pm.text( "Tolerance" )                                
                self.tolerance = pm.floatField(  )
                self.tolerance.setValue( 0.01 )
                
                
                self.button = pm.button( 
                    "Mostly Safe Cleanup",
                     command = lambda x:    self.mrClean.mostlySafeCleanup(    self.precision.getValue(), self.tolerance.getValue()    )
                )
                
                self.warningText = pm.text(
                    "Beware, backup your model first,\n" + 
                    "since this tool might delete more of\n" +
                    "your model than you want it to. This\n" +
                    "tool often helps with *very* broken\n" +
                    "models, but it can potentially make\n" +
                    "changes even where there aren't problems\n" +
                    " on a model."
                )
        


## Most safe cleanup
    ## select the object
    ## select via cleanup, normaifold geometry (normals and geometry)
    ## convert to contained faces
    ## delete the contained faces
    ## select the object
    
  
## Final, after mostly safe cleanup, causes Holes But Catches All Problems
    ## select the object
    ## merge verts
    ## merge edges
    ## select non manifold geo (normals and geo)
    ## delete this
    
    
## Find the above only, but don't delete at end





## select object, convert to vertices
## merge all verts

## select object, convert to edges
## merge all edges

## select object, convert to face
## conform normals on all faces

## check for lamina
##   resulting selection length should be zero  len(your_resulting_selection)==0

## check for non-manifold
##   resulting selection length should be zero  len(your_resulting_selection)==0

## check for edges of zero length
  ##resulting selection length should be zero  len(your_resulting_selection)==0
  
## check for edges of zero area
  ## resulting selection length should be zero  len(your_resulting_selection)==0
  
  
## select object, convert to vertices
## get the number of verts
## merge all verts
## confirm that number of verts is the same as we got

## select object, convert to edges
## get the number of edges
## merge all edges
## confirm that number of edges is the same as we got


