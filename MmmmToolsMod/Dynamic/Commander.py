"""
Viewer - Module containing functionality relating to 
    viewing objects, viewport controls, camerea, etc
"""

import pymel.all as pm
import pymel
import maya.cmds as cmds
import maya
import maya.OpenMaya as om

import traceback, math, random

import collections


#try
#    reload(SelectorVolumeSelect)
#except
#    try
#        import SelectorVolumeSelect
#    except
#        print( traceback.format_exc() )

class Entry(collections.OrderedDict):
    @property
    def name(self):
        return self['name']
    @name.setter
    def name(self, value):
        self['name'] = value
        
    @property
    def func(self):
        return self['func']
    @func.setter
    def func(self, value):
        self['func'] = value
        
    @property
    def annotation(self):
        return self['annotation']
    @annotation.setter
    def annotation(self, value):
        self['annotation'] = value
        
    @property
    def cmdAnnotation(self):
        return self['cmdAnnotation']
    @cmdAnnotation.setter
    def cmdAnnotation(self, value):
        self['cmdAnnotation'] = value
        
    @property
    def cmdName(self):
        return self['cmdName']
    @cmdName.setter
    def cmdName(self, value):
        self['cmdName'] = value
        
    @property
    def uiLabel(self):
        return self['uiLabel']
    @uiLabel.setter
    def uiLabel(self, value):
        self['uiLabel'] = value
        
    @property
    def inMenu(self):
        return self['inMenu']
    @inMenu.setter
    def inMenu(self, value):
        self['inMenu'] = value

    def __init__( self, *args, **kwargs):
        collections.OrderedDict.__init__( self, *args, **kwargs )
        
        self.name = kwargs.get('name')
        self.func = kwargs.get('func')
        self.annotation = kwargs.get('annotation', None)
        self.cmdAnnotation = kwargs.get('cmdAnnotation', None)
        self.cmdName = kwargs.get('cmdName', None)
        self.uiLabel = kwargs.get('uiLabel', None)
        self.inMenu = kwargs.get('inMenu', None)


class Commander(object):
    def __init__(self, parentRef):
        self.parent = parentRef
        self.mmmm = self.parent
        
        ## entries is the complex dictionary that stores the full info for each command
        self.entries = collections.OrderedDict()

        ## commands is a simpler dictionary mapping names to callables
        self.commands = collections.OrderedDict()
        
        ## commands is a simpler dictionary mapping names as dict keys to their vales which are mel cmd names
        self.commandsMelNames = collections.OrderedDict()
        
        self.addCommand( 'Commander/Hello', self.hello )
        self.addCommand( 'Commander/List', self.listCommands )
        self.addCommand( 'Commander/ListMel', self.listMelCommands )
        self.addCommand( 'Commander/ReloadMmmmTools', self.reloadMmmmTools, uiLabel='Reload MmmmTools', inMenu='Developer' )

    def listCommands(self):
            for k in self.commands.keys():
                print( k )
    def findKeyForRuntimeCommand(self):
        ## not implemented, but should give back the
        ## commandsMelNames
        ## key whose value is the given runtime command
        pass
    def listMelCommands(self, showKeys = False):
        self.listCommandsMelNames(showKeys=showKeys)
    def listCommandsMelNames(self, showKeys = False):
        if showKeys==False:
            for v in self.commandsMelNames.values():
                print( v )
        else:
            for k, v in self.commandsMelNames.items():
                print( k )
                print( v )
    
    def getMmmmCmd( self, name ):
        return self.commandsMelNames.get(name,None)
    
    def addCommand(self, name, func, annotation=None, uiLabel=None, uiMenuItem=None, inMenu=None ):

        cmdName = 'MmmmCmds__' + name.replace('/','__')
    
        if annotation==None:
            cmdAnnotation = cmdName + 'Annotation'
        else:
            cmdAnnotation = cmdName + '_' + annotation 
    
        entry=Entry(
            name=name,
            func=func,
            annotation=annotation,
            cmdAnnotation=cmdAnnotation,
            uiLabel=uiLabel,
            cmdName=cmdName,
            inMenu=inMenu
        )
        self.entries[name]=entry
        
        self.createRunTimeCommandForEntry( entry )
        self.commands[name]=func
        self.commandsMelNames[name] = cmdName
    
    ##def theUiLabel should have some string replacement magic to allow uiLabels to also specify priority

    

    def createRunTimeCommandForEntry( self, entry ):
        name = entry.name
        cmdName = entry.cmdName
        cmdAnnotation = entry.cmdAnnotation
    
        try:
            if cmds.runTimeCommand( cmdName, q=True, exists=True ):
                cmds.runTimeCommand( cmdName, e=True, delete=True )
                
            cmds.runTimeCommand(
                cmdName,
                annotation=cmdAnnotation,
                category="Custom Scripts",
                commandLanguage="python",
                hotkeyCtx="",
                command="mmmmTools.commander.commands['" + name + "']()"
            )
        except:
            print( "Error Creating Runtime Command" )                            
            print( traceback.format_exc()  )        

        #if uiMenuItem!=None:
            
        #if uiLabel!=None:
        #    self.addUi( );
    
        
    def hello(self):
        om.MGlobal.displayInfo( "Hello From Commander!")

    def reloadMmmmTools(self):
        #### The syntax here is really weird
        #### but, since we want to mimic how mel initialially starts with
        #### MmmmTools, but also with a reload, this is probably the best way!
        try:
            pm.mel.eval( """ python("reload(MmmmToolsMod)"); """ )
        except:
            print( traceback.format_exc() )
        try:
            pm.mel.eval( """ python("import MmmmToolsMod"); """ )
        except:
            print( traceback.format_exc() )
        try:
            pm.mel.eval( """ python("mmmmTools = MmmmToolsMod.Dynamic.MmmmTools()"); """ )
        except:
            print( traceback.format_exc() )
