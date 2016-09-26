#  get first leaf,  get all other leaves
#  remove shape nodes from other leaves
#       duplicate first leaf, and get its shape node
#       parent this new shape node to another leaf
#       w
#
#

from pymel.core import *

class UtilPivotFixer(object):
       def __init__(self):
               objs = ls(selection=True)
               for obj in objs:
                       tmpObj = duplicate( obj )
                       move ( obj, 0,0,0, rotatePivotRelative=True, scalePivotRelative=True  )
                       makeIdentity( obj, apply=True, translate=True, rotate=False, scale=False )
                       p = pointConstraint( tmpObj, obj )
                       o = orientConstraint( tmpObj, obj )
                       s = scaleConstraint( tmpObj, obj )
                       delete( p )
                       delete( o )
                       delete( s )
                       delete( tmpObj )