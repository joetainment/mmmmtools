import pymel.all as pm
import maya.cmds as cmds

@staticmethod
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