import pymel.all as pm
import pymel
import maya.cmds as cmds
import traceback

def isShape(shape):
    parent=shape.getParent( )
    result=False
    try:
        if   cmds.nodeType( shape.name() )!= "transform"   and   cmds.nodeType( shape.name() )!= "joint":
            parent=shape.getParent( )
            if parent!=None:
                result=True
    except:
        print( traceback.format_exc() )
    return result
