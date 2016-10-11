## This script deletes objects that 



## Chaos Eater Script  (Name by Roger Siuraneta)
import pymel.all as pm
import pymel
import traceback

## detect empty transform nodes
## and transform nodes with empty polygon shape nodes
## nodes with zero faces, and delete those objects
## via deleting their transform nodes


## Get a list of all objects that are selected
oSel = pm.ls(selection=True)
objs = oSel[:]

## Make an empty list
## of objects to delete later,
## we will add objects to this list
## when we find objects with zero polygons
objsToDelete = [ ]

## Loop through and detect, adding to list
for obj in objs:
    try:
        print( type(obj)  )
        if type(obj)==pymel.core.nodetypes.Transform:
            print( "found a transform" )
            ## Get the shape node of the mesh
            shapesToDelete = []
            shapes = obj.getShapes()
            for shape in shapes:
                ## get the number of faces on the shape
                facesCount = shape.numFaces()
        
                ## Find out if it is an intemediate shape
                isIntermediate = shape.intermediateObject.get()
        
                print( "isIntermediate: " + str(isIntermediate) )
        
                if facesCount == 0   or   isIntermediate==True:
                    shapesToDelete.append( shape )
            ## Now that extra shapes are deleted, check to see if any
            ## shapes are left, and if not, delete the entire object
            pm.delete( shapesToDelete )
            
            ## Get shapes again, partly too see if any are left at all
            ## if no shapes are left, delete the transform node
            shapes = obj.getShapes()
            if len(  obj.getChildren()  ) == 0:
                objsToDelete.append( obj )
    except:
        print( "error on obj: " + obj.name()  )
        print( traceback.format_exc()   )

print( shapesToDelete )
pm.delete( objsToDelete )


pm.select( oSel )
