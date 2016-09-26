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
Hotstrings module.

This is a module that accepts very short commands, and which then
runs various Maya and MmmmTools commands upon reveiving a short command

eg command: l
lower case L, could trigger then maya command to create a light

eg command: c
Can trigger the creation of a cube by running the polyCube command.

Basically, hotstrings is just a way to stack *way* more hotkeys onto the
keyboard.  A lot of short hotstrings can be entered faster than the user
could click on the equivilant commands in the menus.
"""
            ##   OLD OUTDATED COMMENTS, CAN SOON BE REMOVED
            ## Joe Crawford's Hotstring Script
            ## (Joe can be found at http://www.celestinestudios.com)
            ## run this and then use a hotkey
            ## (probably backslash because its right by enter) to run:
            ##                 python(  "app = Hotstrings()" );

#import maya
#import maya.cmds as cmds
import pymel.all as pm

import maya.OpenMaya as OpenMaya

from Utils import Utils


u = Utils


## Try to load the Hotstring actions from another file.
## try backup on failure, and make default simple
## action if backup file fails.
try:
    import HotstringsActions
    reload( HotstringsActions )
    import HotstringsActions
except:
    u.log( "HotstringsActions file could not be loaded.  "
            "Most like because of an error in the file.  "
            "Loading backup instead."
          )
    try:
        import BackupHotstringsActions as HotstringsActions
    except:
        u.log( "Backup of HotstringsActions could "
               "not be loaded. No actions will be "
               "available for Hotstrings."
             )
        HotstringsActions = object()
        HotstringsActions.actions = {'default':"""   print "No actions are available";  """}

        

class HotstringsUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.ini = parent.ini
        
        self.test = "default"
        self.result = "none"
        self.windowName = "Hotstrings For Maya"
        
        
    def getUserInput(self):
        self.result = pm.promptDialog(
            title=self.windowName,
            message='Enter Hotstring:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='')

        self.parent.text = 'help'
            
        if self.result == 'OK':
            self.parent.text = pm.promptDialog(query=True, text=True)

        self.parent.doAction()        
        

class Hotstrings(object):

    #add extra variables here


        
    def __init__(self, parent, make_ui=True):
        self.parent = parent
        self.mmmmTools = self.parent
        self.ini = parent.ini
        self.loadActions()
        
        self.text = 'help'
        
        self.rtcmds =  pm.mel.eval("runTimeCommand -q -ca;")
        if make_ui:
            self.ui = HotstringsUi(self)
            
    
    def go(self):
        self.ui.getUserInput()
            
            
    def doAction(self, cmd=None):        
        ## If a spefic command was given use it, otherwise, use self.text to
        ##  get the action.
        if not cmd is None:
            self.text=cmd

            
        ## Run scripts using special logic if run is used
        if self.text.startswith('run '):
            scriptNameToRun = str(self.text)[4:]
            self.mmmmTools.scripter.runScripterScript( scriptNameToRun )
            return
            
        ## Make sure its possible to get from the dictionary,
        ## otherwise make the command None
        try:
            command = self.actions[self.text]
        except:
            command = False
        
        ## Determine the type of command, and if it is a string, try to run it.
        ## show errors if it can't be run.
        if command is None:
            u.log("Please Type a command in the window. Example:  c   ")
        else:
            if isinstance(command, str) or isinstance(command, unicode):
                if isinstance(command, unicode):
                    command = str(command)
                ## The next commented lines are placeholders for
                ## functionality to run specific hardcoded functions
                ## or commands
                #if self.text == 'hard coded command example fdsaf':
                #    print("Hardcoded command run")
                ## The if False is here as a placeholder also.
                if False:
                    pass
                elif self.text == "":
                    u.log("Please Type a command in the window. Example:  c  ")
                else:
                    try:
                        pm.mel.eval(command)
                    except:
                        u.log( "Hotstring command could not be evaluated." )
            else:
                u.log( "Hotstring command was not a string, so it could not "
                       "be evaluated." )

    
    def help(self):
        u.log("\nAvailable Hotstrings Commands:  \n")
        self.printActions()
        u.log("A list of hotstrings commands is shown above.")
        u.log("To use hotstrings, type the backslash key,")
        u.log("then type a command in the hotstrings window and press enter.")
        u.log("For example, push backslash, then in the window")
        u.log("that appears type:    c      and then press enter \n")
    
    def printActions(self):
        keys = self.actions.keys()
        for k in keys:
            u.log( "\n\n\n Command:  " + k )
            u.log(self.actions[k])
        u.log("\n")
            
    def loadActions(self):
        self.actions = HotstringsActions.actions

    def userStrToAction(self, commandsFromLast=None, textFromLast=""):
        rtcmds =  self.rtcmds   ## pm.mel.eval("runTimeCommand -q -ca;")
        
        cmdsStartingWith = []
        cmdsContaining = []
        
        
        if commandsFromLast is not None:
            commandsStr = 'Commands similar were found, but you must be more specific, or end your command with a space to force a "best guess".\n\n '
            for commandFromLast in commandsFromLast:
                commandsStr += commandFromLast + "   "
                
            messageStr = commandsStr  
                
        else:
            messageStr = ' Enter HotMel "search" command.\n\n HotMel commands are made automatically for most of the menu items in Maya, and often match the name. You can try typing in words to search for here. If several matches are found, they will be shown.\n\n End the command with spacebar to force best guess.\n End the command with a semicolon to run as Mel code.\n Use "runTimeCommand -q -ca;" to print a list of all available commands in the script editor.\n\n Press Enter To Execute'
                
            
        
        
        
        promptWin = pm.promptDialog(
            title="HotMel",
            message=messageStr,
            text=textFromLast,
            button=['OK'],
            defaultButton='OK',
            dismissString='')
        try:
            userStr = pm.promptDialog(query=True, text=True)
        except:
            print( "Error getting value from prompt dialog." )
            return
        
        searchStr = userStr.replace( " ", "" )
        
        for cmdStr in rtcmds:
            if cmdStr.startswith(searchStr):
                cmdsStartingWith.append( cmdStr )
            elif searchStr in cmdStr:
                cmdsContaining.append( cmdStr )
                
        
        cmdsStartingWith.sort()
        cmdsContaining.sort()
        
        cmdsFound = cmdsStartingWith + cmdsContaining
        
        
        
        
        ## If nothing entered, bail
        if userStr == "":
            tmp=0  ## do nothing here
            
        ## If we have an exact match, run it    
        elif userStr in cmdsFound:
            pm.mel.eval( searchStr )
        
        ## If it ends in a semicolon, then run it as a mel command
        elif userStr.endswith( ";" ):
            pm.mel.eval( searchStr )
        
        ## If it ends in a space, then run the first thing we find that start
        elif userStr.endswith( " " ):
            print userStr[:-1]
            spaceCmdFound = False
            for cmdToTest in cmdsFound:
                print "command: " + cmdToTest
                if cmdToTest.startswith( userStr[:-1] ):
                    print( cmdToTest )
                    pm.mel.eval( cmdToTest )
                    spaceCmdFound = True
                    break  ## We only want to run one command!
            if spaceCmdFound==False:
                for cmdToTest in cmdsFound:
                    if userStr[:-1] in cmdToTest:
                        print( cmdToTest )
                        pm.mel.eval( cmdToTest )
                        spaceCmdFound = True
                        break
                        
                    
        ## If there's only one command that matches, then run it         
        elif len(cmdsFound)==1:
            pm.mel.eval( cmdsFound[0] )
        
        
        ##  If none of these thngs are found, then run another thing entirely    
        else:
            defaultWasFound=False
            
            if len(cmdsFound)==2:
                if cmdsFound[1].endswith( "Options" ):
                    defaultWasFound=True
                    pm.mel.eval( cmdsFound[0] )
                
            if defaultWasFound==False:
                print(  cmdsFound )
                tmp = ""
                for cmd in cmdsFound[:4]:
                    tmp = tmp + " " + cmd
                OpenMaya.MGlobal.displayInfo( "Suggestions: " + tmp )
                self.userStrToAction( commandsFromLast=cmdsFound, textFromLast=userStr)
        
### End of Hotstrings Class ###    

