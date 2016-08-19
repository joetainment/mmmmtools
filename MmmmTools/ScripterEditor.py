import pymel.all as pm
import imp
import uuid
import MmmmTools

class ScripterEditorUi(object):
    def __init__(self,mmmmToolsRef=None,makeUi=True):
        widthForAll = 900 
        self.mmmmTools = mmmmToolsRef
        self.attrName = 'notes'   ##'mmmmScriptStringAttr'
        self.activeScriptText = ''
        self.scriptModule = None
        self.node = None
        self.codeString = ''
        self.activeScriptLabelStartText = "Actice Script being Edited is:  "
        self.win = pm.window("Scripter - Editor", width=widthForAll)
        initialUuid = str( uuid.uuid4() ).replace('-','_')

        with self.win:
            self.col = pm.columnLayout( width=600 )
            with self.col:
                self.getScriptFromSelectionButton = pm.button(
                    label="Get or Make Script From Selection",
                    command=lambda x: self.getScriptFromSelection(),
                    width=widthForAll,
                )
                pm.text( " ")
                pm.text( "Script prefix: (it is recommended this be left as the default)" )
                self.scriptPrefixTextField = pm.textField(
                    text="script__",
                    width=widthForAll,
                )
                pm.text( "Script name: (it is recommended that you use a unique and descriptive name)" )                
                self.scriptNameTextField = pm.textField(
                    text=initialUuid,
                    width=widthForAll,
                )
                self.scriptGetButton = pm.button(
                    label="Make the script, or get the script if it already exists. (Works using the above fields, prefix and name.)",
                    command=lambda x: self.getScriptContents(),
                    width=widthForAll,
                )
                
                pm.text( " " )
                pm.text( "   " )  ## different spaces used to keep unique names
                self.activeScriptText = pm.text( self.activeScriptLabelStartText )
                pm.text( "Script contents: (Editing here will immediately edit the corresponding mmmmScriptStringAttr attribute on the object.)" )
                self.scriptContentsScrollField = pm.scrollField(
                    keyPressCommand = lambda x: self.setScriptContents(),
                    changeCommand = lambda x: self.setScriptContents(),
                    width=widthForAll, height=500,                    
                )
                self.scriptRunButton = pm.button(
                    label="Run Script Contents",
                    command=lambda x: self.runScript(),
                    width=widthForAll,
                )

    def updateScriptNames(self):
        self.scriptPrefix = self.scriptPrefixTextField.getText()
        self.scriptName = self.scriptNameTextField.getText()
        self.scriptFullName = self.scriptPrefix + self.scriptName
                                
    def updateInfo(self):
        s = self
       
        self.updateScriptNames()
        candidates = pm.ls( s.scriptFullName + "*" )
        
        if len(candidates)>1:
            try:
                foundObjs = pm.ls( s.scriptFullName )
                assert(  len(foundObjs)==1  )
                candidates[0]=foundObjs[0]
            except:
                print( 'Major problem found: you should have exactly one object'
                    'with that script name in your scene. Please double check'
                    ' your naming.'
                )
        elif len(candidates)==0:
            originalSelection = pm.ls(selection=True)  ## store selection to get it back later
            self.node = pm.createNode( 'transform', n=s.scriptFullName )   ## type, n=name
            try:
                scriptsParent = pm.ls( 'scripts*' )[0]
            except:
                scriptsParent = pm.createNode( 'transform', n='scripts' )
            pm.parent( self.node, scriptsParent )
            pm.select( originalSelection)  ## restore selection
            
        else:
            self.node = candidates[0]
            
        try:
            getattr(self.node, self.attrName)
        except:
            try:
                self.node.addAttr( self.attrName, dt='string' )
                print( 'An attribute named "' + self.attrName + '" was added to ' + self.node.name()  )                
            except:
                print( "Couldn't add attribute. Continuing anyway...")            
            
    def getScriptFromSelection(self):
        try:
            sel = pm.ls(selection=True)
            attr = None
            foundObj = None
            for obj in sel:
                try:
                    attr = getattr( obj, self.attrName ) 
                        ## this will fail if the attribute doesn't
                        ## exist, and the next line won't run
                    foundObj = obj
                except:
                    continue
            if foundObj is None:
                try:
                    foundObj= pm.ls(selection=True)[0]
                except:
                    print( "An object must be selected in order to get the script." )
                    raise
            else:
                self.node = foundObj
                n = foundObj.name()
                self.updateScriptNames()
                pre = self.scriptPrefix
                if n.startswith( pre ) and len(n) > len( pre ):
                    n = n[ len(self.scriptPrefix) : ]
                    self.scriptNameTextField.setText( n )
                else:
                    self.scriptPrefixTextField.setText('')
                    self.scriptPrefix = ''
                    self.scriptNameTextField.setText( n )
            self.getScriptContents()
        except:
            print( traceback.format_exc()  )
            print( "Couldn't get script from selection." )
       

    def getScriptContents(self):
        s = self
        self.updateInfo()
        

        self.codeString = getattr(self.node, self.attrName).get()
        if self.codeString is None:
            self.codeString = ''

        self.codeString = self.codeString.replace('\t','    ')
        self.scriptContentsScrollField.setText( self.codeString )
        self.activeScriptText.setLabel( self.scriptPrefix + self.scriptName )        
    
    
    def setScriptContents(self):
        self.updateInfo()
        self.codeString = self.scriptContentsScrollField.getText().replace('\t','    ')
        scriptAttr = getattr( self.node, self.attrName )
        scriptAttr.set( self.codeString )
        

    def runScript( self ):
        code = self.scriptContentsScrollField.getText()
        if len( self.scriptContentsScrollField.getText() ):
            self.setScriptContents()
        self.scriptModule = self.mmmmTools.scripter.runScriptCode( scriptName=self.scriptFullName, scriptCode=code )
        ##mmmmScripts = self.mmmmTools.scripter.scripts

    def importCode(self, name, code, add_to_sys_modules=0):
        import sys,imp
    
        module = imp.new_module(name)
    
        exec code in module.__dict__
        if add_to_sys_modules:
            sys.modules[name] = module
    
        return module
        
        
pass