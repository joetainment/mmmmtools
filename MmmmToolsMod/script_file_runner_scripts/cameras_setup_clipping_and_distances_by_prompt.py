import maya.OpenMaya as om
import pymel.all as pm
import maya.cmds as cmds


om.MGlobal.displayInfo(
    "Enter near clip and far clip, comma separated:"
)

try:
    userNumbers = input()
    ## Convert both numbers to float
    ## userNumbers should be a tuple we can
    ## index
    userNumbers = float(userNumbers[0]), float(userNumbers[1])
except:
    om.MGlobal.displayError(
      "Error, did not enter:  Near clip and far clip, comma separated."
    )

userNear = userNumbers[0]*1.0
userFar = userNumbers[1]*1.0
    

    
topCamXform = pm.PyNode('top')
sideCamXform = pm.PyNode('side')
frontCamXform = pm.PyNode('front')
perspCamXform = pm.PyNode('persp')

sideCam = pm.PyNode('sideShape')
topCam = pm.PyNode('topShape')
frontCam = pm.PyNode('frontShape')
perspCam = pm.PyNode('perspShape')


sideCam.nearClipPlane.set( userNear )
sideCam.farClipPlane.set( userFar )
sideCamXform.translateX.set( userFar / 2.0 )


topCam.nearClipPlane.set( userNear )
topCam.farClipPlane.set( userFar )
topCamXform.translateY.set( userFar / 2.0 )

frontCam.nearClipPlane.set( userNear )
frontCam.farClipPlane.set( userFar )
frontCamXform.translateZ.set( userFar / 2.0 )

perspCam.nearClipPlane.set( userNear )
perspCam.farClipPlane.set( userFar )

om.MGlobal.displayInfo(
    "Cams have been set."
)