import maya.cmds as cmds
import pymel.all as pm
import traceback


controlCurve = pm.PyNode('control_curve')

## to make a numerical 'floating point'
## attribute, we use  at='double', keyable=True
controlCurve.addAttr( 'allCurl', at='double', keyable=True )

controlCurve.addAttr( 'pointerAllCurl', at='double', keyable=True )
controlCurve.addAttr( 'middleAllCurl', at='double', keyable=True )
controlCurve.addAttr( 'pinkyAllCurl', at='double', keyable=True )

controlCurve.addAttr( 'pointerACurl', at='double', keyable=True )
controlCurve.addAttr( 'pointerBCurl', at='double', keyable=True )
controlCurve.addAttr( 'pointerCCurl', at='double', keyable=True )


controlCurve.addAttr( 'middleACurl', at='double', keyable=True )
controlCurve.addAttr( 'middleBCurl', at='double', keyable=True )
controlCurve.addAttr( 'middleCCurl', at='double', keyable=True )

controlCurve.addAttr( 'pinkyACurl', at='double', keyable=True )
controlCurve.addAttr( 'pinkyBCurl', at='double', keyable=True )
controlCurve.addAttr( 'pinkyCCurl', at='double', keyable=True )
pointerA = pm.PyNode('pointer_a')
pointerB = pm.PyNode('pointer_b')
pointerC = pm.PyNode('pointer_c')

middleA = pm.PyNode('middle_a')
middleB = pm.PyNode('middle_b')
middleC = pm.PyNode('middle_c')

pinkyA = pm.PyNode('pinky_a')
pinkyB = pm.PyNode('pinky_b')
pinkyC = pm.PyNode('pinky_c')



pointerAll = [ pointerA, pointerB, pointerC ]
middleAll = [ middleA, middleB, middleC ]
pinkyAll = [ pinkyA, pinkyB, pinkyC ]
all = pointerAll + middleAll + pinkyAll

adds = { }

for jnt in all:
    addNodeY = pm.createNode( 'plusMinusAverage' )
    addNodeZ = pm.createNode( 'plusMinusAverage' )
    addNodeY.rename(  jnt.name()+'_addY' )
    addNodeZ.rename(  jnt.name()+'_addZ' )
    ## the operator >> means "connect" for pymel
    addNodeY.output1D >> jnt.rotateY
    addNodeZ.output1D >> jnt.rotateZ
    
    adds[ jnt.name()+'Y' ] = addNodeY
    adds[ jnt.name()+'Z' ] = addNodeZ

## We can't hard core the name because Maya might change that
## #controlCurve.pointerAllCurl >> pm.PyNode('pointer_a_addZ').input1D
## so we use our adds dictionary to get the right answer
## pointerAllCurl connections
target = adds[ 'pointer_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerAllCurl >> target.input1D[num]
target = adds[ 'pointer_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerAllCurl >> target.input1D[num]
target = adds[ 'pointer_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerAllCurl >> target.input1D[num]


## pointer A,B,C connections
target = adds[ 'pointer_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerACurl >> target.input1D[num]
target = adds[ 'pointer_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerBCurl >> target.input1D[num]
target = adds[ 'pointer_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pointerCCurl >> target.input1D[num]


## middleAllCurl connections
target = adds[ 'middle_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleAllCurl >> target.input1D[num]
target = adds[ 'middle_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleAllCurl >> target.input1D[num]
target = adds[ 'middle_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleAllCurl >> target.input1D[num]


## middle A,B,C connections
target = adds[ 'middle_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleACurl >> target.input1D[num]
target = adds[ 'middle_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleBCurl >> target.input1D[num]
target = adds[ 'middle_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.middleCCurl >> target.input1D[num]


## pinkyAllCurl connections
target = adds[ 'pinky_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyAllCurl >> target.input1D[num]
target = adds[ 'pinky_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyAllCurl >> target.input1D[num]
target = adds[ 'pinky_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyAllCurl >> target.input1D[num]


## pinky A,B,C connections
target = adds[ 'pinky_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyACurl >> target.input1D[num]
target = adds[ 'pinky_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyBCurl >> target.input1D[num]
target = adds[ 'pinky_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.pinkyCCurl >> target.input1D[num]




## allCurl connections
target = adds[ 'pointer_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'pointer_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'pointer_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'middle_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'middle_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'middle_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'pinky_a' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'pinky_b' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]
target = adds[ 'pinky_c' + 'Z' ]
num = target.input1D.getNumElements()
controlCurve.allCurl >> target.input1D[num]








"""  ## These are ignorable comments
pointerAllCurlTargetsZ = [pointerA, pointerB, pointerC]
attrToTargets = {
'pointerAllCurl'+'Z': [pointerA, pointerB, pointerC]
}
"""  ## These are ignorable comments
