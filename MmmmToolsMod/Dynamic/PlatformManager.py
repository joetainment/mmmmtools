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
MmmmTools module to provide infomation on computer arch,
operating system, etc. Also provides classes to MmmmTools
for path management and manipulation.

Only limited information about Maya is computed/found here.
Just enough to make some basic paths etc
    
For extended Maya information, see the Env module.
"""    


import pymel.all as pm
import maya.cmds as cmds

import platform
import sys
import os
import shutil
import cPickleimport UtilsMod

## Setup shortcutsUtils = UtilsMod.UtilsPather = UtilsMod.PatherDuck = UtilsMod.Duck
u = Utils

class PlatformManager(object):
    """
    MmmmTools class/interface to information about the platform it's running on.
    """
    def __init__(self, parent):
        u.log( "PlatformManager: running inside self __init__ function.")
        self.parent = parent
        
        ## Set up very basic objects to store data in.
        self.info = Duck()
        self.info.arch = Duck()
        self.info.os = Duck()
        self.info.python = Duck()
        self.info.maya = Duck()
        self.info.mmmm = Duck()
        
        self.initInfoArch()
        self.initInfoOs()
        self.initInfoPython()
        self.initInfoMaya()
        self.initInfoMmmm()
        
        
    def initInfoArch(self):
        self.info.arch.machineType = platform.machine()
        self.info.arch.networkName = platform.node()
        self.info.arch.processorType = platform.processor()
        
    def initInfoPython(self):    
        self.info.python.buildNumber, self.info.python.buildDate = platform.python_build()
        self.info.python.compiler = platform.python_compiler()
        self.info.python.branch = platform.python_branch()
        self.info.python.implementation = platform.python_implementation()
        self.info.python.revision = platform.python_revision()
        self.info.python.version = platform.python_version()
        tmp = platform.python_version_tuple()
        self.info.python.versionTuple = tmp
        major,minor,patch = tmp
        self.info.python.versionMajor = major
        self.info.python.versionMinor = minor
        self.info.python.versionPatch = patch
        
    def initInfoOs(self):
        pass
        
    def initInfoMaya(self):
        tmp = self.getMayaPath().makeAbsolute()
        self.info.maya.maya_app_dir_with_version_pather = tmp
        self.info.maya.maya_app_dir_with_version_str = tmp.st
        self.info.maya.maya_app_dir_with_version_scripts_pather = tmp2 = tmp + 'scripts'
        self.info.maya.maya_app_dir_with_version_scripts_str = tmp2.st
        
        self.info.maya.maya_app_dir_with_version_prefs_pather = \
            self.info.maya.maya_app_dir_with_version_pather + \
            'prefs'
        
        self.info.maya.gMainWindowStr = pm.mel.eval (
            'global string $gMainWindow; string $temp=$gMainWindow;')
        
        t = self.info.maya.maya_bin_paths_str = pm.mel.eval('getenv "PATH";')
        
        u.log( 'Result of Maya, getenv:' )
        u.log( t )
        

    def initInfoMmmm(self):
        m = self.info.mmmm.mmmm_pather = \
            (          
                self.info.maya.maya_app_dir_with_version_scripts_pather +
                'MmmmToolsMod'
            )
        self.info.mmmm_path_str = m.st
        self.info.mmmm_path = m

    def getFullInfoString(self, repr=False):
        st = ""
        for k,v in self.info.__dict__.items():
            #u.log("Platform Manager Info Dictionary: " + str(k) )
            try:
                dict = v.__dict__
            except:
                dict = {}
            
            ## sr will be used to convert to strings
            if repr:
                sr = self.strOrRepr
                    ## works like the repr
                    ## function but won't change existing str's
            else:
                sr = str
            
            for kk,vv in dict.items():
                typeInfo = "          ::" + str(type(vv))
                text = "PlatformManager info: " + sr(k) + "   :: " + sr(kk) + " : " + sr(vv) + typeInfo
                u.log( text )
        if not sr is str:
            print( "Note that for any non string values, info string are generated using their python repr functions." )
        return text
        
    def strOrRepr(self, v):
        if not isinstance(v,str):
            v = repr(v)
        return v
        
                
    def getMayaPath(self):
        return u.getMayaPath()