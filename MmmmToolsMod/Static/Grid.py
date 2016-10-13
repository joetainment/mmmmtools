## Allow importing of non root modules for built
## in Maya stuff only, such as pm and cmds
import pymel
import pymel.all as pm
import maya
import maya.cmds as cmds



def reset(setManip=False):
    pymel.all.grid(reset=True)
    if setManip==True:
        ## Reset grid is spacing of 5 with 5 divisions,
        ## ends up being just 1.0
        setManipToSpacing( 1.0 )
   
def reset_via_numbers( multiplier=1.0, spacing=1.0, wholeSize=4096, setManip=False):
    ##Reset, but remember, default grid size is wacky, based on 5.0
    pymel.all.grid(reset=True)
    ## now change it to be power of two friendly 1.0*multiplier
    ## also set divisions to one and size
    pymel.all.grid( 
        size = wholeSize * multiplier,
        spacing = spacing * multiplier,
        divisions = 1
    )
    if setManip==True:
        setManipToSpacing( spacing*multiplier )
   
    
def getWholeSize():
    """
    This function gets the size of the *entire* grid,
    not the spacing between grid lines.
    """
    return pymel.all.grid( query=True, size=True )

def setWholeSize( wholeSize):
    """
    This function sets the size of the *entire* grid,
    not the spacing between grid lines.
    """
    pymel.all.grid( size=wholeSize )
    
def getSpacing( log=False):
    sp = pymel.all.grid( query=True, spacing=True )
    if log:
        print( "Grid spacing value is: " + str(sp) )
    return sp
    
def getDivisions( log=False):
    sp = pymel.all.grid( query=True, divisions=True )
    if sp < 1:  ## Just in case maya ever gives us a number lower than the logically smallest
        sp = 1
    if log:
        print( "Grid spacing value is: " + str(sp) )
    return sp

def setSpacing( spacing, setManip=False, log=False):
    if log:
        print( "Grid spacing value is: " + str(sp) )        
    pymel.all.grid( spacing=spacing )
    if setManip:
        setManipToSpacing(spacing)
    
def setManipToSpacing( spacing ):
    pymel.all.manipMoveContext( 'Move', e=True, snapRelative=True, snapValue=spacing )

def grow( setManip=False, log=False):
    spacing = getSpacing( log=log)
    new_spacing = spacing * 2
    setSpacing( new_spacing, setManip=setManip )
    if log==True:
        pymel.all.warning(    "Grid spacing value is: " + str(  getSpacing() )    )        
        
def shrink( setManip=False, log=False):
    spacing = getSpacing( log=log)
    new_spacing = spacing * 0.5
    setSpacing( new_spacing, setManip=setManip, )
    if log==True:
        pymel.all.warning(    "Grid spacing value is: " + str(  getSpacing()  )    )
        
def putSelectedVertsOnGrid():
    snapVertsToGrid()  ## basically just an alias of the function name
        
def snapVertsToGrid():
    originalSelection = pymel.all.ls( selection=True, flatten=True )
    pymel.all.mel.eval('ConvertSelectionToVertices;')
    selVerts = pymel.all.ls( selection=True, flatten=True )
    #objectSelection = pymel.all.ls(selection=True, shapes=True )
    
    #selObjs = originalSelection[:]  ## copy the list
    #selVerts = pymel.all.polyListComponentConversion(
    #    fromFace=True, fromVertex=True, fromEdge=True,
    #    fromVertexFace=True,
    #    toVertex=True )
    #    
    #selVerts = 
        
        
        
    spacing = getSpacing()
    divisions = getDivisions()
    
    spacingOfDivisions = spacing / float(divisions)
    
    for item in selVerts:
        if isinstance( item, pymel.all.MeshVertex ):
            for v in item:
                pW = v.getPosition(space='world')
                p = pW.homogenize()  ## Turn it into simply coords
                #print( type(p.x)  )                
                def onGrid(n, s):
                    return (  spacingOfDivisions * float(   round( n/float(s) )  )   )
                p.x = onGrid( p.x, spacingOfDivisions )
                p.y = onGrid( p.y, spacingOfDivisions )
                p.z = onGrid( p.z, spacingOfDivisions )
                #print( p.x, p.y, p.z )                               
                v.setPosition( p.homogenize(), space='world' )
                #print p.x,p.y,p.z
                #print( help(p)  )
                #break
    pymel.all.select( originalSelection )
    


    
def getGridSnappableSpacing():
    snappableSpacing = pm.grid(query=True, spacing=True)/pm.grid(query=True, divisions=True)
    return snappableSpacing


def putSelectedObjsOnGrid():
    ss = getGridSnappableSpacing()
    putSelectedObjsOnSnappableSpacing(ss)

    
def putSelectedObjsOnSnappableSpacing(snappableSpacing):
    oSel = pm.ls(selection=True)
    objs = oSel[:]
    for obj in objs:
        putObjOnSnappableSpacing(obj, snappableSpacing  )
    pm.select(oSel)


def putObjsOnSnappableSpacing( objs, snappableSpacing ):
    oSel = pm.ls(selection=True)
    for obj in objs:
        putObjOnSnappableSpacing( obj, snappableSpacing )
    usedObj = obj
    

def putObjOnSnappableSpacing( obj, snappableSpacing ):
    oSel = pm.ls(selection=True)
    destinationObj = obj
    usedObj = obj
    
    
    pm.select( destinationObj )
    t = pm.xform(query=True, rotatePivot=True, worldSpace=True )
    vt = pm.core.datatypes.Vector( t[0], t[1], t[2] )
    vt = onSnappableSpacingVec(vt, snappableSpacing)
    
    
    pm.select( usedObj )
    pm.move( vt, worldSpace=True, absolute=True, worldSpaceDistance=True)
    
    ## We compensate by getting the *object being moved*'s
    ## pivot
    t2 = pm.xform(query=True, rotatePivot=True, worldSpace=True )
    vt2 = pm.core.datatypes.Vector( t2[0], t2[1], t2[2] )
    
    ## vExtra is the additional amount compensated
    vExtra = vt - vt2
    
    vDest = vt+vExtra
    
    vFinal = vDest
    
    pm.move( vFinal, worldSpace=True, absolute=True, worldSpaceDistance=True)
    
    pm.select(oSel)

def onSnappableSpacing(n, snappableSpacing):
    return (  snappableSpacing * float(   round( n/float(snappableSpacing) )  )   )

def onSnappableSpacingVec(v, snappableSpacing):
    ## Only points need to use homogen
    ## this is simply a vector...
    #vh = v.homogenize()
    x = onSnappableSpacing( v.x, snappableSpacing )
    y = onSnappableSpacing( v.y, snappableSpacing )
    z = onSnappableSpacing( v.z, snappableSpacing )    
    return pm.core.datatypes.Vector( x,y,z )


putSelectedObjsOnGrid()

