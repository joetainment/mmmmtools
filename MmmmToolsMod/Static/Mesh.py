import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya.OpenMaya as om
import traceback



def activateSplitPolygonTool( ):
    pm.mel.eval("SplitPolygonTool;")


def centerPivotOnSelectedComponents( ):
      ##Convert selection to verts
      sF= (cmds.ls (sl=1))
      print (sF)
      sV= (cmds.polyListComponentConversion( (cmds.ls (sl=1, flatten=1)), tv=True))
      print (sV)
      cmds.select (sV)
    
      ##make list of selected verts
      selectedItems = (cmds.ls (flatten=True, selection=True))
      lengthOfList = len(selectedItems)
      print ("***Number of items in list " + str(lengthOfList))
    
      ##average verts
      ##print (selectedItems)
      xTotal=0
      yTotal=0
      zTotal=0
      for i in xrange(len(selectedItems)):
      ##print ("iteration" + str((i)+1))
        print ("Selected Item in iteration " + str((i)+1) + ": " + str(selectedItems[i]))
        print (cmds.pointPosition (selectedItems[i]))
        xTotal = xTotal + (cmds.pointPosition (selectedItems[i])[0])
        yTotal = yTotal + (cmds.pointPosition (selectedItems[i])[1])
        zTotal = zTotal + (cmds.pointPosition (selectedItems[i])[2])
        i=i+1
    
      xNew = (xTotal)/(lengthOfList)
      yNew = (yTotal)/(lengthOfList)
      zNew = (zTotal)/(lengthOfList)
      print ("center of selected items " + str(xNew) + " " + str(yNew) + " " + str(zNew))
      ##move pivot of selected obj to average of selected verts
      parentObj= (cmds.ls (hilite=True))
      ##print (parentObj[0])
      scalePivotNew = (str(parentObj[0]) + ".scalePivot")
      rotatePivotNew = (str(parentObj[0]) + ".rotatePivot")
      ##print (scalePivotNew)
      ##print (rotatePivotNew)
      cmds.move ((xNew), (yNew), (zNew), scalePivotNew, rotatePivotNew)
      cmds.select (parentObj) ##revert to original selection's parent obj    
    


def convertSelectionToCreasedEdges():
    pm.mel.eval( "ConvertSelectionToEdges;" )
    objs = pm.ls(selection=True, flatten=True)
    objsToSelect = []
    for obj in objs:
        try:
            creaseValue = pm.polyCrease( obj, query=True, value=True )
            creaseValue = creaseValue[0]
        except:
            creaseValue = 0

        if creaseValue > 0.01:
            #print( "found a creased edge" )
            objsToSelect.append(obj)

    if len(objsToSelect) > 0:
        #print(objsToSelect)
        #print("selecting")    
        pm.select( objsToSelect, replace=True )
    else:
        pm.select( clear=True )

def convertSelectionToHardEdges():
    pm.mel.eval( "ConvertSelectionToEdges;" )
    cmps = pm.ls(selection=True, flatten=True )
    to_select = []
    for cmp in cmps:
        if cmp.isSmooth()==False:
            to_select.append( cmp )
    pm.select( to_select )

    
def creaseSelectedEdges():
    setCreaseValueOnSelection( 20.0 )


    
        
def pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace():

    original_selection = pm.ls(selection = True)
    objs = original_selection[:]

    for obj in objs:
        try:
            previous_parent = obj.getParent()
            pm.parent( obj, world=True )                
            pm.move ( obj.scalePivot , [0,0,0] )
            pm.move ( obj.rotatePivot , [0,0,0] )
            pm.makeIdentity (obj, apply = True, normal = 0, preserveNormals = True )
            pm.delete (ch = True )
            pm.parent( obj, previous_parent )                
        except:
            print( traceback.format_exc()     )

def setAttributeOnSelected( attrName, v ):
    objs = pm.ls(selection=True, flatten=True)
    for obj in objs:
        try:
            obj.setAttr( attrName, v )
        except:
            print("Could not affect " + obj )
    
    
def setCreaseValueOnSelection( v ):
    objs = pm.ls(selection=True) ## removed flatten=True because it makes it crazy slow
    for obj in objs:
        try:
            creaseValue = pm.polyCrease( obj, value = v )
        except:
            pass  ## we don't care if this fails, no big deal
            

def uncreaseSelectedEdges():
    setCreaseValueOnSelection( 0.0 )

    
    