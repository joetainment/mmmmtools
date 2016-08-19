#  get first leaf,  get all other leaves
#  remove shape nodes from other leaves
#       duplicate first leaf, and get its shape node
#       parent this new shape node to another leaf
#       w
#
#


from pymel.core import *


class UtilObjectReplacer(object):
       def __init__(self):
               objs = ls(selection=True)
               #objsO = objs.copy()
               objS = objs.pop( )


               for objT in objs:
                       select(objT)
                       shapeToDelete = pickWalk(direction = "down")
                       delete(shapeToDelete)

                       select(objS)
                       tmpObj = duplicate(objS)
                       select(tmpObj)
                       pickWalk( direction="down" )
                       tmpShape = ls(selection=True)
                       select( objT, add=True)
                       parent( tmpShape, objT, shape=True, relative=True)
                       delete( tmpObj )
