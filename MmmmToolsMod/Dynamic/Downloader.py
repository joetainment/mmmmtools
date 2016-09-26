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


import os, sys, shutil
import urllib
import zipfile

import maya.cmds as cmds
import maya.mel
import pymel.all as pm

from Utils import Utils
from Utils import Pather

u = Utils

class Downloader(object):
    def __init__(self,parent):
        self.parent = parent
        self.mmmm = self.parent
        self.pman = self.mmmm.platformManager
        self.ini = self.mmmm.ini
        self.conf = self.mmmm.conf
    
    
    def download( self ):
        ## Download hklocaltools
        url = self.conf.downloader_hklocaltools_url                
        downloadDirPather = \
            self.pman.info.mmmm.mmmm_pather + \
            self.conf.subscriptsDownloaded_str + \
            self.conf.downloader_hklocaltools_dest_dir

        downloadFileStr = self.conf.downloader_hklocaltools_dest_zip_file
        downloadFilePather = downloadDirPather + downloadFileStr

        self.downloadFile( url, downloadDirPather, downloadFilePather )

        extractToDirPather = downloadDirPather
        extractToFilePather = extractToDirPather + \
                    self.conf.downloader_hklocaltools_dest_mel_file

        fileInsideZip = \
            self.conf.downloader_hklocaltools_file_to_extract
                    
        self.extractFileFromZip(  downloadFilePather, fileInsideZip, 
                            extractToDirPather, extractToFilePather,
                            mode='text' )

                            
        ## File Texture Manager - no extract from zip, it's just a mel
        url = self.conf.downloader_filetexturemanager_url
                
        downloadDirPather = \
            self.pman.info.mmmm.mmmm_pather + \
            self.conf.subscriptsDownloaded_str + \
            self.conf.downloader_filetexturemanager_dest_dir
        
        downloadFilePather = downloadDirPather + \
                self.conf.downloader_filetexturemanager_dest_mel_file
                            
        self.downloadFile( url, downloadDirPather, downloadFilePather )
        
        ## kprogressiverendering  - no extract from zip, it's just a mel
        downloadDirPather = \
            self.pman.info.mmmm.mmmm_pather + \
            self.conf.subscriptsDownloaded_str + \
            self.conf.downloader_kprogressiverendering_dest_dir
        downloadFilePather = downloadDirPather + \
                self.conf.downloader_kprogressiverendering_dest_mel_file        
        url = self.conf.downloader_kprogressiverendering_url
        self.downloadFile( url, downloadDirPather, downloadFilePather )
        
    def downloadFile(self, url, destDirPather, destFilePather):
        try:
            ## In case the folder doesn't exist, make the location
            ## we are downloading to.
            try:
                os.makedirs(   destDirPather.str_   )
            except:
                u.log( "Download dir not created, probably because it "
                        "already exists: " + destDirPather.str_ )
            ## Urllib does the actual downloading here
            urllib.urlretrieve(url,    destFilePather.str_ ) 
        except:
            u.log("Could not download file: " + destFilePather.str_ )        

            
    def extractFileFromZip(self, zipFilePather, fileInsideZip,
                           extractToDirPather, extractToFilePather,
                           mode='binary'):
        try:
            ## open a zip read handle for the downloaded file
            if mode == 'text':
                zmode = 'r'
                emode = 'w'
            elif mode == 'binary':
                zmode = 'rb'
                emode = 'wb'
            zip = zipfile.ZipFile( zipFilePather.str_, zmode )    
            file(extractToFilePather.str_, emode ).write(
                zip.read( fileInsideZip )
                )
            zip.close()
            try:
                file.close()
            except:
                u.log("Could not close extacted file, it probably "
                        "already been closed.")
        except:
            u.log("Could not extract file: " + extractToFilePather.str_ )

        """
        ################################
        ######  Download File Texture Manager
        ################################

    
        ################################
        ######  Download k_progressiveRendering
        ################################
        try:
            ##  The name is what we'll call the file, it gets used for the zip file and the final mel that we write.
            name = self.conf.downloader_kprogressiverendering_name
            
            # The zip file and final mel file have different extensions, set .
            melext = '.mel'
            zipext = '.zip'
        
            
            url = self.conf.downloader_kprogressiverendering_url
            
            #All managed scripts go into the subscripts folder, and then get their appropriate name.
            dest = str(location) + '/' + self.conf.downloader_kprogressiverendering_dest + '/' + name + melext
            #In case the folder doesn't exist, make the location we are downloading to.
            try:
                os.makedirs(   str(location) + '/' + self.conf.downloader_kprogressiverendering_dest   )
            except:
                pass

                
            ## Urllib does the actual downloading here
            urllib.urlretrieve(url,    dest)
                
        except:
            print("Could not download k_progressiveRendering")
        
            
        ################################
        ######  Download Ya Selection Manager
        ################################    
        #try:
        #    ##  The name is what we'll call the file, it gets used for the zip file and the final mel that we write.
        #    name = self.conf.downloader_yaselectionmanager_name
        #    
        #    # The zip file and final mel file have different extensions, set .
        #    melext = '.mel'
        #    zipext = '.zip'
       # 
       #     
       #     url = self.conf.downloader_yaselectionmanager_url
       #     
       #     #All managed scripts go into the subscripts folder, and then get their appropriate name.
       #     dest = str(location) + '/' + self.conf.downloader_yaselectionmanager_dest + '/' + name + melext
       #     #In case the folder doesn't exist, make the location we are downloading to.
       #     try:
       #         os.makedirs(   str(location) + '/' + self.conf.downloader_yaselectionmanager_dest   )
       #     except:
       #         pass
        #
        #        
        #    ## Urllib does the actual downloading here
        #    urllib.urlretrieve(url,    dest) 
        #
        #except:
        #    print("Could not download Ya Selection Manager")
        """