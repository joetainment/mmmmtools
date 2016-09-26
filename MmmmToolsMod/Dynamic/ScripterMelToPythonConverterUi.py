import pymel.all as pm
import imp
import uuid
import maya.cmds as cmds
import pymel.all as pm
import pymel.tools.mel2py as mel2py
import traceback
import MmmmToolsMod
class ScripterMelToPythonConverterUi(object):
    def __init__(self,mmmmToolsRef=None,makeUi=True):
        #widthForAll = 900
        self.mmmmTools = mmmmToolsRef
        if self.mmmmTools == None:
            self.mmmmTools = MmmmToolsMod.Dynamic.MmmmTools.mmmmToolsInstance
        
        self.convertFunc = self.mmmmTools.u.convertMelToPython
        if makeUi==True:
            self.initUi()
        
    def initUi(self):
        win = self.win = pm.window("Mmmm Mel To Python Converter")
        with win:
          col = self.col = pm.columnLayout(adjustableColumn=True)
          with col:
          
            labelMel = self.labelMel = pm.text("Mel:")              
            tf01 = self.tf01 = pm.scrollField( wordWrap=True )
            btnRunMel = self.btnRunMel = pm.button("Run Mel",
              command= lambda x:  pm.mel.eval( self.tf01.getText()  )
            )            
            labelSpacer01 = self.labelSpacer01 = pm.text("\n")
            
            
            labelPython = self.labelPython = pm.text("Python:")
            tf02 = self.tf02 = pm.scrollField( editable=False,  wordWrap=True  )
            btnRunPython = self.btnRunMel = pm.button("Run Python",
              command= lambda x:  self.execPython( codeStr=self.tf02.getText() )
            )             
            labelSpacer02 = self.labelSpacer02 = pm.text("\n")
              

            btnConvert = self.btnConvert = pm.button("Convert Mel To Python",
              command= lambda x:
                  self.tf02.setText(
                      self.convertFunc( self.tf01.getText()  )
                  )
            )

            
        win.show()
        
    def execPython(self, codeStr=""):
        exec codeStr