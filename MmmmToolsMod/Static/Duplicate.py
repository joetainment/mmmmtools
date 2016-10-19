import pymel.all as pm
import pymel
import maya.cmds as cmds
import traceback


def duplicateShape( shape, selectDup=False ):

        '''
        Duplicates the shape node, does not by default select the result.
        Takes as an argument a single pymel shape node.
        '''

        oSel = pm.ls(selection=True)
        
        ## we need a temporary xform to move the shape to
        originalParent = shape.getParent()
        tempXform = pm.createNode('transform')
        pm.parent( shape, tempXform, shape=True, relative=True )

        ## Duplicate the original shape
        ## we'll get a new duplicate of the transform
        ## and our duplicated shape node will be its shape
        ## it's guaranteed to be a simple one xform
        ## hierarchy because we started from the new xform we created
        dups = pm.duplicate( shape )
        tempDuplicatedXform = dups[0]
        dupShape = tempDuplicatedXform.getShape()
        
    
        ## Now put the original xform back where we got it from!
        ## also parent new duplicated shape back to original xform
        pm.parent( shape, originalParent, shape=True, relative=True )
        pm.parent( dupShape, originalParent, shape=True, relative=True )
        ## Clean up the temporary xforms that were used
        pm.delete( tempXform )
        pm.delete( tempDuplicatedXform )
        
        ## restore selection and return result
        if selectDup==False:
            pm.select( oSel )
        return dupShape


def dupXformNoChildren( obj ):
    ## takes only a single object
    assert type(obj) == pymel.core.nodetypes.Transform
    print( obj )
    
    dupShapesFinal = []
    tempDuplicatedXforms = []
    
    for s in obj.getShapes():
    
        s = obj.getShape()

        ## we need a temporary xform to move the shape to
        tempXform = pm.createNode('transform')
        pm.parent( s, tempXform, shape=True, relative=True )

        ## Duplicate the original shape
        ## we'll get a new duplicate of the transform
        ## and our duplicated shape node will be its shape
        dups = pm.duplicate( s )
        tempDuplicatedXform = dups[0]
        tempDuplicatedXforms.append( tempDuplicatedXform )
        
        dupShapesFinal.append( tempDuplicatedXform.getShape() )
    
        ## Now put the original xform back where we got it from!
        pm.parent( s, obj, shape=True, relative=True )
        pm.delete( tempXform )
        
        ## Now we should be back where we started, except with a new
        ## duplicated shape node at the origin, with a indentity
        ## xform node
        
    ## Now that we have duplicates of all the shapes,
    ## we need a duplicated xform node
    dupList = pm.duplicate( obj, parentOnly=True, returnRootsOnly=True )
    dupXform = dupList[0]
    ## Now parent all the duplicated shapes to the duplicated xform
    for s in dupShapesFinal:
        pm.parent( s, dupXform, shape=True, relative=True )
        
        
    ## We have to delete tempInplaceXform later, because we need it for a bit
    pm.delete( tempDuplicatedXforms )
    

