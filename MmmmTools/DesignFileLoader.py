import pymel.all as pm
import maya.cmds as cmds
import StringIO
import sys


class UiElementInfo(object):
    def __init__(self, nameFull=None, nameShort=None, typ=None, parentWindow=None ):
        self.parentWindow = parentWindow
        self.nameFull = nameFull
        self.nameShort = nameShort
        self.typ = typ

class UiFileLoader(object):
    def __init__(self, uiFile, autoHookup=False):
        if autoHookup:
            print( "autoHooup not yet implemented" )
            
        self.widgets = {}
        uiInfoDict = self.loadUiFile( uiFile )
        design = uiInfoDict['design']
        self.design = design      
        elements = uiInfoDict['elements']
        
        ## Get info about all the created elements
        uiElementsInfos = self.makeUiElementInfos( elements, parentWindow=design )
        #print( uiElementsInfos )

        MapTypeToPymelClass = { 'QPushButton': pm.Button, 'QmayaLabel':pm.Text, 'QmayaField':pm.TextField, 'QmayaScrollField':pm.ScrollField }
        
        for el in uiElementsInfos.values():
            #print( el.nameShort )
            #print( el.typ )
            cFunc = MapTypeToPymelClass.get( el.typ, None )
            if not cFunc is None:
                #print( el.nameShort )
                print( el.nameFull )                
                self.widgets[ el.nameShort ] = cFunc( el.nameFull, edit=True )       

        #print( 'widget are:' )
        #for nm,el in self.widgets.items():
            #print( el.nameFull )
            
        
                
        #print( self.widgets['okButton'].getLabel()  )
        #self.widgets['okButton'].setLabel('ButtonWowy')
        self.widgets['okButton'].setCommand(    getattr( self, 'okButton'+'OnClick' )    )
        #print(        help(    type(self.widgets['okButton'])    )        )
                
        self.widgets['win'] = pm.Window( design, edit=True )
        self.widgets['win'].show()

    def fixUiElementsInfosToHaveFullPath(self, uiElementsInfos, windowName):
        """
        Get the full ui name of an element
        where elements is a dict of mel uiName/uiType pairs
        
        returns a new elements dict with full ui paths
        """
        allUiNames = cmds.lsUI( dumpWidgets=True )        
        inWindowUiNames = [ nm for nm in allUiNames if windowName in nm ]
        
        cleaned = {}
        for nm in inWindowUiNames:
            while nm.endswith('|'):
                nm = nm[:-1]
            cleaned[nm]=1
        inWindowUiNames = cleaned.keys()
        
        
        #print( 'inWindowUiNames is:')
        #print( inWindowUiNames )
        
        fullPathUiElementsInfos = {}
        for nm in inWindowUiNames:
            #print( uiElementsInfos )
            for elName, el in uiElementsInfos.items():
                if nm.endswith( el.nameShort):
                    newEl = UiElementInfo(
                        nameFull=nm,
                        nameShort=el.nameShort,
                        typ=el.typ,
                        parentWindow=el.parentWindow
                    )
                    
                    fullPathUiElementsInfos[nm] = newEl                   
        
        return fullPathUiElementsInfos
        
    def loadUiFile(self, uiFile):
        return self.loadUsingCmdsAndReturnInfoDict( uiFile )
  
    def loadUsingCmdsAndReturnInfoDict(self, uiFile):
        
        ## Remember where stuff was printing before
        seFile = 'c:/users/joe/mmmmScriptEditorHistory.txt'
        
        oldStatusOfHistoryFilename = cmds.scriptEditorInfo( query=True, historyFilename=True )
        oldStatusOfWriteHistory = cmds.scriptEditorInfo( query=True, writeHistory=True )

        ## Redirect printing        
        cmds.scriptEditorInfo( historyFilename=seFile )
        cmds.scriptEditorInfo( writeHistory=1 )
        
        cmds.scriptEditorInfo(clearHistoryFile=True)
        design = cmds.loadUI( uiFile=uiFile, v=True )
        
        ## Restore remembered old print location
        cmds.scriptEditorInfo( historyFilename=oldStatusOfHistoryFilename )
        cmds.scriptEditorInfo( writeHistory=oldStatusOfWriteHistory )
        
        fh = open(seFile,'r')
        printed = fh.read()
        fh.close()
        uiElements = self.splitUiPrintout( printed )

        result = { 'design':design, 'elements':uiElements }
            
        return result

    def makeUiElementInfos(self, elements, parentWindow):
        infos = {}
        for nm, typ in elements.items():
            infos[nm]=UiElementInfo(
                nameShort=nm,
                typ=typ,
                parentWindow=parentWindow
            )
            
        ## Make the elements have full paths
        ## Before the next line, they are just the short name
        infos = self.fixUiElementsInfosToHaveFullPath( infos, parentWindow )            
        return infos

    def splitUiPrintout( self, printed ):
        uiElements = {}
        lines = printed.split('\r\n')

        for line in lines:
            if line.startswith( '# Creating a '):
                #print( 'line is:' )
                #print( line )
                
                sections = line.split('"')
           
                #print( 'sections is:' )
                #print( sections )
                inQuotes = False
                lineName = ''
                lineType = ''
                for sec in sections:
                    if not inQuotes:
                        l = line.replace('# Creating a ', '' )
                        l = l.replace('.', '' )
                        l = l.split( ' named' )[0]
                        #print( 'l is:' )
                        #print( l )
                        lineType = l                    
                    else:
                        lineName = sec
                        uiElements[lineName] = lineType

                    ## make quote state opposite next time
                    ## through for loop
                    inQuotes = not inQuotes
        return uiElements