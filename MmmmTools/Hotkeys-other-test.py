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
import traceback

import MmmmTools

from Utils import Utils

u = U = Utils

#Note:
# Of crucial importance!!!
#                    Annotations must be different for nameCommand 
#This cost about 4 hours of time because annotations would seem to be just comments, and you'd think duplicates wouldn't matter,
#but they do!  Stupid Maya....

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
        self.ini = parent.ini
        self.conf = self.ini.conf
        self.pman = self.mmmm.platformManager
        self.info = self.pman.info
        
        #self.conf.env_prefs = self.conf.env_user_maya_path_and_version + "/prefs"
        self.conf.hotKeyFiles = [ "userNamedCommands.mel", "userRunTimeCommands.mel", "userHotkeys.mel" ]
        self.conf.mmmmUserHotKeyFiles = \
            [   "userNamedCommands.mel.1.MmmmTools.Hotkeys.mel", \
                "userRunTimeCommands.mel.1.MmmmTools.Hotkeys.mel", \
                "userHotkeys.mel.1.MmmmTools.Hotkeys.mel" ]
        #print(  "Enabled is:   " + self.ini.getItem("enable_hotkeys")  )
        
        ## Check to see if the ini file shows hotkeys enabled, and if it does
        ## start the hotkey manager.
        self.enabled = False
        try:
            if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
                self.enabled = True
            else:
                #print("Hotkeys not enabled.")
                pass
        except:
            print("\n  Could not load hotkeys or could not find Hotkey data in config Files. \n")

        if self.enabled:
            self.startHotkeys()
            
    def startHotkeys(self):
        self.namedCommands = []
        self.namedCommandsRelease = []
        
        self.checkForMmmmToolsUserHotkeys()
            
        self.setHotkeysToDefaults()
        
    def go(self):
        if self.enabled:
            self.applyUserHotkeys()
            #self.setHotkeysToDefaults()
            print( "The Hotkeys manager is starting to go!" )

        
        
    def saveHotkeys(self):
        #maya.mel.eval("hotkeyEditorSave;")
        cmds.savePrefs(hotkeys = True)

        print("Hotkeys are trying to save..." + self.conf.hotKeyFiles[0])
        
        countdown = [8,7,6,5,4,3,2,1]
        for i in range(len(countdown)):
            #print( '\n' + str(countdown[i]) + '\n' )
            for f in self.conf.hotKeyFiles:
                namePather = \
                    self.info.maya.maya_app_dir_with_version_prefs_pather \
                    + f
                sourceOfBackup_str = \
                    namePather.st + \
                    "." + str(countdown[i]) + ".MmmmTools.Hotkeys.mel"
                destination_str = \
                    namePather.st + \
                    "." + str(countdown[i]+1) + ".MmmmTools.Hotkeys.mel"
                
                destination_str = \
                    destination_str.replace('\\','/' )
            
                sourceOfBackup_str = sourceOfBackup_str.replace('\\','/' )
                
                    
                cmds.sysFile( sourceOfBackup_str, copy=destination_str) 
                #print( "saved file:  " + name + " to " + destination )    
            
        #save the actual hotkeys .mel files to the new MmmmTools.Hotkeys.mel files
        i = 1
        for f in self.conf.hotKeyFiles:
            namePather = \
                    self.info.maya.maya_app_dir_with_version_prefs_pather \
                    + f
            destination_str = \
                    namePather.st + \
                    "." + "1" + ".MmmmTools.Hotkeys.mel"

            destination_str = \
                 destination_str.replace('\\','/' )
            
            name_str = namePather.st.replace('\\','/' )
            
            cmds.sysFile( name_str, copy=destination_str) 
        
    def goBackToOlderHotkeys(self):
        countdown = [8,7,6,5,4,3,2,1]
        for i in range(len(countdown)):
            for f in self.conf.hotKeyFiles:
                namePather = \
                    self.info.maya.maya_app_dir_with_version_prefs_pather \
                    + f
                destination_str = \
                    namePather.st + \
                    "." + str(countdown[i]) + \
                    ".MmmmTools.Hotkeys.mel"
                sourceOfOldHotkeys_str = \
                    namePather.st + \
                    ( "." + str(countdown[i]+1) + ".MmmmTools.Hotkeys.mel" )
                
                destination_str = \
                    destination_str.replace('\\','/' )
                sourceOfOldHotkeys_str = \
                    sourceOfOldHotkeys_str.replace('\\','/' )
                
                cmds.sysFile( sourceOfOldHotkeys_str, copy=destination_str) 
        

    def checkForMmmmToolsUserHotkeys(self):
        for f in self.conf.hotKeyFiles:
            #Make    name   equal to one of the hotkey preferences file (there are really three important ones that we loop through)
            namePather = \
                self.info.maya.maya_app_dir_with_version_prefs_pather \
                + f
                
            #print(name)
            fileToCheckFor_str = \
                namePather.st + \
                "." + "1" + ".MmmmTools.Hotkeys.mel"
            destination_str = \
                namePather.st + \
                "." + "1" + ".MmmmTools.Hotkeys.mel.deleteme"
            
            
            ## Since maya cmds is handling the file operations here,
            ## be sure to use unix style paths...
            fileToCheckFor_str = fileToCheckFor_str.replace( '\\', '/' )
            destination_str = destination_str.replace( '\\', '/' )
            name_str = namePather.st.replace( '\\', '/' )
            
            #Test the presence of a file by attempting to copy it
            test = cmds.sysFile( fileToCheckFor_str, copy=destination_str)
            
            ##If the file doesn't exist, make it
            ## However, if the file did exist, and the copy suceeds,
            ## we delete the copy
            if test == False:
                cmds.sysFile( name_str, copy=fileToCheckFor_str) 
            else:
                cmds.sysFile( destination_str, delete=True )

        
    def applyUserHotkeys(self):
    
        
        """
        for f in self.conf.mmmmUserHotKeyFiles:
            namePather = \
                self.info.maya.maya_app_dir_with_version_prefs_pather \
                + f
            name_str = namePather.st.replace( '\\', '/' )
            try:
                maya.mel.eval( 'source ' + '"' + name_str + '";' )
            except Exception, exception:
                print( "\n\n\n   There was an error running the following script:" +\
                        str(f) +  "\n The error was:  " + str(exception)  )
        """
        pass
        
    def getMayaVersionAsFloat(self):
        versionFull = cmds.about(v=True)
        versionSplitList = versionFull.split(".")
        versionString = versionSplitList[0]
        version = float(versionString)
        return version

    def applyHotkeys(self):
        if self.getMayaVersionAsFloat() >= 2016.0 :
            try:
                cmds.hotkeySet( "Mmmm_Default", edit=True, delete=True )
            except:
                print( traceback.format_exc() )
            try:
                cmds.hotkeySet( "Mmmm_Default", source="Maya_Default", current=True )
            except:
                print( traceback.format_exc() )
        self.applyHotkeysRelease()  #might need to run before the Press command
        self.applyHotkeysPress()

    def applyHotkeysPress(self):        
        """
        Applies press hotkeys in the situations that require it. (Release hotkeys are in another function.)
        """
        if self.getMayaVersionAsFloat() >= 2016.0:
            self.applyHotkeysPress2016AndLater()
        else:
            self.applyHotkeysPress2015AndEarlier()
            
            
    def applyHotkeysPress2016AndLater(self):     
            for i in self.namedCommands:
                
                ## Determine which modifiers are being used. (Because Maya is already naturally
                ## sensitive to shift, by using capitals or symbols, we don't test for shift.
                try:
                    try:
                        isCtlPressed=i['ctl']
                    except:
                        isCtlPressed=False
                    try:
                        isAltPressed=i['alt']
                    except:
                        isAltPressed=False
                except:
                    pass
                ## Based on the above logic, generate strings to be used while creating the hotkeys.    
                if isAltPressed == True:
                    AltPressedString = " Alt + "
                else:
                    AltPressedString = " "        
                if isCtlPressed == True:
                    CtlPressedString = " Ctrl + "
                else:
                    CtlPressedString = " "
            
                ## Create a printout of the command being made and the hotkey that will use it.
                print(  "About to add runTimeCommand and nameCommand named "\
                    + i['name'] + "         Pushing: " + CtlPressedString + AltPressedString + i['key']  )
                try:
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
                    cmds.hotkey( k=i['key'], name=i['name']+"NameCommand", ctl=isCtlPressed, alt=isAltPressed)
                except:
                    print( "Error Binding Hotkey" )
                    print( traceback.format_exc()  )                

    def applyHotkeysPress2015AndEarlier(self):                         
        for i in self.namedCommands:
            
            ## Determine which modifiers are being used. (Because Maya is already naturally
            ## sensitive to shift, by using capitals or symbols, we don't test for shift.
            try:
                try:
                    isCtlPressed=i['ctl']
                except:
                    isCtlPressed=False
                try:
                    isAltPressed=i['alt']
                except:
                    isAltPressed=False
            except:
                pass
            ## Based on the above logic, generate strings to be used while creating the hotkeys.    
            if isAltPressed == True:
                AltPressedString = " Alt + "
            else:
                AltPressedString = " "        
            if isCtlPressed == True:
                CtlPressedString = " Ctrl + "
            else:
                CtlPressedString = " "
        
            ## Create a printout of the command being made and the hotkey that will use it.
            print(  "About to add nameCommand named "\
                + i['name'] + "         Pushing: " + CtlPressedString + AltPressedString + i['key']  )
            try:
                cmds.nameCommand( i['name'], annotation=i['annotation'], command=i['mel'] )
            except:
                print( "Error Creating Named Command" )
            ## Add the actual hotkey to Maya.
            try:                    
                cmds.hotkey( k=i['key'], name=i['name'], ctl=isCtlPressed, alt=isAltPressed)
            except:
                print( "Error Binding Hotkey" )
                    

    def applyHotkeysRelease(self):        
        """
        Applies release hotkeys in the situations that require it.
        """
        for i in self.namedCommandsRelease:
        
            ## Determine which modifiers are being used. (Because Maya is already naturally
            ## sensitive to shift, by using capitals or symbols, we don't test for shift.
            ## ****This and the part right below are duplicated code! 
            ## Find a good way to get rid of duplication.
            try:
                try:
                    isCtlPressed=i['ctl']
                except:
                    isCtlPressed=False
                try:
                    isAltPressed=i['alt']
                except:
                    isAltPressed=False
            except:
                pass
            
            ## Based on the above logic, generate strings to be used while creating the hotkeys.                
            if isAltPressed == True:
                AltPressedString = " Alt + "
            else:
                AltPressedString = " "        
            if isCtlPressed == True:
                CtlPressedString = " Ctrl + "
            else:
                CtlPressedString = " "

            ## Create a printout of the command being made and the hotkey that will use it.
            print(  "About to add nameCommandRelease named " + i['name'] + "         Releasing: " + CtlPressedString + AltPressedString + CtlPressedString + AltPressedString + i['key']  )
            try:
                cmds.nameCommand( i['name']+"Release", annotation=i['annotation']+"Release", command=i['mel'] )
            except:
                print( "Error Creating Named Command" )

            ## Add the actual hotkey to Maya.                
            try:
                ##Its very important that Release is added to name string below.
                cmds.hotkey( k=i['key'], ctl=isCtlPressed, alt=isAltPressed ,releaseName=i['name']+"Release" )
            except:
                print( "Error Binding Hotkey" )


        
    def setHotkeysToDefaults(self):
        cmds.hotkey(factorySettings=True)
        self.namedCommands = []
        self.namedCommandsRelease = []
        self.hotkeysAsDefaults()
        self.applyHotkeys()
        self.applyUserHotkeys()
        
    def setHotkeysToDefaultsNoUserHotkeys(self):
        cmds.hotkey(factorySettings=True)
        try:
            cmds.hotkeySet( "Maya_Default", current=True )
        except:
            print( traceback.format_exc() )
        self.applyHotkeysRelease()  #might need to run before the Press command        
        #self.namedCommands = []
        #self.namedCommandsRelease = []
        #self.hotkeysAsDefaults()
        #self.applyHotkeys()        

    def setHotkeysToPolygons(self):
        self.namedCommands = []
        self.hotkeysAsDefaults()
        self.hotkeysAsPolygons()
        self.applyHotkeys()

    def setHotkeysToUvs(self):
        self.namedCommands = []
        self.hotkeysAsDefaults()
        self.hotkeysAsUvs()
        self.applyHotkeys()
        

    def setHotkeysToRendering(self):
        self.namedCommands = []
        self.hotkeysAsDefaults()
        self.hotkeysAsRendering()
        self.applyHotkeys()
        

    #All the customizing parts are below here, so that its all kept together and easier to edit for the user.
        
    def hotkeysAsDefaults(self):
        """
        Define the set of default hotkeys.  These hotkeys are actually used in the other sets as well.
        """
        
        #Home, End,  9, semicolon are free by default
        #Pageup, PageDown are good to use in this mode too
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmHotstrings'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '\\'
        nameCommand['ctl'] = True        
        nameCommand['mel'] = """
                            python(  "mmmmTools.hotstrings.go()"  );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate       

        
        #Home, End,  9, semicolon are free by default
        #Pageup, PageDown are good to use in this mode too
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmHotMel'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '\\'
        nameCommand['alt'] = True        
        nameCommand['mel'] = """
                            python(  "mmmmTools.hotstrings.userStrToAction()"  );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmWireFrameOnShadedToggle'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '$'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            {string $curPanel; $curPanel = `getPanel -withFocus`; int $x=`modelEditor -q -wos $curPanel`; $x = ($x*-1)+1; setWireframeOnShadedOption $x $curPanel;}
                            //python(  "mmmmTools.u.toggleWireFrameOnShaded()"  );
                            """
        self.namedCommands.append(nameCommand)
              
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmOrthographicToggle'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '@'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """python(  "mmmmTools.u.camOrthoToggle()"  );"""
        self.namedCommands.append(nameCommand)         
        
     
        
    
    
    def hotkeysAsPolygons(self):
                            
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmDuplicateFace'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'd'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            DuplicateFace;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    

    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSlide'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'h'
        nameCommand['mel'] = """
                            SlideEdgeTool;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
    
    
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmEditEdgeFlow'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['alt'] = True        
        nameCommand['mel'] = """
                            polyEditEdgeFlow -constructionHistory 1 -adjustEdgeFlow 1;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmInstanceMirror'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'i'
        nameCommand['mel'] = """
                            instance; scale -1 1 1;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        ################
        ####   Important!  This needs a release, since J release defaults to scale snap.
        ## Press   - just j
        nameCommand = {}
        nameCommand['name'] = 'mmmmConnectComponents'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            ConnectComponents;
                            // qnexOpt -e manipType connect;
                            //// used to be: 
                            """
        self.namedCommands.append(nameCommand)
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-j'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False        
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate        
        
        
        
        
        #################
        ####   Important!  This needs a release, since J release defaults to scale snap.
        ## Press   - ctrl j
        nameCommand = {}
        nameCommand['name'] = 'mmmmConnectWithModelingToolkit'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            nexOpt -e manipType connect;
                            """
        self.namedCommands.append(nameCommand)
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-j'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False        
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate
    
    
    
    
    
    
    
    
    
    
    
        #################
        ####   Important!  This needs a release, since J release defaults to scale snap.
        ## Press    - shit j
        nameCommand = {}
        nameCommand['name'] = 'mmmmInsertEdgeLoopTool'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'J'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        
        nameCommand['mel'] = """
                            SplitEdgeRingTool;
                            """
        self.namedCommands.append(nameCommand)
        
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-j'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'J'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False        
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate


        
        
        #################
        ####   Important!  This needs a release, since J release defaults to scale snap.
        ## Press      -  ctrl shift   j
        nameCommand = {}
        nameCommand['name'] = 'mmmmConnectWithOMT'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'J'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            OMT_to_connectComponents();
                            """
        self.namedCommands.append(nameCommand)
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-J'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'J'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate
        

        #################
        ####   Important!  This needs a release, since J release defaults to scale snap.
        ## Press        -  alt  j
        nameCommand = {}
        nameCommand['name'] = 'mmmmConnectAndSelectEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            polySplitRing -ch on -splitType 1 -weight 0.5 -smoothingAngle 180;
                            ////  need to implement mmmmConnectAndSelectEdges
                            """
        self.namedCommands.append(nameCommand)
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-Alt-j'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True        
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate        




        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectSelectionBorderEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'K'
        nameCommand['mel'] = """
                            select -r `polyListComponentConversion -ff -te -bo`;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeRing'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'k'
        nameCommand['mel'] = """
                            SelectEdgeRing;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate       
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeRingAlt'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'k'
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            SelectEdgeRing;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate       


        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeLoop'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'l'
        nameCommand['mel'] = """
                            SelectEdgeLoop;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmVolumeSelectVerts'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'L'
        nameCommand['mel'] = """
                            python( "mmmmTools.selector.volumeSelect()" );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmVolumeSelectFaces'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'l'
        nameCommand['ctl'] = True        
        nameCommand['mel'] = """
                            python( "mmmmTools.selector.volumeSelect(faces=True)" );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmExtrude'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['mel'] = """
                            PolyExtrude;
                            """
        self.namedCommands.append(nameCommand)
        ## Release
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingPolygons-m'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate            


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCollapse'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'n'
        nameCommand['mel'] = """
                            polyCollapseEdge;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmFillHole'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'O'  # didn't use unmodified one because it is a useful marking menu
        nameCommand['mel'] = """
                            FillHole;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRetoperProject'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'o'  # didn't use unmodified one because it is a useful marking menu
        nameCommand['alt'] = True
        nameCommand['mel'] = """
            python( "MmmmTools.Modeler.ModelerRetoper.ModelerRetoper.getInstance().projectSelection()" );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRetoperSetReference'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'O'  # didn't use unmodified one because it is a useful marking menu
        nameCommand['alt'] = True
        nameCommand['mel'] = """
            python( "MmmmTools.Modeler.ModelerRetoper.ModelerRetoper.getInstance().setReference()" );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        #MmmmTools.Modeler.ModelerRetoper.ModelerRetoper.getInstance().makeLive()
        #MmmmTools.Modeler.ModelerRetoper.ModelerRetoper.getInstance().makeNotLive()


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCenterPivot'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'p'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True        
        nameCommand['mel'] = """
                            CenterPivot;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmQuadDraw'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'p'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False        
        if self.getMayaVersionAsFloat() >= 2016.0:
            nameCommand['mel'] = """
                                dR_quadDrawTool;
                                """
        else:
            nameCommand['mel'] = """
                                nexOpt -e manipType quadraw;
                                """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmTriangulate'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 't'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True        
        nameCommand['mel'] = """
                            Triangulate;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate        

        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSculptGeometryTool'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'U' # regular u is the sculpt marking menu
        nameCommand['mel'] = """
                            SculptGeometryTool;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmLocalTools'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '8'
        nameCommand['mel'] = """
                            catchQuiet(  HKLTOptionBox()  );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmHKLocalToolsTakeReference'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '9'
        nameCommand['mel'] = """
                            HKLocalToolsAction();
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmExtract'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ')'
        nameCommand['mel'] = """
                            ExtractFace;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCombine'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '0'
        nameCommand['mel'] = """
                            CombinePolygons;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmDeleteEdgeAndVertex'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '='
        nameCommand['mel'] = """
                            performPolyDeleteElements;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
    
    
        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmHarden'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ';'
        nameCommand['mel'] = """
                            SoftPolyEdgeElements 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmUncreaseAndSoften'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '"'
        nameCommand['mel'] = """
                            python( "mmmmTools.modeler.uncreaseSelectedEdges()" );
                            SoftPolyEdgeElements 1;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
        #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCreaseAndHarden'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ':'
        nameCommand['mel'] = """
                            python( "mmmmTools.modeler.creaseSelectedEdges()" );
                            SoftPolyEdgeElements 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSoften'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "'"
        nameCommand['mel'] = """
                            SoftPolyEdgeElements 1;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmBevel'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ','
        nameCommand['mel'] = """
                            BevelPolygon;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmBridgeEdge'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ','
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        if self.getMayaVersionAsFloat() >= 2016.0:
            nameCommand['mel'] = """
                                BridgeEdge;
                                """
        else:
            nameCommand['mel'] = """
                                nexOpt -e manipType bridge;
                                """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmBridgeEdgeOld'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ','
        nameCommand['ctl'] = True
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            BridgeEdge;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#      just  .   
        nameCommand = {}
        nameCommand['name'] = 'mmmmMergeToCenter'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            polyMergeToCenter;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#     ctrl  alt  .
        nameCommand = {}
        nameCommand['name'] = 'mmmmMergeWithOptions'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = True
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            PolyMergeOptions;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#  alt  .
        nameCommand = {}
        nameCommand['name'] = 'mmmmMergeTouchingVertsAndEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            {    
                                //// Merge touching edges and verts
                                string $sel[] = `ls -selection`;
                                polyMergeVertex  -d 1e-06 -am 0 -ch 1;
                                select $sel;
                                polySewEdge -t 1e-06 -tx 0 -ws 1 -ch 1;
                                select $sel;
                            }
                            
                            //// PolyMerge;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#          ctrl .
        nameCommand = {}
        nameCommand['name'] = 'mmmmTargetWeld'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            //// Target weld from modeling tooklit
                            nexOpt -e manipType weld;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        

        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmMultiCut'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'
        if self.getMayaVersionAsFloat() >= 2016.0:        
            nameCommand['mel'] = """
                                dR_multiCutTool;
                                """ 
                            
        else:
            nameCommand['mel'] = """
                            //// MultiCut Tool (a sub tool of the modeling toolkit toolsqqQQqqqQ
                            nexOpt -e manipType cut;
                            
                            //this hotkey used to use SplitPolygonTool;
                            """                
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSplitPolyAtEdgesOnly'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '?'
        nameCommand['mel'] = """
                            polySplitCtx -e -ste true  polySplitContext;
                            SplitPolygonTool;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSplitPolyNotAtEdgesOnly'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'        
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            polySplitCtx -e -ste false  polySplitContext;
                            SplitPolygonTool;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmToggleGrid3dViewPolys'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'G'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            ToggleGrid;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate 
        
        
        
         
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmGridGrow'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ']'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
            python(  "MmmmTools.Modeler.ModelerGridTools.ModelerGridTools.grow(log=True, setManip=True)"  );
                            """
                            
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
         
         
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmGridShrink'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '['
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                python(  "MmmmTools.Modeler.ModelerGridTools.ModelerGridTools.shrink(log=True, setManip=True)"  );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate 
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmGridSnapSelectedVerts'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '['
        nameCommand['ctl'] = False
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                python(  "MmmmTools.Modeler.ModelerGridTools.ModelerGridTools.snapVertsToGrid()"  );
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def hotkeysAsUvs(self):
        #Home, End,  9, semicolon are free
        #Pageup, PageDown are good to use in this mode too
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmPlanarProjection'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyProjectionArgList "1" {"0", "Planar", "ls -selection", "0"} "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCylindricalProjection'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ','
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyProjectionArgList "1" {"1", "Cylindrical", "ls -selection", "0"} "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSphericalProjection'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyProjectionArgList "1" {"1", "Spherical", "ls -selection", "0"} "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
            
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmAutomaticProjection'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyAutoProj 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmShowTextureBorderEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ';'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            setPolygonDisplaySettings("textBorderEdge");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCutUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            polyPerformAction polyMapCut e 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmReloadTextures'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '9'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            python("mmmmTools.fileTextureReloader.reload()");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmLayoutUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '8'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            polyLayoutUV -lm 1 -sc 1 -se 2 -rbf 1 -fr 0 -ps 0.2 -l 2 -ch 1;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmMoveAndSewUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'h'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyMapSewMove 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSewUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'n'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            polyPerformAction polyMapSew e 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate      
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmToggleGrid3dViewUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'G'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            ToggleGrid;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmUnfoldUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'u'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performUnfold 0;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectSelectionBorderEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'K'
        nameCommand['mel'] = """
                            select -r `polyListComponentConversion -ff -te -bo`;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate    
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeRing'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'k'
        nameCommand['mel'] = """
                            SelectEdgeRing;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeRingAlt'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'k'
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            SelectEdgeRing;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate

        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectEdgeLoop'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'l'
        nameCommand['mel'] = """
                            SelectEdgeLoop;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmTextureWindow'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '0'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            TextureViewWindow;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectAndConvertToUvs'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 's'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            ConvertSelectionToUVs;
                            changeSelectMode -component; selectType -alc false; selectType -puv true; selectType -smu true; selectType -suv true;
                            updateObjectSelectionMasks;
                            updateComponentSelectionMasks;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectAndConvertToUvsShell'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'S'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            ConvertSelectionToUVs;
                            SelectUVShell;
                            changeSelectMode -component; selectType -alc false; selectType -puv true; selectType -smu true; selectType -suv true;
                            updateObjectSelectionMasks;
                            updateComponentSelectionMasks;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate        
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmSelectTextureBorderEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '?'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            python("mmmmTools.selectTextureBorderEdges.selectTextureBorderEdges();")
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRoadKill'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            MmmmToolsRoadKill;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmToggleTextureBorderEdges'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '^'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            python("mmmmTools.texturer.toggleSeams()");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmDoNothingUvs-j'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'j'
        nameCommand['mel'] = """
                            //
                            """
        self.namedCommandsRelease.append(nameCommand)
        #End of section to duplicate
        
        

    def hotkeysAsSurfaces(self):
        #Home, End,  9, semicolon are free
        #Pageup, PageDown are good to use in this mode too
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmPlanarProjection'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            performPolyProjectionArgList "1" {"0", "Planar", "ls -selection", "0"} "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate


        
    def hotkeysAsRendering(self):
        #Home, End,  9, semicolon are free
        #Pageup, PageDown are good to use in this mode too
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmShowHypershadeWindow'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            HypershadeWindow;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCreateAndAssignBlinn'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '0'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            createAndAssignShader blinn "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmCreateAndAssignBlinn2'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'n'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            createAndAssignShader blinn "";
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmGraphMaterialsOnSelectedObjects'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ','
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "graphMaterials");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmAddSelectedToGraph'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "addSelected");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRemoveSelectedFromGraph'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '.'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "removeSelected");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRearrangeGraph'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = 'm'
        nameCommand['ctl'] = False
        nameCommand['alt'] = True
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "rearrangeGraph");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmShowUpAndDownstream'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
    
    
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmShowUpstream'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = '/'
        nameCommand['ctl'] = True
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "showUpstream");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmShowDownstream'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "?"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            hyperShadePanelGraphCommand("hyperShadePanel1", "showDownstream");
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmToggleClearBeforeGraphing'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = ";"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                            optionVar -intValue hsClearBeforeGraphing `menuItem -query -checkBox hyperShadePanel1Window|TearOffPane|hyperShadePanel1|hyperShadePanelMenuOptionsMenu|clearBeforeItem`;

                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmMakeLightLinks'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "h"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                                lightlink -make -useActiveLights -useActiveObjects;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmBreakLightLinks'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "j"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
        lightlink -break -useActiveLights -useActiveObjects;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmIPR'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "i"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                                RenderViewWindow;
                                catchQuiet( `renderWindowMenuCommand keepImageInRenderView renderView` );
                                IPRRenderIntoNewWindow;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmRender'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "9"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                                RenderViewWindow;
                                catchQuiet( `renderWindowMenuCommand keepImageInRenderView renderView` );
                                RenderIntoNewWindow;
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate
        
        
        #This section is meant to be duplicated and altered #
        #Edit the name, key and mel parts#
        nameCommand = {}
        nameCommand['name'] = 'mmmmGetSelectionByMaterial'
        nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
        nameCommand['key'] = "'"
        nameCommand['ctl'] = False
        nameCommand['alt'] = False
        nameCommand['mel'] = """
                                hyperShade -objects `ls -sl`; 
                            """
        self.namedCommands.append(nameCommand)
        #End of section to duplicate