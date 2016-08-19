## convert object selection to polygons only
import pymel.all as pm
import maya.cmds as cmds
import os, sys, traceback


#user_path = user_path.replace( '/','\\')
#print(    help( type(user_path)  )    )


#print( l for l in os.walk(searchPath)  )
#print( searchPath )
#print os.path.exists( searchPath )


    def __init__(self, parentRef=None, mmmmToolsRef=None):
        self.mmmmTools = mmmmToolsRef

        self.scriptFileRunner = MmmmScriptFileRunner(
        self.win = pm.window("Script File Runner")
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.textPath = pm.text( "Path to scripts:" )
                self.textFieldPath = pm.textField(
                    text=self.scriptFileRunner.searchPath,
                    width=400,
                    changeCommand= lambda x : self.onTextPathChangeCommand()
                )
                self.btnRefresh = pm.button( "Refresh Scripts",
                self.text = pm.text( "Script File To Run:" )
                self.buildMenu(  )
                ## self.textFieldScript = pm.textField( width=500 )
                self.btnRunScript = pm.button(
                    "Run Script",
                    command = lambda x:
                        self.scriptFileRunner.runScript(
                        )
                )
        self.scriptFileRunner.changePath(
            self.textFieldPath.getText(), refresh=True
        )
        self.buildMenu( )
            print( traceback.format_exc()  )
        #for entry in self.ddMenuEntires:
        #    try:
        #        pm.deleteUI( entry )
        #    except:
        #        print( traceback.format_exc()  )


class MmmmScriptFileRunner(object):
    def __init__(self, parentRef=None, mmmmToolsRef=None, autoRun=False, searchPath=None):
        self.mmmmTools = mmmmToolsRef
        if autoRun==True:
            self.runScriptByUserInputNumber()
        
    def runScriptByUserInputNumber(self):
            userInput = input()
        except EOFError:
            pass
            userInput = None

        if type(userInput)==type(-1):
            self.runScript( self.scriptsFound[userInput] )
        sep = os.sep


        self.searchPath = os.path.join( userPath, 'scripts/MmmmTools/' + self.mmmmToolsSubfolderWithScripts )
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
            self.findScripts()
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
    def runScriptByNumber(self, number ):
        try:
            fh = open( absPathToScript, 'r' )
            code = fh.read()
            fh.close()
            execDict = {'mmmmTools':self.mmmmTools, 'pm':pm,  'cmds':cmds}
            exec code in execDict
        except:
            print(  traceback.format_exc()  )