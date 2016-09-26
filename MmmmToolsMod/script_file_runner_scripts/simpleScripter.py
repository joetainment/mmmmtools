import pymel.all as pm

do_one_to_many = True
mel_command = "performTransferAttributes 0;"

class SimpleScripterUi(object):
    def __init__(self):
        self.simpleScripter = SimpleScripter()
        self.win = pm.window("Simple Scripter")
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.text = pm.text( "Mel Script code to repeat:" )
                self.textFieldScript = pm.textField( width=500, text=mel_command )
                self.btnOneToMany = pm.button(
                    "Run as One To Many",
                    command = lambda x:
                     self.simpleScripter.oneToMany(
                         self.textFieldScript.getText()
                     )
                )

class SimpleScripter(object):
    def __init__(self):
        pass
    def oneToMany(self, code):
        oSel = pm.ls(selection=True)
        objs = oSel[:]
        srcObj = objs.pop(0)
        
        for obj in objs:
            try:
                pm.select( srcObj )
                pm.select( obj, add=True )
                pm.mel.eval( code )
            except:
                print(  traceback.format_exc()  )
        pm.select( oSel )
            
            
s = SimpleScripterUi()
     
