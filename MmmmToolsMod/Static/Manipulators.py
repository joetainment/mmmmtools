import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya.OpenMaya as om
import traceback


def cycleSelectByFaceCenters():
    l = om.MGlobal.displayInfo
    state = pm.polySelectConstraint( query=True, wholeSensitive=True )
    if state:
        pm.polySelectConstraint( wholeSensitive=False )
        l( 'Select By Face Centers - ON   (Maya bug may prevent this from showing until next selection change.)')
    else:
        pm.polySelectConstraint( wholeSensitive=True )
        l( 'Select By Face Centers - OFF  (Maya bug may prevent this from showing until next selection change.)' )


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
