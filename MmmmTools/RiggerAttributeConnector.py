import maya.cmds as cmds
import pymel.all as pm


class RiggerAttributeConnector(object):
    def __init__(self, showUi=False, go=True, sourceAttrName='', targetAttrName=''):
        if showUi == True:
            self.ui = RiggerAttributeConnectorUi( parent = self )
            
        elif go==True:
            ## if any default behaviour makes sense, put it here
            tmp = 0
            
    
    def connectAttributes( self, sourceAttrName, targetAttrName, multiplier=0.0 ):

        sourceAttrName = sourceAttrName
        targetAttrName = targetAttrName

        multValue = multiplier
                ##print( help( multValue )   )
        
        ## Get a list of all selected objects
        objs = pm.ls( selection=True )
        
        sourceObj = objs.pop( 0 )
        sourceAttr = getattr( sourceObj, sourceAttrName ) 
        
        doMult = False
        if multiplier != 0.0:
            doMult = True
        
        if doMult:
            m = pm.createNode( "multiplyDivide" )
            m.input2X.set( multValue )
        
        ## Loop through all the selected objects, except the first one
        for obj in objs:
            ## This stuff might fail, so put it in a try block
            try:
                targetAttr = getattr( obj, targetAttrName ) 
                if doMult:
                    sourceAttr >> m.input1X
                    m.outputX >> targetAttr   
                else:
                    sourceAttr >> targetAttr
                
            except:
                print( "An error occured on object: " + obj.name() + "\n"
                    + traceback.format_exc() + "\n"
                )        
        
        
class RiggerAttributeConnectorUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.win = pm.window( "Attribute Connector" )
        
        self.go()
        
    def go(self):
        with self.win:
            self.col = pm.columnLayout()
            
            self.sourceText = pm.text( "Attribute source" )
            self.sourceField = pm.textField( width = 300 )
             
            self.text7 = pm.text( " " )
            self.targetText = pm.text( "Attribute target" )
            
            ## text that says attribute
            ## place to enter text for which attribute
            self.targetField = pm.textField( width = 300)
            
            self.text5 = pm.text( " " )  
            self.text6 = pm.text( "Multiplier (Only has affects resut if it is changed from the default 0.0 to another number.)" )
            self.multField = pm.floatField( width=300 ) 
            
            
            
            self.button = pm.button(
                "Connect the attribute of the source to all the targets \n (source is first selected)",
                command = lambda x: self.parent.connectAttributes(
                    sourceAttrName = self.sourceField.getText(),
                    targetAttrName = self.targetField.getText(),
                    multiplier = self.multField.getValue()
                )
            )
            ## text that says value
            ## place to enter the new value
        self.win.show( )