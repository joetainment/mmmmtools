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
Env module for MmmmTools. This class exists mainly to help provide information
to maya and the mmmmTools.platformManager object. This class calculates paths
to several items specified in the Configuration.py module, and also add those
paths to maya as mel variables and as environment variables.

Overall, this class helps to allow MmmmTools to run other scripts and other
binaries which wouldn't normally be searched for and found by Maya.
"""

import sys
import os
import shutil

import maya.cmds as cmds
import maya.mel
import pymel.all as pm

#import EnvPopularScriptsAutoSourceimport UtilsMod
#reload(EnvPopularScriptsAutoSource) ## inefficient but it's fast enough
u = Utils = UtilsMod.UtilsPather = UtilsMod.Pather
class Env(object):
    """
    Env class for MmmmTools
    
    Very specific class to use in composing the main MmmmTools class, useless
    as a general purpose class.
    
    ****
    Some functionality does exist in here that should be moved into
    the more general purpose Utils class. In particular the sections for
    adding environment variables, changing system binary path. Such sections
    can and should be changed into more abstract general purpose utils.
    
    """
    def __init__(self, parent ):
        ##Init reference to parent and to configuration
        self.parent = parent
        self.mmmm = self.parent
        self.pman = self.mmmm.platformManager
        self.ini = self.parent.ini
        self.conf = self.ini.conf

        ##set variables to known values
        
        self.setupSystemPaths()
        #self.setupRoadkill()  ## roadkill removed from modern mmmmtools versions
        self.setupScriptPaths()
        
        ## Source popular scripts (list is defined in Configuration module)
        #EnvPopularScriptsAutoSource.main( self )
        
        self.makeAutoHotkeyPath()

    
    def setupSystemPaths(self):
        pass ## not currently needed, but future versions of MmmmTools
             ## will likely do stuff here
        
    # def setupRoadkill(self):
        # self.roadkillAddPathToMayaBinSearchPaths()
        # self.roadkillAddPathToMelGlobalsAndPutEnv()
    
    # def roadkillAddPathToMelGlobalsAndPutEnv(self):
        # """
        # Add maya variables for the path to roadkill, by using: pm.mel.eval()
        # """
        # ps = self.pman.info.mmmm.roadkill_pather.st
        # ps = ps.replace('\\','\\\\')
                # ## Double up the slashes since mel interprets
                # ## them as escapes are we're making a string of mel code
        # pm.mel.eval( 'putenv "roadkill_path_absolute" ' + '"' + ps + '"' + ';' )
        # pm.mel.eval( 'global string $gRoadKillPath = "' + ps +  '";')
            
    # def roadkillAddPathToMayaBinSearchPaths(self):
        # """
        # Add roadkill path to maya's path where it tries to run bins from.
        # """
        
        # ## Get maya's binary search path (where it looks for executables)
        # env_paths = self.pman.info.maya.maya_bin_paths_str
        
        # ## Build a pather for the roadkill folder where roadkill exe is
        # roadkill_pather = self.pman.info.mmmm.roadkill_pather = (
            # self.pman.info.mmmm.mmmm_pather +
            # self.conf.roadkill_dir
            # )
        
        # ## Make combine the existing search paths with the new one 
        # ## a simple replace is used to remove double semicolons
        # ## since we don't know where semicolons might already be
        # new_env_paths = \
            # (env_paths + ";" + roadkill_pather.st).replace(';;',';')
        # ## No matter what platform we are on, we don't want backslashes in
        # ## the name new_env_path that maya will have.
        # ## (Maya when queried, gives slashes on all platforms.
        # new_env_paths_slashes = new_env_paths.replace('\\','/')
        # ## Puth the new paths into maya
        # pm.mel.eval( 'putenv "PATH" ' + '"' +
                        # new_env_paths_slashes +
                        # '"' + ';'
                    # )
        # ## Remember that this paths string is in maya form, not windows form
        # ## it has slashes, not backslashes
        # self.pman.info.maya.maya_bin_paths_str = new_env_paths_slashes
        
        
    def setupScriptPaths(self):
        ## Make shortcuts for thing buried in self, to avoid digging 
        ini = self.mmmm.ini
        conf = self.mmmm.ini.conf
        pman = self.pman
        info = pman.info
        immmm = info.mmmm
        
        ## Get maya's script paths, (where it looks for mel scripts)
        paths_str = pm.mel.eval('getenv "MAYA_SCRIPT_PATH";')
        
        ## Get path strings from ini (Configuration)
        subscripts_str = ini.conf.subscripts_str
        subscripts_downloaded_str = conf.subscriptsDownloaded_str
        autoscripts_str = conf.autoscripts_str
        
        ## Build Pathers From String
        ##      The paths below are made and kept as pathers, not strings!
        p_mmmm = immmm.mmmm_pather  ## supposed to already be absolute
        p_maya_scripts = info.maya.maya_app_dir_with_version_scripts_pather
        p_subscripts = p_mmmm + subscripts_str
        p_subscripts_downloaded = p_mmmm + subscripts_downloaded_str
        p_autoscripts = p_maya_scripts + autoscripts_str
        
        ## Make lists that we will fill up in the for loops
        ##      these lists will hold our new paths to add
        ##      both as pathers and as strings
        mList = [ ]
        mListStr = (
            paths_str + ';' +
            p_mmmm.st + ';' +
            p_subscripts.st + ';'  +
            p_subscripts_downloaded.st + ';' +
            p_autoscripts.st + ';'
            )
        
        ## Make a list of pathers that we want to add to the scripts path
        dList = [ p_subscripts, p_subscripts_downloaded, p_autoscripts  ]
        
        ## Loop through list of pathers in order to find the subfolders
        ##      inside of each pather's dir
        ##      then add the subfolders to the lists which will be added
        ##      to the script paths.
        for dir in dList:
            try:
                iter = os.listdir( dir.st )
            except:
                iter = []
                u.log( "Unable to list contents of folder. Perhaps it "
                       "does not exist. Folder was: " + dir.st )
                
            for f in iter:
                #make a full path name for each file name str f
                ff = dir + f
                
                if os.path.isdir( ff.st ):
                    mList.append(ff)
                    mListStr = mListStr + ff.st + ';'
        
        ## **** Consider adding code here to loop through each immediate
        ##  subfolder of the subscripts path, and consider writing something
        ##  to loop through each of their user setups
        mListStrSlashes = mListStr.replace('\\','/')
        pm.mel.eval( 'putenv "MAYA_SCRIPT_PATH" ' + '"' + mListStrSlashes + '"' + ';')
        
        ## We need to rehash the script path, otherwise mel won't find the
        ##  newly added paths
        pm.mel.eval('rehash;')
        
        ## Run the user setup files from all the folder in mList, which
        ##      should be the subscripts and autoscripts
        for d in mList:
            p_userSetup = d + conf.userSetup_str
            if os.path.isfile(p_userSetup.st):
                try:
                    pm.mel.eval( 'source "' + userSetupFile.st + '"' + ';' )
                except:
                    pass
        
        ## Place information about paths found into platformManager
        immmm.subscripts_pather = \
            immmm.mmmm_pather + subscripts_str
        immmm.subscripts_downloaded_pather = \
            immmm.mmmm_pather + subscripts_downloaded_str
        immmm.autoscripts_downloaded_pather = \
            self.pman.info.maya.maya_app_dir_with_version_scripts_pather + \
            autoscripts_str

            
    def getMayaPath(self):
        appEnvFile = cmds.about(env=True)
        path, file = os.path.split(appEnvFile)
        return path

 
    def makeAutoHotkeyPath(self):
        try:
            self.makeAutoHotkeyPathStage2()
        except:
            u.log( "Could not set up paths for Autohotkey. "
                   "Proceeding without it."
                  )
    def makeAutoHotkeyPathStage2(self):
        """
        Sets up autohotkey.  This function uses windows specific things,
        but that's ok, because autohotkey only works on Windows anyway.
        """
    
        p = self.pman.info.mmmm.autohotkey_pather = \
            self.pman.info.mmmm.mmmm_pather + self.conf.autohotkey_folder
            
        #ps = p.st  ## get pather as string
        #pm.mel.eval( 'putenv "autohotkey_path_absolute" ' + '"' + ps + '"' + ';' )
        #pm.mel.eval( 'global string $gAutoHotkeyPath = "' + ps +  '";')
        
        exePather = p + self.conf.autohotkey_exe
        
        ahkPather = p + self.conf.autohotkey_script 
        
        q = '\\"'  #this is an escaped backslash
                    #  thus command will thus contail a backslash
                    #  before the quote, which will be escaped when
                    #  evaluated by mel
        
        c = 'system("start '
        c += q + exePather.st.replace('\\','\\\\') + q
        #c += ' '
        #c += q + ahkPather.st.replace('\\','\\\\') + q
        c += '");'
        
        #import subprocess
        cc = exePather.st + ' ' + '"' +ahkPather.st + '"'
        #subprocess.call( cc )
        #print( cc  )  ## print the command that would be called to start autohotkey
        self.conf.autohotkey_command = cc
        
        #try:
        #    pm.mel.eval( 'putenv "autohotkey_command" ' + '"' + ps + '/' + self.conf.autohotkey_exe + '"' + ';' )
        #except:
        #    pass
           

pass