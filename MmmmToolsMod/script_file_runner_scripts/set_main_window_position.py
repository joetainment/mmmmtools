import pymel.all as pm
import pymel
import maya.cmds as pm

melGlobals = pymel.core.language.MelGlobals()
wname = melGlobals['gMainWindow']


##  {'width': 1904, 'top': 1039, 'left': 1159, 'height': 1034}
pm.window( wname, edit=True, leftEdge=1159)
pm.window( wname, edit=True, topEdge=1039 )
pm.window( wname, edit=True, width=1904 )
pm.window( wname, edit=True, height=1034 )
