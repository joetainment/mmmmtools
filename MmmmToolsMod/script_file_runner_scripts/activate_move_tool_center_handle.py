"""
This script changes the active handle to the 3D space.  It's very useful for
use together with snapping, when the object, and it's manipulator start off screen
but you want to move them to the screen.

The default move context is 'Move'

Notes from the Maya documentation

    0 - U axis handle is active
    1 - V axis handle is active
    2 - N axis handle is active ( default )
    3 - Center handle (all 3 axes) is active

applicable only when the manip mode is 3.
alignAlong(aa)     [float, float, float]     createedit
    Aligns active handle along vector.
constrainAlongNormal(xn)     boolean     queryedit
    When true, transform constraints are applied along the vertex normal first and only use the closest point when no intersection is found along the normal.
currentActiveHandle(cah)     int     queryedit
    Sets the active handle for the manip. Values can be:

    0 - X axis handle is active
    1 - Y axis handle is active
    2 - Z axis handle is active
    3 - Center handle (all 3 axes) is active
    4 - XY plane handle is active
    5 - YZ plane handle is active
    6 - XZ plane handle is active
"""

import pymel.all as pm
import maya.cmds as cmds
mpName = 'Move'
pm.manipMoveContext( mpName, edit=True, currentActiveHandle=3 )