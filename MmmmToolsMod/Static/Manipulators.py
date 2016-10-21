import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya.OpenMaya as om
import traceback



def cycleManipXformConstraint():

    contextNames = [
        ['Move', pm.manipMoveContext],
        ['Rotate', pm.manipRotateContext],
        ['Scale',pm.manipScaleContext],
    ]

    result = pm.manipMoveContext( 'Move', xformConstraint=True, query=True )


    if result=='none':
        for contextName, contextFunc in contextNames:
            contextFunc(contextName, xformConstraint='edge', edit=True)
        om.MGlobal.displayInfo( 'edge constraint mode active' )
    elif result=='edge':
        for contextName, contextFunc in contextNames:
            contextFunc(contextName, xformConstraint='surface', edit=True)
        om.MGlobal.displayInfo( 'surface constraint mode active' )
    else:
        for contextName, contextFunc in contextNames:
            contextFunc(contextName, xformConstraint='none', edit=True)
        om.MGlobal.displayInfo( 'no constraint mode active' )
