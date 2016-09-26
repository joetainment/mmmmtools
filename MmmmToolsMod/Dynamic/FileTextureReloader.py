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


## This bring all the pymel scripts into the local namespace  it also bring in maya.cmds as cmds and mm as maya.mel
from pymel.core import *
import os, sys


class FileTextureReloader(object):
    def __init__(self, parentRef=None):        self.parentRef = parentRef
        self.fileNodes = []
        self.fileDict = {}
    
    def reload(self):
        self.getFileNodes()
        self.trackFileNodes()
    
    def getFileNodes(self):
        ## Set initial variables
        fileNodes = [] #Start with an empty list of file nodes
        filePath = '' #Set default path to empty
    
        ## Get selection
        sel = ls(sl=1)

        #Test the selection to see if anything is selected, and remember that for later
        try:
            a = (  sel[0] == ""  )
            isSelection = True  # If there is no selection, it will never get to this part
        except:
            isSelection = False
        
        
        ## If nothing is selected,  get all file texture nodes, and reload them all
        if isSelection == False:
            self.fileNodes = ls(typ='file')  #Get all file nodes
            
        ## Else (meaning some objects are selected), get just the file texture nodes attached to them, and then reload those.
        else:
            ## Set up some initial values
            shapeNode = []
            surfaceShader = []
            shadingGroup = []
            connection = []
            
            ## Loop through all the selected object
            for i in range(0,len(sel)):
                shapeNode=listRelatives(sel[i], s=1)
                shadingGroup=listConnections(shapeNode, t="shadingEngine")
                surfaceShader=listConnections(str(shadingGroup[0]) + ".surfaceShader")
                connection=listHistory(surfaceShader)
                self.fileNodes = ls(connection, typ='file')

    def trackFileNodes(self):
        ## Loop through all the current fileNodes
        for fileNode in self.fileNodes:
            filePath=getAttr(fileNode + ".fileTextureName")
            #fileNodeName = getAttr(fileNode + ".name")
            ##Put some logic here to only reload file textures that have changed. ****
            
            fileKey = fileNode + " using " + filePath
            
            fileTime = os.stat(filePath).st_mtime
            
            info = {"name":fileNode, "path": filePath, "time":fileTime}
            
            if fileKey in self.fileDict:
                if self.fileDict[fileKey]["time"] < fileTime:
                    self.refreshFileNode(fileNode, filePath)
                    self.fileDict[fileKey]["time"] = os.stat(filePath).st_mtime
                else:
                    print("File " + filePath + " is already showing newest version.")
                    
                    
            else:
                self.refreshFileNode(fileNode, filePath)
                self.fileDict[fileKey] = info
                

            
    def refreshFileNode(self, fileNode, filePath):
            setAttr((fileNode + ".fileTextureName"), filePath, type="string")
                    
                
    
        
