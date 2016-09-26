import pymel.all as pm
import MmmmTools


mmmmTools = MmmmTools.MmmmTools.mmmmToolsInstance

UiFileLoader = mmmmTools.designFileLoader.UiFileLoader

class TestUi(UiFileLoader):
    def __init__(self, uiFile ):
        UiFileLoader.__init__(self, uiFile, autoHookup=False )
        
        nm = 'okButton'
        self.widgets[nm].setCommand(    getattr( self, 'okButton'+'OnClick' )    )    

        
    def okButtonOnClick(self,dummy):
        print( "hello world" )        




uiFile = r"""D:\Dropbox\maya\2013-x64\scripts\mmmmGenericWindow.ui"""
testUi = TestUi(uiFile)
