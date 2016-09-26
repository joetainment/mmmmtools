import pymel.all as pm
import maya.cmds as cmds
import traceback

addableAttrList = [
"vray_subdivision",
"vray_subquality",
"vray_displacement",
]
## \r\n is for replaceing is notepad++



class AddVrayAttributeGroupUi(object):
    
    def __init__(self):
        self.win=pm.window()
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.label1 = pm.text( "Attribute Group Name (To Be Added)" )
                self.dropdown = pm.optionMenu( "menu", 
                    changeCommand = self.onDropDownChange                
                )
                with self.dropdown:
                    for i,v in enumerate(addableAttrList):
                        pm.menuItem( v )
                self.attrNameField = pm.textField( )
                self.addAttrButton = pm.button(
                    "Add Attribtutes!",
                    command = lambda x:  self.addAttributeGroup(
                       self.attrNameField.getText()
                    )
                )
                
        self.win.show()
    
    def onDropDownChange(self,  newDropdownValue ):
        self.attrNameField.setText(
            newDropdownValue
        )
       
    def addAttributeGroup( self, user_given_vray_attr_group ):
    
        ## Get selection
        sel = pm.ls(selection=True)
        ## Copy selection in case we modify the list
        objs = sel[:]
        
        for obj in objs:
            try:
                shp = obj
                try:
                    shp = obj.getShape()
                except:
                    shp = obj
                ##if hasattr( obj, "getShape" ):
                ##    shp = obj.getShape()
                pm.mel.eval(
                    'vray addAttributesFromGroup "'
                    + shp.name()
                    + '" "' + user_given_vray_attr_group + '" 1;'
                )
            except:
                print "not working"
        
        ##restore original selection
        pm.select(sel)



myUi = AddVrayAttributeGroupUi()