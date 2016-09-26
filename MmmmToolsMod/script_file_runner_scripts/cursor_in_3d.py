
########## Experimental Work In Progress #########

import pymel.all as pm
import maya.cmds as cmds

## Get the selected objects
originalSelection = pm.ls(selection=True)
selection =  pm.ls(selection=True)

to = pm.PyNode('to')
fro = pm.PyNode('from')

print(    help(  type(to)  )    )
#m = to.worldSpaceMatrix

class MmmmTemporaryObjectContext(object):
    def __init__(self):
        self.useLocator=True
    
    def __enter__(self):
        self.tmpObject = pm.spaceLocator( )
        self.tmpObjectShape = self.tmpObject.getShape()
        return tmpObject
    def __exit__(self):
        if self.tmpObjectShape.name() == pm.PyNode( self.tmpObjectShape.name() ).name():
            pm.delete( tmpObjectShape )
        if self.tmpObject.name() == pm.PyNode( self.tmpObject.name() ).name():
            children = self.tmpObject.getChildren()
            if len( children ) == 0:
                pm.delete( tmpObjectShape )    
        
class MmmmCursor(object):
    def placeCursor(self):
        with MmmmTemporaryObjectContext() as tmp:
           self.cursorMatrixInWorldSpace = tmp.getMatrix( worldSpace=True )


