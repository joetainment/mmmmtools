## MmmmTools   -  Usability Improvements For Maya
## Copyright (C) <2008>  Joseph Crawford
##
## This file is part of MmmmTools.
##
## MmmmTools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MmmmTools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
################################################
## More information is available:
## MmmmTools website - http://celestinestudios.com/mmmmtools
################################################



"""
MmmmTools hotkey functionality module.  The main purpose is for
allowing users to switch between multiple sets of hotkeys
"on the fly", which can result in significant speed up.

This allows the user to use a large number of unmodified keyboard keys
as hotkeys, rather than the usually crowded keyboard shortcut where
nearly every unmodified key is already taken.

This module also provides a great head start for people that haven't spent
a lot of time setting up hotkeys in Maya, as it provides hotkeys for many
functions that are commonly used in Maya but that do not have default hotkeys.
"""

import maya.cmds as cmds
import pymel.all as pm
import maya.mel
import maya.OpenMaya as om
import traceback


##import MmmmTools.UtilsMod as Utils



#Note:
# Of crucial importance!!!
#                    Annotations must be different for nameCommand 
#This cost about 4 hours of time because annotations would seem to be just comments, and you'd think duplicates wouldn't matter,
#but they do!  Stupid Maya....


## we often use   keySetName  instead of   setName   since
## setName is potentially confusing and seems like a method that sets a name
## when it's hotkeySet the s is capitalized to match maya's naming
## when it's keySet  the s is upper case
## the k in hotkey is not ever capitalized

class Hotkeys(object):
    """
    Hotkey manager Class.  It will set everything up upon initialization,
    after which it can be called when the user wishes to change hotkey
    sets. Note that this will only happen if the ini token is set as follows:
        enable_hotkeys=1
    ****The user interface should allow an easy method for turning on the
    enable hotkeys functions, and perhaps even ask the user when they first open it.
    """
    def __init__(self, parent):
        """
        Initialize Everything and Setup The Hotkeys manager so it can be called later.
        The calling object should be passed as a parent when this class is created.
        """
        ## Setup initial references to the main MmmmTools system and its importand parts such as configuration
        self.parent = parent
        self.mmmm = self.parent
        self.keySetPrefix = "Mmmm_"
        self.entryListsByKeySet = {}
        self.initModulesForDefinitions()
        ## self.initEntriesForDefault()
        
        #keySetFullName = self.keySetPrefix + keySetShortName
        for entryListName, entryList   in   self.entryListsByKeySet.items():
            self.createHotkeySet( entryListName )
            for entry in entryList:
                entry['set'] = entryListName
                self.createHotkeyAndRequiredFromEntry( entry )
        
        if  pm.hotkeySet( current=True, query=True ).startswith( "Mmmm_" ):
            pm.hotkeySet( "Maya_Default", current=True, edit=True )

        commander = self.mmmm.commander     
        commander.addCommand(
            'Hotkeys/HotkeysUi',
            self.createUi    
        )
        
        commander.addCommand(
            'Hotkeys/NextKeySet',
            self.nextKeySet
        )
        commander.addCommand(
            'Hotkeys/PrevKeySet',
            self.prevKeySet
        )
        
    def cycleKeySet(self,backwards=False):
        ## this should cycle between hotkey sets
        
        #first make a list of all hotkey sets
        #sort it alphabetically and make an index for each one
        #get the index of our current set
        # if there is a next index, switch to it
        # else we are last index, switch to index 0
        sets = pm.hotkeySet( query=True, hotkeySetArray=True)
        sets.sort()
        currentSet = pm.hotkeySet( current=True, query=True )
        #print( sets )
        #print( currentSet )
        
        index = sets.index(currentSet)
        
        if not backwards:
            index += 1
            if index >= len(sets):
                index=0
        else:
            index -= 1
            if index < 0:
                index = len(sets)-1
                
        newKeySet = sets[index]
        om.MGlobal.displayInfo( newKeySet + "  Hotkey Set Activated" );
        pm.hotkeySet( newKeySet, current=True, edit=True )
    
    def nextKeySet(self):
        self.cycleKeySet()
        
    def prevKeySet(self):
        self.cycleKeySet(backwards=True)
    
    def listHotkeySets(self):
        sets = pm.hotkeySet( query=True, hotkeySetArray=True)
        print(sets)
        return sets
    
    def createMmmmHotkeySet(self, keySetNameNoPrefix, sourceSetName = "Maya_Default" ):
        setFullName = self.keySetPrefix + keySetNameNoPrefix
        self.createHotkeySet( setFullName )
    
    def createHotkeySet(self, keySetFullName, sourceSetName = "Maya_Default", ):
        isDeleted = False
        isExisting = pm.hotkeySet( keySetFullName, query=True, exists=True)
        if isExisting==True:
            print( "deleting")
            isDeleted = pm.hotkeySet( keySetFullName, edit=True, delete=True)
        else:
            print( "not deleting, did not already exist")
        
        result = pm.hotkeySet( keySetFullName, source = sourceSetName )  ## create=True is implied but can't be specified without maya error        
        
        #self.MmmmHotkeys Polygons
    
    
    
    def switchToHotkeySet( self, keySetNameNoPrefix ):
        self.switchToHotkeySet( self.keySetPrefix)
        pm.hotkeySet( keySetFullName, edit=True, current=True)
    
    def switchToHotkeySet( self, keySetFullName ):
        pm.hotkeySet( keySetFullName, edit=True, current=True)
        
    def initForSetPolygons(self):
        x=0
    
    def getSetFullName(self, shortName ):
        return self.keySetPrefix+shortName
    
    def initEntriesForModeling(self):
        x=0
        
    def initEntriesForDefault(self):
        x=0
        
    def initModulesForDefinitions(self):
        self.imported_modules = {}
        hotkey_modules_to_import =[    
            'Mmmm_Default',    
            'Mmmm_Polygons',    
            'Mmmm_Uvs',    
            'Mmmm_Rendering',
        ]
        importCode = """
try:
    *module*=*module*
    ## if we get this far, then the module must exist, and we should reload it
    try:
        reload(*module*)
    except:
        ## in this case, the reload fails, so print the traceback
        print( traceback.format_exc() )
    
except:
    ## in this case, *module* has never been loaded before
    try:
        import *module*
    except:
        ## in this case, the import fails, so print the traceback
        print( traceback.format_exc() )
"""
        for m in hotkey_modules_to_import:
            loc = locals()
            glb = globals()
            exec( importCode.replace('*module*', m ) , glb, loc )
            imported_module = glb[m]
            self.imported_modules[m] = imported_module
                
    
        for key, m in self.imported_modules.items():
            self.entryListsByKeySet[key] = m.getEntries()
            
            
        
        
        
    
        
        

        
    def createHotkeyAndRequiredFromEntry(self, entry ):
        hotkeySetAtFunctionStart = pm.hotkeySet( current=True, query=True )

        i = entry                  
        pm.hotkeySet( i['set'], current=True, edit=True )


        ## Determine which modifiers are being used. (Because Maya is already naturally
        ## sensitive to shift, by using capitals or symbols, we don't test for shift.
        try:
            try:
                isCtl=i['ctl']
            except:
                isCtl=False
            try:
                isAlt=i['alt']
            except:
                isAlt=False
        except:
            pass
        ## Based on the above logic, generate strings to be used while creating the hotkeys.    
        if isAlt == True:
            AltString = " Alt + "
        else:
            AltString = " "        
        if isCtl == True:
            CtlString = " Ctrl + "
        else:
            CtlString = " "

        if not i.get('doRelease',False):
            ## Create a printout of the command being made and the hotkey that will use it.
            print(  "About to add runTimeCommand and nameCommand named "\
                + i['name'] + "         Pushing: " + CtlString + AltString + i['key']  )
            try:
                if cmds.runTimeCommand( i['name'], q=True, exists=True ):
                    cmds.runTimeCommand( i['name'], e=True, delete=True )
                    
                cmds.runTimeCommand(
                    i['name'],
                    annotation=i['annotation'],
                    category="Custom Scripts",
                    commandLanguage="mel",
                    hotkeyCtx="",
                    command=i['mel']
                )
            except:
                print( "Error Creating Runtime Command" )                            
                print( traceback.format_exc()  )
                
            try:
                cmds.nameCommand(
                    i['name']+"NameCommand",
                    annotation=i['annotation'],
                    sourceType='mel',
                    command=i['name']
                )
            except:
                print( "Error Creating Named Command" )
            ## Add the actual hotkey to Maya.
            try:                    
                cmds.hotkey( k=i['key'], name=i['name']+"NameCommand", ctl=isCtl, alt=isAlt)
            except:
                print( "Error Binding Hotkey" )
                print( traceback.format_exc()  )


        
        if i.get('doRelease',False):
            ## Create a printout of the command being made and the hotkey that will use it.
            print(  "About to add nameCommandRelease named " + i['name'] + "         Releasing: " + CtlString + AltString + i['key']  )
            
        try:
            if cmds.runTimeCommand( i['name']+"Release", q=True, exists=True ):
                cmds.runTimeCommand( i['name']+"Release", e=True, delete=True )
                
            cmds.runTimeCommand(
                i['name']+"Release",
                annotation=i['annotation'],
                category="Custom Scripts",
                commandLanguage="mel",
                hotkeyCtx="",
                command=i['mel']
            )
        except:
            print( "Error Creating Runtime Command" )                            
            print( traceback.format_exc()  )            
            
            try:
                cmds.nameCommand( i['name']+"Release", annotation=i['annotation']+"Release", command=i['mel']+"Release" )
            except:
                print( "Error Creating Named Command" )

            ## Add the actual hotkey to Maya.                
            try:
                ##Its very important that Release is added to name string below.
                cmds.hotkey( k=i['key'], ctl=isCtl, alt=isAlt ,releaseName=i['name']+"Release" )
            except:
                print( "Error Binding Hotkey" )                    

        pm.hotkeySet( hotkeySetAtFunctionStart, current=True, edit=True )

    def createUi(self, parentWidget=None):
        self.ui = HotkeysUi( self, parentWidget=parentWidget, mmmm=self.mmmm )
        return self.ui


class HotkeysUi(object):
    def __init__(self, parentRef, parentWidget=None, mmmm=None ):
        self.parentRef = parentRef
        self.buttons = []
        self.widgets = {}
        
        self.mmmm = mmmm
        

        if parentWidget==None:
            parentWidget = self.widgets['parentWidget'] = pm.Window(
                sizeable = True, title = "Mmmm Hotkeys Manager", titleBar=True
            )
        else:
            self.widgets['parentWidget'] = parentWidget

        with parentWidget:
            self.layout = pm.columnLayout()
            with self.layout:
            
                self.widgets['editorBtn'] =  pm.button( "Maya Hotkey Editor Window...",
                    annotation=
                        "Open the Maya's default builtin hotkey editor window. "
                        +
                        " There is nothing MmmmTools specific about this, it's just a shortcut.",
                    command='pm.mel.eval("HotkeyPreferencesWindow;")',
                )
                
                self.widgets['infoText'] = pm.text("\nInstructions (read tooltip, hover here)\n",
                                    annotation = 
                      "Note that users should avoid editing the hotkey sets \n"
                    + "starting with Mmmm. If you wish to modify them, \n"
                    + "you should duplicate the Mmmm keyset you want to modify, \n"
                    + "rename, so it does not start with Mmmm, and make change to your own copy. \n\n"
                    + "Changing the Mmmm keySets themselves requires writing/altering python code. \n"
                    + "Our recommendation is that for your own hotkeys, you make your own hotkey sets, \n"
                    + "and switch to them as necessary. (See other button tooltips for more info.)"
                )
                
                                
                self.widgets['nextKeySetBtn'] = pm.button( "Next Hotkey Set",
                    command = lambda x: self.parentRef.nextKeySet(),
                    annotation="Go to the next keyset, in alphabetical order. \n\n "
                    + "In case you want to add it to a shelf/button: \n"
                    + "The mel command to do this is: MmmmCmds__Hotkeys__NextKeySet",
                )
                self.widgets['prevKeySetBtn'] = pm.button( "Prev Hotkey Set",
                    command = lambda x: self.parentRef.prevKeySet(),
                    annotation="Go to the previous keyset, in alphabetical order. \n\n "
                    + "In case you want to add it to a shelf/button: \n"
                    + "The mel command to do this is: MmmmCmds__Hotkeys__PrevKeySet",
                )
                
                #self.widgets['refreshListBtn'] = pm.button( "Refresh Hotkey Set Dropdown List" )
                self.widgets['dropdownLabel'] =  pm.text("\n Choose active hotkey set:",
                    annotation="You may need to either click the refresh button, "
                    +"or if that is unavailable, close and reopen this window, to refresh the list."
                )
                
                self.widgets['dropdown'] = pm.optionMenu( "MmmmKeySetDropdownMenu", 
                    changeCommand = self.onDropDownChange,
                )
                keySets = pm.hotkeySet( query=True, hotkeySetArray=True)
                keySets.sort()
                for keySet in keySets :
                    pm.menuItem( keySet )

        
    def onDropDownChange(self,selected):
        pm.hotkeySet( selected, current=True, edit=True )
        om.MGlobal.displayInfo( selected + "  Hotkey Set Activated" );

