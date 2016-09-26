import pymel.all as pm
import maya.cmds as cmds

##This script was written by Marina while taking the Maya Scripting class taught by Joe Crawford.  

class RiggerJointOrientHelper(object):  ## inherit from object by default
  def __init__(self):
    self.ui = RiggerJointOrientHelperUi(self)
  def rotateJoint( self, rotateX, rotateY, rotateZ, rotateRelative=False ):
    objs = cmds.ls( selection=True )
    try:
        pm.mel.eval( """
            setToolTo $gRotate;
            manipRotateValues Rotate;
            toolPropertyShow;
            changeToolIcon;
        """ )
    except:
        print( "switching to rotate tool (with error correction via exception handling)" )
    try:
        pm.mel.eval( """
            setToolTo $gRotate;
            manipRotateValues Rotate;
            toolPropertyShow;
            changeToolIcon;
        """ )
    except:
        print( "(...continuing error correction via exception handling)" )
    for i in objs:
        try:
            cmds.rotate( rotateX, rotateY, rotateZ , i + ".rotateAxis", os=True, relative=rotateRelative  )
        except:
            try:
                cmds.rotate( rotateX, rotateY, rotateZ , i, os=True, relative=rotateRelative  )
            except:
                print( "Couldn't rotate joint.")
                print(  traceback.format_exc(  )  )

class RiggerJointOrientHelperUi(object):
  def __init__(self, parentRef):
    self.parentRef = parentRef
    self.win = pm.window( title="Joint Orientation", width=250, height=180)
    self.col = pm.columnLayout()
    self.row1 = pm.rowColumnLayout(
      width = 200, 
      numberOfColumns=2 
      )
    self.rotateXText = pm.text(
      label="X rotate:",
      parent=self.row1 )
    self.rotateXField = pm.intField(
      parent=self.row1 )
    self.rotateYText = pm.text(
      label="Y rotate:",
      parent=self.row1 )
    self.rotateYField = pm.intField(
      parent=self.row1 )
    self.rotateZText = pm.text(
      label="Z rotate:",
      parent=self.row1 )
    self.rotateZField = pm.intField(
      parent=self.row1 )
    self.button = pm.button(
      label="Rotate Joints",
      width=200,
      command = lambda x: parentRef.rotateJoint(
         self.rotateXField.getValue() ,self.rotateYField.getValue() ,self.rotateZField.getValue()   ),
         parent=self.col )
    self.button = pm.button(
      label="Rotate Joints Relative",
      width=200,
      command = lambda x: parentRef.rotateJoint(
         self.rotateXField.getValue() ,self.rotateYField.getValue() ,self.rotateZField.getValue(), rotateRelative=True   ),
         parent=self.col )

    
    
    self.win.show()
    self.win.setWidth(260)
    self.win.setHeight(210)
