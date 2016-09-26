## convert object selection to polygons only
import pymel.all as pm
import maya.cmds as cmds
import os, sys, traceback


#user_path = user_path.replace( '/','\\')
#print(    help( type(user_path)  )    )


#print( l for l in os.walk(searchPath)  )
#print( searchPath )
#print os.path.exists( searchPath )

class ScriptFileRunnerUi(object):
    def __init__(self, parentRef=None, mmmmToolsRef=None):
        self.mmmmTools = mmmmToolsRef        self.parentRef = parentRef

        self.scriptFileRunner = MmmmScriptFileRunner(            parentRef = self,            mmmmToolsRef=self.mmmmTools        )        self.scriptFileRunner.findScripts()
        self.win = pm.window("Script File Runner")                self.ddMenuEntires = [ ]
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.textPath = pm.text( "Path to scripts:" )
                self.textFieldPath = pm.textField(
                    text=self.scriptFileRunner.searchPath,
                    width=400,
                    changeCommand= lambda x : self.onTextPathChangeCommand()
                )
                self.btnRefresh = pm.button( "Refresh Scripts",                    command = lambda x: self.buildMenu( )                )
                self.text = pm.text( "Script File To Run:" )                self.ddMenu = pm.optionMenu( changeCommand = self.onDdMenuChange )
                self.buildMenu(  )
                ## self.textFieldScript = pm.textField( width=500 )
                self.btnRunScript = pm.button(
                    "Run Script",
                    command = lambda x:
                        self.scriptFileRunner.runScript(                            self.chosenScript
                        )
                )        self.win.show()    def onTextPathChangeCommand(self):
        self.scriptFileRunner.changePath(
            self.textFieldPath.getText(), refresh=True
        )
        self.buildMenu( )    def buildMenu(self):        menuToBuildOn = self.ddMenu        try:            menuToBuildOn.clear()        except:
            print( traceback.format_exc()  )        self.scriptFileRunner.findScripts()        #print( help( type(self.ddMenu) )  )
        #for entry in self.ddMenuEntires:
        #    try:
        #        pm.deleteUI( entry )
        #    except:
        #        print( traceback.format_exc()  )
        with menuToBuildOn:            for script in self.scriptFileRunner.scriptsFound:                tmp = pm.menuItem( label=script)                self.ddMenuEntires.append( tmp )    def onDdMenuChange( self, choice ):        self.chosenScript = choice                

class MmmmScriptFileRunner(object):
    def __init__(self, parentRef=None, mmmmToolsRef=None, autoRun=False, searchPath=None):
        self.mmmmTools = mmmmToolsRef        self.mmmmToolsSubfolderWithScripts = 'script_file_runner_scripts'        self.scriptsFound = []        self.initSearchPath()
        if autoRun==True:
            self.runScriptByUserInputNumber()
        
    def runScriptByUserInputNumber(self):        self.findScripts()        try:
            userInput = input()
        except EOFError:
            pass
            userInput = None

        if type(userInput)==type(-1):
            self.runScript( self.scriptsFound[userInput] )    def initSearchPath(self):        userPath = self.mmmmTools.utils.getMayaPath().str()
        sep = os.sep


        self.searchPath = os.path.join( userPath, 'scripts/MmmmToolsMod/' + self.mmmmToolsSubfolderWithScripts )
        self.searchPath = self.searchPath.replace( '/', '\\' )

        ## Quick hack to make it work off windows
        ##  **** should be fixed later to use pather
        if os.sep == '/':
            self.searchPath = self.searchPath.replace( '\\', '/' )
            
    def changePath( self, newPath, refresh=False ):
        if os.sep == '/':
            newPath = newPath.replace( '\\', '/' )
        else:
            newPath = newPath.replace( '/', '\\' )
        self.searchPath = newPath
        print( self.searchPath )
        if refresh==True:
            self.findScripts()    def findScripts(self):
        ## Clear scripts found
        self.scriptsFound = []
        
        count = 0
        for dirpath, dnames, fnames in os.walk( self.searchPath ):
            #print "hey"
            for fname in fnames:
                n = os.path.join( dirpath, fname )
                if n.endswith( '.py' ) or n.endswith( '.txt' ):
                    self.scriptsFound.append( n )
                    print(    str( count ) + ":  " + n    )
                    count+=1
    def runScriptByNumber(self, number ):        self.runScript( self.scriptsFound[ number ] )    def runScript( self, absPathToScript ):
        try:
            fh = open( absPathToScript, 'r' )
            code = fh.read()
            fh.close()
            execDict = {'mmmmTools':self.mmmmTools, 'pm':pm,  'cmds':cmds}
            exec code in execDict
        except:
            print(  traceback.format_exc()  )