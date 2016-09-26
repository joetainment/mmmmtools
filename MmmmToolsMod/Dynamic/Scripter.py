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
##
## Center Pivot On Component Selection Originally Written by Kert Saville
##
################################################
import math, sys, os
import traceback
import maya.cmds as cmds
import pymel.all as pm
import random

import maya.OpenMaya as OpenMaya

try:
    reload( ScripterEditor )
except:
    pass
import ScripterEditor

try:
    reload( ScripterMelToPythonConverterUi )
except:
    pass
import ScripterMelToPythonConverterUi

try:
    reload( ScriptFileRunner )
except:
    pass
import ScriptFileRunner

#print( ScriptFileRunner )
#print( ScriptFileRunner.MmmmScriptFileRunner )
#ScriptFileRunner_Mod = ScriptFileRunner
#ScriptFileRunner = ScriptFileRunner_Mod.ScriptFileRunner




class Scripter(object):
    def __init__(self,parentRef):
        self.scripts = {}
        self.parentRef = parentRef
        self.mmmmTools = self.parentRef
        self.conf = self.mmmmTools.configuration.conf
        #self.scriptFileRunner = ScriptFileRunner.MmmmScriptFileRunner(
        #    parentRef = self,
        #    mmmmToolsRef = self.mmmmTools,
        #)

    def runScripterScript( self, scriptName ):
        ## this function should be cleaned up so it doesn't repeat code from runScriptCode
        scriptInfoDict = self.mmmmTools.scripter.scripts[scriptName]
        scriptCode = scriptInfoDict['code']
        module = self.runScriptCode( scriptName=scriptName, scriptCode=scriptCode )
    
    def makeScripterNode( self ):
        node = pm.createNode('mmmmScripterNodeV001v')
        originalName = node.name()
        node.rename( originalName + 'Shape' )
        t = node.getParent()
        t.rename( originalName )
        node.rename( t.name()+'Shape' )
        c = pm.createNode('transform')
        c.rename( 'computationEnforcer' )
        d = pm.createNode('plusMinusAverage')
        d.rename( 'dependency__plug_all_dependencies_into_1D_inputs_00' )
        d.output1D >> node.dependency
        pm.parent( c, t )
        node.output >> c.translateX
        pm.select(t)
        return [t,node,c]
    
    def runScriptCode( self, scriptName='', scriptCode='', add_to_sys_modules=0, populateModule=True ):
    
    
        im = self.mmmmTools.u.importCode
    
        scriptCode = scriptCode.replace('\t','    ')
    
        vars_dict = {}
        

        try:
            self_node = pm.PyNode(scriptName)
            #attrs = self_node.listAttr()
        except:
            self_node = None
            #attrs = None
            print( traceback.format_exc() )
            print( "Continuing, did not add .")

        #attrsDict = {}    
        #if not attrs is None:
        #    for a in attrs:
        #        nodeName, attrName = a.split('.')
        #        attrsDict( str(nodeName) )
                
        
        if populateModule:
            vars_dict['self'] = 'specialMmmmToolsMagicToken_this_var_will_be_replaced'
                ## the im function knows to look for this
            vars_dict['self_name'] = scriptName
            vars_dict['self_node'] = self_node
            vars_dict['pm'] = pm
            vars_dict['mmmmTools'] = self.mmmmTools
            vars_dict['mmmm'] = self.mmmmTools
            vars_dict['U'] = self.mmmmTools.u
            vars_dict['get_connected_nodes'] = \
                self.mmmmTools.u.getConnectedNodesFromArrayTypeAttr
            vars_dict['traceback'] = traceback
            vars_dict['random'] = random
        
        scripts = self.mmmmTools.scripter.scripts
        scriptInfoDict = scripts.setdefault( scriptName, {} )
        module = im( scriptName, scriptCode, vars_dict=vars_dict )

        scriptInfoDict['module']=module
        scripts[scriptName]=scriptInfoDict
        return module
    
    def runScriptsFromSelection(self, attrNameHoldingScriptContents='notes'):
        for obj in pm.ls(selection=True):
            try:
                attr = getattr( obj, attrNameHoldingScriptContents )
                scriptCode = attr.get()
                scriptName = obj.name()
                self.runScriptCode( scriptName,  scriptCode )
            except:
                print("An error occurred and one of the objects scripts couldn't be run.")
                print( traceback.format_exc() )
                print( "Continuing, attempting to run scripts on any other selected objects.")
    
    def runScripterEditor( self, makeUi=True ):
        reload( ScripterEditor )
        self.scripterEditor = ScripterEditor.ScripterEditorUi( makeUi=True, mmmmToolsRef=self.mmmmTools )    

    def runMelToPythonConverterUi( self, makeUi=True ):
        reload( ScripterMelToPythonConverterUi )
        self.scripterEditor = ScripterMelToPythonConverterUi.ScripterMelToPythonConverterUi( makeUi=True, mmmmToolsRef=self.mmmmTools )

    def runScriptFileRunnerUi( self, makeUi=True ):        ## has no current function to not make ui        ## ScriptFileRunner at start refers to the module        reload( ScriptFileRunner )        ScriptFileRunner.ScriptFileRunnerUi( parentRef=self, mmmmToolsRef = self.mmmmTools )
    def connectToAttributeArray( self, attrName=None ):
        if attrName is None:
            attrName = raw_input()
        
        objs = pm.ls(selection=True)

        node_with_attr = objs.pop()

        objsmsgs = [ obj.message for obj in objs ]       
        
        try:
            attr = getattr( node_with_attr, attrName )
        except:
            node_with_attr.addAttr( attrName, dataType='stringArray' )
            attr = getattr( node_with_attr, attrName ) 

        print( 'attr info:' )
        print( attr )
        print( type(attr) )
        attr.set( objsmsgs )
        
    def selectConnectedToAttributeArray( self, attrName=None ):
        if attrName is None:
            attrName = raw_input()
        
        objs = pm.ls(selection=True)
        
        pm.select(clear=True)
        
        for obj in objs:
            arrAttr = getattr(obj, attrName)
            nodes = self.mmmmTools.u.getConnectedNodesFromArrayTypeAttr( arrAttr )
            pm.select( nodes, add=True )

        
        
        