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
Configuration information for MmmmTools.
Contains functions for loading the data from the ini file,
as well as many 'hardcoded' variables written into
this python script.
Essentially, they are all kept in this module
so the configuration isn't spread out across many files.
This makes it easy to find and change such settings.
"""


##########################################
####   Imports 
###########################################

import maya.cmds as cmds
import maya.mel
import pymel.all as pm

import sys
import os
import shutil
import cPickle
from ConfigParser import ConfigParser

from Utils import Utils
from Utils import Pather
from Utils import Duck

################################
####  Classes
################################

class Conf(object):
    """
    These are static configuration values, used by many of the other modules.
    A lot of them are hard coded, but since it's just python script code
    it's easier to do this than read the data from another file type.
    They are put here so they are all in the same place.
    User text-editor editable values are stored elsewhere,
    in the ini file and its associated objects.
    """
    def __init__(self,parent):
        self.parent = parent
        self.mmmm = self.parent.mmmm
        self.pman = self.parent.pman
        
        self.hardcoded = Duck()
        self.calculated = Duck()
        
        self.initConfigHardcodedProperties()
        
    def initConfigHardcodedProperties(self):
        ## Everything in here should be a hardcoded property, in a basic python type
        ## (eg: str, int, float, list, dict)
        ## Nothing computed or dynamic!!!
        
        self.aboutString = "MmmmTools - Usability Improvements For Maya"
        self.autohotkey_folder = 'AutoHotkey'
        self.autohotkey_exe = 'AutoHotkey.exe'
        self.autohotkey_script = 'MmmmTools.ahk'
        
        self.roadkill_dir = "RoadKill"
        
        self.userSetup_str = 'userSetup.mel'
        self.subscripts_str = 'subscripts'
        self.subscriptsDownloaded_str = 'subscriptsDownloaded'
        self.autoscripts_str = 'autoscripts'

        #self.popular_script_goz_filename = 'GoZScript.mel'
        #self.popular_script_hklt_filename = 'HKLocalTools.mel'
        self.popular_script_filenames_list = [
                #self.popular_script_hklt_filename,
                #self.popular_script_goz_filename,
        ]
        
        # ##  HK Local Tools Configuration
        # self.downloader_hklocaltools_url = \
                    # "http://www.henrykorol.net/Scripts/LocalTools/HKLocalTools.zip"
        # self.downloader_hklocaltools_dest_zip_file = "HKLocalTools.zip"
        # self.downloader_hklocaltools_dest_dir = "HKLocalTools"
        # self.downloader_hklocaltools_file_to_extract = 'HKLocalTools/HKLocalTools.mel'
        # self.downloader_hklocaltools_dest_mel_file = 'HKLocalTools.mel'

        # ##  Ya Selection Manager Configuration
        # self.downloader_yaselectionmanager_url = \
                    # "http://celestinestudios.com/mmmmtools/subscripts/yaselectionmanager/ya_selectionManager.mel"
        # self.downloader_yaselectionmanager_name = "ya_selectionManager"
        # self.downloader_yaselectionmanager_dest = "YaSelectionManager"
        # self.downloader_yaselectionmanager_mel_dest_file = 'YaSelectionManager/ya_selectionManager.mel'


        # ##  FileTextureManager Configuration
        # self.downloader_filetexturemanager_url = \
                    # "http://celestinestudios.com/mmmmtools/subscripts/filetexturemanager/FileTextureManager.mel"
        # self.downloader_filetexturemanager_dest_dir = "FileTextureManager"
        # self.downloader_filetexturemanager_dest_zip_file = "FileTextureManager.zip"
        # self.downloader_filetexturemanager_file_to_extract = 'FileTextureManager/FileTextureManager.mel'
        # self.downloader_filetexturemanager_dest_mel_file = 'FileTextureManager.mel'


        # ##  KProgressiveRendering Configuration
        # self.downloader_kprogressiverendering_url = \
                    # "http://celestinestudios.com/mmmmtools/subscripts/kprogressiverendering/k_progressiveRendering.mel"
        # self.downloader_kprogressiverendering_dest_dir = "KProgressiveRendering"
        # self.downloader_kprogressiverendering_dest_mel_file = 'k_progressiveRendering.mel'
        
        ## Threading Configuration for multithreaded processes
        self.threads_run_at_start = 0
        
        self.texturer_show_seams_border_thickness = 3.5
        
        self.config_file_header_msg_to_user_string = """    
#  Note: DO NOT EDIT THIS FILE IN NOTEPAD
#  Use a decent text editor like Notepad++, Emacs or Vim.
#  If you haven't got a good text editor, you can also,
#  just use Wordpad.
#
# Maya/MmmmTools will overwrite this file. Only configuration
# data will be left intact.
# The keys here are not case sensitive.
        """+'\n'
        
        
class Configuration(object):
    """
    MmmmTools configuration handling module.
    This is used for storing both static configuration
    and for dynamic ini text-file based configuration.
    """
    def __init__(self, parent):
        ## Setup basics refs
        s = self
        s.parent = parent
        s.mmmm = s.parent
        s.pman = s.mmmm.platformManager
        s.conf = Conf(self)
        ## Tracks if ini files had to be copied,        ## if MmmmTools ini copying is required on this Maya start        ## we will set this to true        self.ini_needed_to_be_copied = False
        ## Get path information so that the ConfigParser knows where
        ## to get it's data from
        ini_file_folder_pather = s.pman.info.maya.maya_app_dir_with_version_scripts_pather
        ini_file_name_str = Pather('MmmmTools.ini')        ini_defaults_file_name_str = Pather('MmmmTools-defaults.ini')
        
        ####  ****  This is windows specific.  A check should go here to only do this on windows.
        ####  ****  really proper os aware paths need to be used instead in the long term
        s.ini_file_pather = ini_file_folder_pather + ini_file_name_str        #### Create a pather to defaults,        #### Ensure ini exists, otherwise, copy defaults        try:            s.ini_defaults_file_pather = ini_file_folder_pather + ini_defaults_file_name_str
                                    if not os.path.exists( s.ini_file_pather.str() ):                shutil.copy(    s.ini_defaults_file_pather.str(),  s.ini_file_pather.str()    )                ##print( "new ini copied" )                self.ini_needed_to_be_copied = True            ##else:                ##print( "ini existed already" )        except:            print(  traceback.format_exc()  )
        ## Setup information the ConfigParser and information if will need
        s.configParserDefaultSection = 'mmmmtools_configuration'  #note, the config file is not case sensitive    
        s.configParser = ConfigParser()
        s.items = { 'app':'mmmmTools' }        
        
        ## Parse configuration from ini file
        s.parseConfig()  ## reads ini file and sets its data in self.items
        
    def parseConfig(self):
        #Load initial configuration from file, and make the items dictionary from it.
        self.setItemsByFile()  #automaticall refreshes dictionary
        
        #print out some tests
        Utils.log(  self.getItem('app')  )
        
        #Save The Configuration
        self.setFileByItems()
            ## The written information will be up to date
            ## because fileWrite automatically refreshes from dictionary
                         


    def readConfigFromSelfFile( self ):
        """
        Update the self's configParser by making it read self's file.
        """
        ## Open file and read it to config, this also works for refreshing it from the file        
        fileReadHandle = file( self.ini_file_pather.str()  )
        self.configParser.readfp( fileReadHandle )

        ## Now that the config is loaded, we can close the file
        fileReadHandle.close()        
                         

    def getConfigParserItemList(self):
        """
        Gets the itemList from the default section of the config parser,
        which is the only section this class cares about.
        It is a list of key value pairs that can be entered into
        the items dictionary.
        """
        return self.configParser.items( self.configParserDefaultSection )
                         
    def setItemsByFile(self, refreshItemsDictionary=True):
        """
        Set self's items dict by updating configParser from file and getting it's itemList.
        The optional argument should be depreciated
        """
        self.readConfigFromSelfFile()
        
        
        ## Get an item list from the configParser default section 
        itemList = self.getConfigParserItemList()
        
        ## Refresh the dictionary with the item list if called for
        if refreshItemsDictionary==True:
            self.refreshItemsDictionary( itemList )
    
    def refreshItemsDictionary(self, itemList ):
        """
        Update self 'items' dictionary with the k/v pairs in the item list.
        """
        for k,v in itemList:
            self.items[ k ] = v
        
    
        
    def setFileByItems( self, setItemsFromDictionary=True ):
        """
        Set's the config parser's info from the dictionary and
        then writes the config file.
        """
        if setItemsFromDictionary == True:
            self.setItemsFromDictionary()
        self.writeConfigFileFromConfigParser(  )
            
    def writeConfigFileFromConfigParser(self):
        """
        writeConfigFileFromConfigParser and include some
        default information that should always be on top of the file.
        """
        fileWriteHandle = file( self.ini_file_pather.str() , 'wb' )
        fileWriteHandle.writelines( self.conf.config_file_header_msg_to_user_string )
        self.configParser.write( fileWriteHandle )
        fileWriteHandle.close()
    
    def getItem(self, itemName):
        """
        ...easy exception handling
        """
        try:
            return self.items[itemName]
        except:
            return ""
            
    def setItem(self, itemName, itemValue):
        """
        ...easy exception handling
        """
        try:
            self.items[itemName] = itemValue
        except:
            Utils.log( "Configuraion:  Failed with attempting to set item: ", itemName, itemValue )
            raise   ##This should never happen, but a bug showed once, so the try is still here
            
    def get(self, itemName):
        """
        ...easy exception handling
        """
        return self.getItem( itemName )
        
    def set(self, itemName, itemValue):
        self.setItem( itemName, itemValue )
    
        
    def getItemInConfigParser(self, item, section=''):
        if section == '':
            section = self.configParserDefaultSection
        item = self.configParser.get(section, item)
        return item
        
    def setItemInConfigParser(self, option, value, section='' ):
        if section == '':
            section = self.configParserDefaultSection
        self.configParser.set(section, option, value)
        
    def setItemsFromDictionary(self, dict=None):
        if dict is None:
            dict = self.items
        for k,v in dict.items():
            #Set each item based on the key, and then the value for that key
            self.setItemInConfigParser( k, v )
        
    def getMayaPath(self):
        return Utils.getMayaPath()
