import pymel.all as pm
import random
import math
import traceback


helpString=""" 
Actual python code can be evaluated for the new value.
        i is the current iteration
        r is python's random module
        m is python's math module
        pm is pymel
        
    for example you could enter "translate" as the attribute to change
    and use the following code to change the attributes on many objects.
    Try it on a bunch of default cubes. (perhaps 20 cubes?)
    
    (  r(-0.3,0.3), i, m.sin(i)/3  )
"""

 
class RiggerAttributeSetter(object):
  def __init__(self, showUi=False, go=True, attribute='', value=''):
    if showUi:
      self.ui = RiggerAttributeSetterUi(parent=self)
    else:
      if go==True:
        self.setAttributes( attribute, value )
    
  def setAttributes(self, attribute, value):
    ## Get a list of all selected objects
    objs = pm.ls(selection=True)
    attribute = str(attribute)
    ## Loop through the list, and try setting each object
    for i,obj in enumerate(objs):
        ## Get the attribute based on the attribute name in the UI
        try:
            attr = getattr(  obj,  attribute   )
            a = attr.get()
            r = random.uniform
            m = math
            #i = i  ## just a reminder!  i is useful
        
            ## Get the value from the UI
            val = eval(  value  )
            ## Convert the value from the UI into a floating point number
        
        
        
            attr.set(  val  )
        except:
          print('Failed for object' + obj.name()  )
          print( traceback.format_exc() )
   

class RiggerAttributeSetterUi(object):
  def __init__(self, parent):
    self.parent = parent
    self.win = pm.window('Attribute Setter', resizeToFitChildren=True)
    with self.win:
      self.col = pm.columnLayout()
      with self.col:
        self.helpButton = pm.button(
          label="Show Help",
          command=lambda x: self.showHelp(),
        )      
        ## Text label that says "Attribute to change:"
        self.attributeLabel = pm.text( 'Attribute to change:' )
        ## Text entry field, a place where the user will type in the attribute to change
        self.attributeField = pm.textField(  width=600   )
        ## Text label that says "New value for attribute:"
        self.valueLabel = pm.text( 'New value for attribute:' )
        ## Text entry field, a place where the user will type the new value to set the attribute to
        self.valueField = pm.textField(   width=600  )
        
        self.go = pm.button(
          label="Set Attributes",
          command=lambda x: self.parent.setAttributes(
            attribute=self.attributeField.getText(),
            value=self.valueField.getText(),
          )
        ) 
        
  def showHelp(self):
    helpWindow = pm.window('Attribute Setter Help', resizeToFitChildren=True)
    with helpWindow:
      helpCol = pm.columnLayout()
      with helpCol:  
        helpText = pm.text( helpString )
    helpWindow.show()