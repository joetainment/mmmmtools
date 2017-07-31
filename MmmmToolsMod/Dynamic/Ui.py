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

import sys, os, shutil, thread, traceback

import maya.cmds as cmds
import maya.mel
import pymel.all as pm
import MmmmToolsMod

import UtilsMod

u = UtilsMod.Utils



class MainMenu(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainWindow = parent.mainWindow
        self.mmmmTools = self.parent.parent
        self.mmmm = self.mmmmTools
        self.ini = self.parent.ini
        self.conf = self.ini.conf
        self.ui = self.parent
        self.menuCount = 0
        self.submenus = {}
        
        try:
            pm.deleteUI( self.menu, menu=True )
        except:
            print( 'Not deleting old main MmmmTools menu, probably because Maya is just starting and it does not yet exist. For exception code see: "Ui.MainMenu.__init__"  ')
            #traceback.print_exc()
        
        try:
            ##Turns out that the main window is capable of directly supporting menus, almost as if it is a menuBarLayout.
            try:
                pm.deleteUI('MmmmTools')
            except:
                doNothing = "MmmmTools isn't in menu"
                
                
            self.menu = pm.menu( 'MmmmTools', parent=self.mainWindow, label = 'MmmmTools', tearOff=True )        
            ## **** Here we need someway to delete old menus! ****      eg:    self.mmmmTools.persistent.menusToDelete.append( self.menu )
        except:
            print("MmmmTools Menu could not be created.  Perhaps it already exists and this is not a problem.")
            traceback.print_exc()
            
        
        
    def startDeferred(self):
        #cmds.evalDeferred("mmmmTools.ui.mainMenu.register()")
        nothing = 5

            # def makeMenu(self, label='', name='', parentMenu='', tearOff=True):
                # self.menuCount += 1

                # if parentMenu=='':
                    # parentMenu = 'MmmmTools'
                # try:
                    # cmds.setParent( 'MmmmTools' , menu=True )
                # except:
                    # print("\n\n  Can't set parent menu  \n\n")
                
                # if label=="":
                    # label = "Menu"+str(self.menuCount)
                
                # fixedLabel = label.replace( " ", "")

                # name = fixedLabel
                
                
                # cmds.menu( name, label=label, parent='MmmmTools', tearOff=tearOff )
        
    def makeMenuItem(self, label=None, name=None, command=None, parentMenu=None, subMenu=False, optionBox = False):
        ## Add to the count of items that are in this menu, so that each item
        ## can can it's own unique number.
        self.menuCount += 1
        
        ## The parentMenu normally exists to support submenus
        ## Normally the new menu item should be added to specified parent
        ## however, if none was given we try to add it to the
        ## self.activeParentMenu, otherwise we fall back on the self.menu
        if parentMenu is None:
            if self.activeParentMenu == None:
                parentMenu = self.menu
            else:
                parentMenu = self.activeParentMenu
        
        ## If no label has been given, generate an automatic label.
        ## This will be obvious when see in the user interface
        if label is None:
            label = "MenuAutoLabel"+str(self.menuCount)
        
        ## Set maya's default parent!
        pm.setParent( parentMenu , menu=True)
        
        ## Maka a code-friendly name that can be used for calling functions
        fixedLabel = label.replace( " ", "").replace(".", "").replace("(", "" ).replace(")","").replace("'", "" )
        
        if name=="":
            name = fixedLabel
        
        if command is None or command=="":
            command = "menu" + fixedLabel
        
        if subMenu==True:
            newMenuItem = pm.menuItem( label=label, sm=True, tearOff=True, allowOptionBoxes=True )
        elif optionBox==True:
            newMenuItem = pm.menuItem( command = getattr(self,command+"Options"), optionBox=True  )
        else:
            try:
                ## This is just hard coded for now, should be made a list in conf or something
                labelFixedForMenu = label
                for word in ["Modeler ", "Texturer ", "Selector ", "Rigger " ]:
                    if labelFixedForMenu.startswith( word ):
                        labelFixedForMenu = labelFixedForMenu.replace( word, "", 1 )
                            ## 1 occurance max replacement
                
                newMenuItem = pm.menuItem(
                                label=labelFixedForMenu,
                                command = getattr(self,command)
                              ) #self[command] )
                
            except:
                newMenuItem = pm.menuItem( label=label+" Not Implemented" )
                u.log( "Attempted to add a MmmmTools menu item for a "
                        "UI command that hasn't been written yet. "
                        "The menu item will do nothing."
                     )
                
        return newMenuItem
        
    def makeSubMenu( self, name ):
        m = self.makeMenuItem(label=name, subMenu=True )
        self.submenus[name] = m
        self.activeParentMenu = m
        return m

    def makeMenuItemFromString(self, stringForItem ):
        st = stringForItem
        
        if st == 'div' or st == 'divider':
            pm.menuItem( divider=True )
        elif st == 'Menu Main':
            self.activeParentMenu = self.menu
            pm.setParent( self.menu, menu=True )
            #u.log('Going back to parent menu')
        elif st.startswith( 'Menu '):
            stsub = st.replace('Menu ','')
            #u.log( 'stsub is: ' + stsub )            
            self.makeSubMenu( stsub )
            #u.log('Entering Sub menu')
        elif st.startswith('optionBox '):
            stsub = st.replace('optionBox ', '')
            #u.log( 'stsub is: ' + stsub )
            self.makeMenuItem( label=stsub, optionBox=True )
        else:
            self.makeMenuItem( label=st )
        
        
    def register(self):
        try:      
            self.activeParentMenu = self.menu
            pm.setParent( self.menu, menu=True )
            pm.menuItem(  divider=True );
            
                ## Obsolete, never worked anyway has syntax errors
                ## just an idea...
                    ## mi will make menu items
                    #mi = lambda x(y): self.makeMenuItem( label=y )
                
                    ## md will make dividers
                    #md = lambda x: pm.menuItem(divider=True)    
            
            ## Put a bunch of strings in a list
            ## which will be used to make menu items
            items = [
                #'MmmmTools Dockable UI...',
                #'div',
                'Save Incrementally',
                'Set Project By Pasting Or Typing',
                'div',
                #'Activate Hotkey Manager',
                #'Save User Hotkeys',
                #'Restore Earlier Saved Hotkeys',
                #'div',
                #'Set Hotkeys To Factory Defaults',
                #'Set Hotkeys To User Defaults',
                #'div',
                #'Set Hotkeys To Polygons',
                #'Set Hotkeys To Rendering',
                #'Set Hotkeys To UVs',
                #'div',
                'Hotkeys Window...',
                'Hotstring Window...',
                'div',
                'Menu Selector',                        
                    'Selector     Store Selection To Slot' ,
                    "Selector     Select From Slot's Selection" ,
                    'div',
                    'Selector     Previous Slot' ,
                    'Selector     Next Slot' ,
                    'div',
                    'Selector     Set And Save Named Slot By Name' ,
                    'Selector     Select Named Slot By Name' ,
                    'div',
                    'Selector     Show Used Named Slots' ,
                    'div',
                    #'div',
                    ## Volume Select App/Tool/UI current disabled because of a Maya crash bug.
                    #'Selector     Volume Select Tool' ,
                    'Selector     Volume Select Verts' ,
                    'Selector     Volume Select Faces' ,
                'Menu Main',                     
                'Menu Modeler',                        
                    'Modeler Split Polygon Tool' ,
                    'div',
                    'Modeler Select Non Quads' ,
                    'Modeler Select Tris' ,
                    'Modeler Select NGons' ,
                    'Modeler Select Quads' ,
                    'div',
                    'Modeler Select Hard Edges' ,
                    'Modeler Select Creased Edges' ,
                    'Modeler Crease Selected Edges' ,
                    'Modeler Uncrease Selected Edges' ,
                    'Modeler Crease And Harden Selected Edges' ,
                    'Modeler Uncrease And Soften Selected Edges' ,
                    'Modeler Propagate Edge Hardness On' ,
                    'Modeler Propagate Edge Hardness Off' ,
                    'div',
                    'Modeler Vertex Aligner',
                    'Modeler Center Pivot On Components',
                    'div',
                    'Modeler Zero Pivot Delete History Freeze Xforms WS',
                    'div',
                    'Modeler Mr Clean',
                    'Modeler Retopology Tools',
                    'Modeler Grid Tools',
                    'Modeler Mirror Tools',
                'Menu Main',
                'Menu Texturer',
                    'Texturer Reload Textures',
                    'Texturer UV Xforms Tool',                    
                    'Texturer Select Seams',
                    'Texturer Show Seams',
                    'div',
                    'Texturer Calc And Store UV Sizing',
                    'Texturer Apply Stored UV Sizing',
                    'Texturer Apply Numerical UV Sizing',
                    'div',
                    'Texturer Unfold3D Only Selected',
                    'Texturer Unfold3D Multiple Objects',
                    'div',
                    'Texturer FileTextureManager',
                'Menu Main',                
                'Menu Rigger',
                    'Rigger Attribute Setter',
                    'Rigger Attribute Connector',
                    'Rigger Rename By Regular Expression',
                    'div',
                    'Rigger Pivot Fix',
                    'Rigger Replace Objects',
                    'Rigger Move Up In Hierarchy',
                    'div',
                    'Rigger Align Xforms',
                    'Rigger Constrain Xforms',
                    'Rigger Align Then Constrain Xforms',
                    'Rigger Zero',
                    'Rigger Make Pole Vector',
                    'div',
                    'Rigger Joint Orient Helper',
                    'Rigger Create Twist Joint To Selected Child',
                    'Rigger Create Rivets',
                'Menu Main',
                'Menu Renderer',
                    ## The following line is diabled because MIP shaders work by default in Maya 2011, so it isn't needed right now.
                    'Renderer Show Hypershade MIP Shaders',
                    'Renderer Create Rim Light',
                    'Renderer Adjust Lighting',
                    'Renderer Reflectivity Of Selected Materials To Zero',
                    'Renderer Add VRay Texture Input Gamma Attributes',
                    'Renderer Set VRay Texture To SRGB',
                    'Renderer Set VRay Texture To Linear',
                    'Renderer Enable Hypergraph Thumbnails',
                    'Renderer Disable Hypergraph Thumbnails',
                    'Renderer Expose MIP Shaders   Restart Required',
                    'Renderer Do Not Expose MIP Shaders   Restart Required',
                    'Renderer Transfer Shading Sets By Space For Sel',
                    'Renderer Transfer Shading Sets By Component For Sel',
                    ##  The following two lines are for future planned features
                    #'Create Occluded Ambient Light' )
                    #'Render Animation Interactively' )
                'Menu Main', 
                'Menu Gamer',
                    'Gamer Add Attributes For Export To Selected Objects',
                    'div',                          
                    'Gamer FBX Export Selection',
                    'Gamer FBX Export All', 
                    'div',
                    'Gamer Make UCX Objects And Parent To Last Selected Object',                   
                'Menu Main', 
                'Menu Scripter',
                    'Scripter Editor',
                    'Scripter Run Scripts From Selection',
                    'div',                    
                    'Scripter Connect To Attribute Array By Typing Name',
                    'Scripter Select Connected To Array By Typing Name',
                    'div',
                    'Scripter Make Scripter Node',
                    'div',                    'Scripter File Runner',
                    'div',
                    'Scripter Mel To Python Converter Ui',
                'Menu Main',                
                'div',
                #'Menu Open Maya Toolbox',
                #    'OMT Connect Components',
                #    'OMT Scale Position',
                #    'OMT Select Element',
                #    'OMT Selection Dragger',
                #    'optionBox OMT Selection Dragger',
                #    'OMT Select Loop',
                #    'OMT Select Outline',
                #    'optionBox OMT Select Outline',
                #    'OMT Select Ring',
                #    'OMT Spin Edge',
                #    'OMT Split Around Selection',
                #    'OMT Split Loop',
                #    'OMT Xray Toggle',
                #    'About The Open Maya Toolbox',
                'Menu Main',
                'div',      
                #'Download Extra Scripts...',
                #'HKLocalTools (Downloaded)',
                #
                #'ProgressiveRendering (Downloaded)',
                #'GoZ (Shelf Button Substitute)',
                'div',                
            ]
                
            for item in items:
                #if item == 'Menu Main':
                #    
                #    pm.setParent( self.menu, menu=True )   
                #    u.log('Going back to parent menu')
                #else:
                if isinstance( item, basestring ):
                    self.makeMenuItemFromString( item )
                #elif isinstance(item, dict ):
                #    self.makeMenuItemFromDict( item )
            ## Set back to standard menu
            pm.setParent( self.menu, menu=True )            
            
            
            ## Prepare to make make menus via commander
            commander = self.mmmm.commander
            cmdEntries = commander.entries


            
            #### Make Developer Menu
            developerMenu = pm.menuItem( label='MmmmTools Developer...', sm=True, tearOff=True, allowOptionBoxes=True )
            self.submenus['developerMenu']=developerMenu
            pm.setParent( developerMenu, menu=True )
            for name, entry in cmdEntries.items():
                inMenu = entry['inMenu']
                print( name )
                if inMenu==True or inMenu=='Developer':
                    print( "in menu name is:")
                    print( entry['name'] )
                    uiLabel = entry.get( 'uiLabel' )
                    if uiLabel==None:
                        uiLabel = name
                    pm.menuItem( label=uiLabel,
                        command='mmmmTools.commander.commands["' + name + '"]()',
                    )
                    
            
            commander = self.mmmm.commander
            cmdEntries = commander.entries
            
            pm.setParent( developerMenu, menu=True )
            modelerMenu = self.submenus['modeler'] = pm.menuItem(
                label='Modeler (dev)...', sm=True, tearOff=True,
                allowOptionBoxes=True
            )
            pm.setParent( modelerMenu, menu=True )
            for name, entry in cmdEntries.items():
                inMenu = entry.inMenu
                if inMenu=='Modeler':
                    uiLabel = entry.get( 'uiLabel' )
                    if uiLabel==None:
                        uiLabel = name
                    pm.menuItem( label=uiLabel,
                        command='mmmmTools.commander.commands["' + name + '"]()',
                    )
                    
            pm.setParent( developerMenu, menu=True )
            selectorMenu = self.submenus['selector'] = pm.menuItem(
                label='Selector (dev)...', sm=True, tearOff=True,
                allowOptionBoxes=True
            )
            pm.setParent( selectorMenu, menu=True )
            for name, entry in cmdEntries.items():
                inMenu = entry.inMenu
                if inMenu=='Selector':
                    uiLabel = entry.get( 'uiLabel' )
                    if uiLabel==None:
                        uiLabel = name
                    pm.menuItem( label=uiLabel,
                        command='mmmmTools.commander.commands["' + name + '"]()',
                    )
                    
                    
                    

            pm.menuItem( divider=True )
                               
                    
                    
                    
                    
                    
                    
                    
                        
            pm.setParent( self.menu, menu=True )    
            pm.menuItem( divider=True )    
            pm.menuItem( divider=True )
            pm.menuItem( divider=True )
            ## This one should go last!  Its the about box
            pm.menuItem( "MmmmToolsHelp", label='MmmmTools Help', annotation='Help not yet available.',command=self.menuHelp )
            pm.menuItem( "MmmmToolsAbout", label='About MmmmTools', command=self.menuAbout )

        except:
            u.log("Failed to create MmmmTools main menu.")

    def makeMenuItemFromDict( itemDict ):
        label = itemDict.Label
        command = itemDict['command']
        
    def menuMmmmToolsDockableUI(self, state=None):
        self.mmmmTools.uiDockable.create()
    def menuOMTSettings(self, state=None):
        maya.mel.eval('source "OMT_toolboxMenuForMmmm.mel";')
        maya.mel.eval("OMT_toolManageInterface()")
    def menuOMTConnectComponents(self, state=None):
        maya.mel.eval("OMT_to_connectComponents()")
    def menuOMTScalePosition(self, state=None):
        maya.mel.eval("OMT_to_scalePosition()")
    def menuOMTSelectElement(self, state=None):
        maya.mel.eval("OMT_to_selectElement()")
    def menuOMTSelectionDragger(self, state=None):
        maya.mel.eval("OMT_to_selectionDragger()")
    def menuOMTSelectionDraggerOptions(self, state=None):
        maya.mel.eval('source "OMT_to_selectionDragger.mel";')
        maya.mel.eval("OMT_to_selectionDraggerOptWin();")
    def menuOMTSelectLoop(self, state=None):
        maya.mel.eval("OMT_to_selectLoop()")
    def menuOMTSelectOutline(self, state=None):
        maya.mel.eval("OMT_to_selectOutline()")
    def menuOMTSelectOutlineOptions(self, state=None):
        maya.mel.eval('source "OMT_to_selectOutline.mel";')
        maya.mel.eval("OMT_to_selectOutlineOptWin();")
    def menuOMTSelectRing(self, state=None):
        maya.mel.eval("OMT_to_selectRing()")
    def menuOMTSpinEdge(self, state=None):
        maya.mel.eval("OMT_to_spinEdge()")
    def menuOMTSplitAroundSelection(self, state=None):
        maya.mel.eval("OMT_to_splitAroundSelection()")
    def menuOMTSplitLoop(self, state=None):
        maya.mel.eval("OMT_to_splitLoop()")
    def menuOMTXrayToggle(self, state=None):
        maya.mel.eval("extras_to_xrayToggle()")        
 
    def menuSaveIncrementally(self, state=None):
        self.mmmmTools.u.saveIncrementally()
    def menuSetProjectByPastingOrTyping(self, state=None):
        self.mmmmTools.uiUtils.setProjectByStringUi()
        
        
                              
    def menuSelectorStoreSelectionToSlot(self, state=None):
        self.mmmmTools.selector.setSlot() 
    def menuSelectorSelectFromSlotsSelection(self, state=None):
        self.mmmmTools.selector.selSlot() 
    def menuSelectorPreviousSlot(self, state=None):
        self.mmmmTools.selector.prevSlot() 
    def menuSelectorNextSlot(self, state=None):
        self.mmmmTools.selector.nextSlot() 
    def menuSelectorSetAndSaveNamedSlotByName(self,state):
        self.mmmmTools.selector.setNamedSlotByUi() 
    def menuSelectorSelectNamedSlotByName(self,state):
        self.mmmmTools.selector.selNamedSlotByUi() 
    def menuSelectorShowUsedNamedSlots(self,state):
        self.mmmmTools.selector.showSlotsUi() 
    ## Volume Select App/Tool/UI current disabled because of a Maya crash bug.
    #def menuSelectorVolumeSelectTool(self,state):
    #    self.mmmmTools.selector.volumeSelectApp( ) 
    def menuSelectorVolumeSelectVerts(self,state):
        self.mmmmTools.selector.volumeSelect( ) 
    def menuSelectorVolumeSelectFaces(self,state):
        self.mmmmTools.selector.volumeSelect( faces=True ) 
        

        
    def menuModelerSplitPolygonTool(self, state=None):
        self.mmmmTools.modeler.activateSplitPolygonTool() 
        
    def menuModelerSelectHardEdges(self, state=None):
        self.mmmmTools.modeler.selectHardEdges()         
    def menuModelerSelectCreasedEdges(self, state=None):
        self.mmmmTools.modeler.selectCreasedEdges()
        
    def menuModelerSelectNonQuads(self, state=None):
        self.mmmmTools.modeler.selectNonQuads()
    def menuModelerSelectTris(self, state=None):
        self.mmmmTools.modeler.selectTris()
    def menuModelerSelectNGons(self, state=None):
        self.mmmmTools.modeler.selectNgons()
    def menuModelerSelectQuads(self, state=None):
        self.mmmmTools.modeler.selectQuads()
       
        
    def menuModelerVertexAligner(self, state=None):
        self.mmmmTools.modeler.runAligner( ) 
    def menuModelerPropagateEdgeHardnessOn(self, state=None):
        self.mmmmTools.modeler.propagateEdgeHardnessOn() 
    def menuModelerPropagateEdgeHardnessOff(self, state=None):
        self.mmmmTools.modeler.propagateEdgeHardnessOff() 
    def menuModelerCreaseSelectedEdges(self, state=None):
        self.mmmmTools.modeler.creaseSelectedEdges() 
    def menuModelerUncreaseSelectedEdges(self, state=None):
        self.mmmmTools.modeler.uncreaseSelectedEdges()
    def menuModelerCreaseAndHardenSelectedEdges(self, state=None):
        self.mmmmTools.modeler.creaseSelectedEdges()
        pm.polySoftEdge( angle=0.0 )
    def menuModelerUncreaseAndSoftenSelectedEdges(self, state=None):
        self.mmmmTools.modeler.uncreaseSelectedEdges()
        pm.polySoftEdge( angle=180.0 )
    def menuModelerCenterPivotOnComponents(self, state=None):
        self.mmmmTools.modeler.centerPivotOnComponents() 
        
    def menuModelerZeroPivotDeleteHistoryFreezeXformsWS(self, state ):
        m = self.mmmmTools.modeler
        m.pivotToZeroDeleteHistoryAndFreezeTransformsInWorldSpace()

        
    def menuModelerMrClean(self, state=None):
        self.mmmmTools.modeler.runMrClean()
    def menuModelerMirrorTools(self, state=None):
        self.mmmmTools.modeler.runMirrorer()
    def menuModelerGridTools(self, state=None):
        self.mmmmTools.modeler.runGridTools( )
    def menuModelerRetopologyTools(self, state=None):
        self.mmmmTools.modeler.runRetoper( makeUi=True )

        
           
    def menuTexturerReloadTextures(self, state=None):
        self.mmmmTools.texturer.reloadTextures( )
    def menuTexturerShowSeams(self, state=None):
        self.mmmmTools.texturer.toggleSeams( )
    def menuTexturerSelectSeams(self, state=None):
        self.mmmmTools.texturer.selectSeams( ) 
    def menuTexturerRoadkill(self, state=None):
        self.mmmmTools.texturer.roadkill( )
    def menuTexturerUVXformsTool(self,state):
        self.mmmmTools.texturer.runUvXformsTool()
        
    def menuTexturerCalcAndStoreUVSizing(self,state):
        self.mmmmTools.texturer.grabUvToWorldRatioOfSelection()
    def menuTexturerApplyNumericalUVSizing(self,state):
        self.mmmmTools.texturer.applyNumericalUvToWorldRatioToSelection()        
    def menuTexturerApplyStoredUVSizing(self,state):
        self.mmmmTools.texturer.applyGrabbedUvToWorldRatioToSelection()
      
    def menuTexturerUnfold3DOnlySelected(self,state):
        self.mmmmTools.texturer.unfold3dOnlySelected()
    def menuTexturerUnfold3DMultipleObjects(self,state):
        self.mmmmTools.texturer.unfold3dMultipleObjects()

        
    def menuTexturerFileTextureManager(self, state=None):
        try:
            maya.mel.eval('FileTextureManager();')
        except:
            traceback.print_exc()        


        
    def menuRendererShowHypershadeMIPShaders(self, state=None):
        self.mmmmTools.renderer.runProductionShadersMaker()  ## This used to actually make shaders, now it just enables them to be shown in the hypershade.
        
        
    def menuRendererAddVRayTextureInputGammaAttributes(self, state ):
        self.mmmmTools.renderer.addVrayTextureInputGammaAttributes()
    def menuRendererSetVRayTextureToSRGB(self, state ):
        self.mmmmTools.renderer.setVrayTextureToSRGB()
    def menuRendererSetVRayTextureToLinear(self, state ):
        self.mmmmTools.renderer.setVrayTextureToLinear()
        
    def menuRendererTransferShadingSetsByComponentForSel(self,state):
        MmmmToolsMod.Static.ShadingEngine.transferShadingSetsByComponentForSel( )
    def menuRendererTransferShadingSetsBySpaceForSel(self,state):
        MmmmToolsMod.Static.ShadingEngine.transferShadingSetsBySpaceForSel( )
        
        
    def menuRiggerReplaceObjects(self, state=None):
        self.mmmmTools.rigger.replaceObjects() 
    def menuRiggerPivotFix(self, state=None):
        self.mmmmTools.rigger.pivotFix()  
    def menuRiggerMoveUpInHierarchy(self, state=None):
        self.mmmmTools.rigger.moveUpInHierarchy()
    def menuRiggerAlignThenConstrainXforms(self, state=None):
        self.mmmmTools.rigger.alignThenConstrain()        
    def menuRiggerAlignXforms(self, state=None):
        self.mmmmTools.rigger.align()        
    def menuRiggerConstrainXforms(self, state=None):
        self.mmmmTools.rigger.constrain() 
    def menuRiggerZero(self, state=None):
        self.mmmmTools.rigger.zero()
    def menuRiggerMakePoleVector(self, state=None):
        self.mmmmTools.rigger.makePoleVector()
    def menuRiggerJointOrientHelper(self, state=None):
        self.mmmmTools.rigger.runJointOrientHelper()
    def menuRiggerCreateRivets(self, state=None):
        self.mmmmTools.rigger.runRiveter()
    def menuRiggerAttributeSetter(self, state=None):
        self.mmmmTools.rigger.runAttributeSetter()
    def menuRiggerAttributeConnector(self, state=None):
        self.mmmmTools.rigger.runAttributeConnector()
    def menuRiggerRenameByRegularExpression(self, state=None):
        self.mmmmTools.rigger.runRenameByRegex()    def menuRiggerCreateTwistJointToSelectedChild(self, state=None):
        MmmmToolsMod.Static.Joints.createTwistJointToSelectedChild()

    def menuGamerMakeUCXObjectsAndParentToLastSelectedObject(self,state):
        self.mmmmTools.gamer.runGamerMakeAndParentUcx()
        
    def menuGamerAddAttributesForExportToSelectedObjects(self,state):
        self.mmmmTools.gamer.runGamerAddAttributesForExport()
    #def menuGamerAddAttributeForExportPath(self,state):
    #    self.mmmmTools.gamer.runGamerAddAttributeForExportPath()
        


    def menuGamerFBXExportSelection(self, state=None):
        self.mmmmTools.gamer.runGamerFbxExportSelection()
    def menuGamerFBXExportAll(self, state=None):
        self.mmmmTools.gamer.runGamerFbxExportAll()
        
    def menuScripterEditor(self, state=None):
        self.mmmmTools.scripter.runScripterEditor()
    def menuScripterRunScriptsFromSelection(self, state=None):
        self.mmmmTools.scripter.runScriptsFromSelection()
    def menuScripterConnectToAttributeArrayByTypingName(self,state):
        self.mmmmTools.scripter.connectToAttributeArray()
    def menuScripterSelectConnectedToArrayByTypingName(self,state):
        self.mmmmTools.scripter.selectConnectedToAttributeArray()
    def menuScripterMakeScripterNode(self,state):
        try:
            pm.loadPlugin(
                self.mmmm.platformManager.info.mmmm.mmmm_pather
                + 'plugins/MmmmScripterNodeV001vPlugin.py'
            )
        except:
            print( traceback.format_exc() )
        self.mmmmTools.scripter.makeScripterNode()

    def menuScripterFileRunner(self,state):
        self.mmmmTools.scripter.runScriptFileRunnerUi()
    def menuScripterMelToPythonConverterUi(self,state):
        self.mmmmTools.scripter.runMelToPythonConverterUi()     
        
        
    def menuEnableMmmmTools(self, state=None):
        if state == 0:
            self.conf.mmmmToolsEnabled = state
        elif state == 1:
            self.conf.mmmmToolsEnabled = state             

    def menuHotkeysWindow(self, state=None):
        self.mmmmTools.hotkeys.createUi()
    def menuHotstringWindow(self, state=None):
        self.mmmmTools.hotstrings.go()           
        
    ##  Autoback is no longer used in Maya 2011 because autodesk added their own
    #def menuAutobackSettings(self, state=None):
    #    self.ui.popupWindowAutobackSettings()
        
    def menuRendererCreateRimLight(self, state=None):
        self.mmmmTools.rimLight.create()
    def menuRendererCreateOccludedAmbientLight(self, state=None):
        print( "This function is not yet available.")
    def menuRendererAdjustLighting(self, state=None):
        self.mmmmTools.renderer.runLightsMultiplier()
    def menuRendererReflectivityOfSelectedMaterialsToZero(self, state=None):
         self.mmmmTools.renderer.reflectivityOfSelectedMaterialsToZero()
    def menuRendererRenderAnimationInteractively(self, state=None):
        print( "This function is not yet available.")
    def menuRendererEnableHypergraphThumbnails(self, state=None):
        self.mmmmTools.renderer.setHypershadeThumbnailsEnabled( enabled=True )
    def menuRendererDisableHypergraphThumbnails(self, state=None):
        self.mmmmTools.renderer.setHypershadeThumbnailsEnabled( enabled=False )
    def menuRendererExposeMIPShadersRestartRequired(self, state=None):
        self.mmmmTools.renderer.setMipShadersEnabled( enabled=True )
    def menuRendererDoNotExposeMIPShadersRestartRequired(self, state=None):
        self.mmmmTools.renderer.setMipShadersEnabled( enabled=False )
        


    def menuSelectTextureBorderEdges(self, state=None):
        try:
            self.mmmmTools.selectTextureBorderEdges.selectTextureBorderEdges()
        except:
            traceback.print_exc()
        
    def menuRoadKill(self, state=None):   ## This should be moved elsewhere, perhaps into the autoscripts module?
        pass
            
    def menuReloadTextures(self, state=None):   ## This should be moved elsewhere, perhaps into the autoscripts module?
        try:
            self.mmmmTools.fileTextureReloader.reload()
        except:
            traceback.print_exc()
            
            
    def menuHKLocalToolsDownloaded(self, state=None):   ## This should be moved elsewhere, perhaps into the autoscripts module?
        try:
            maya.mel.eval('HKLTOptionBox();')
        except:
            traceback.print_exc()
    def menuProgressiveRenderingDownloaded(self, state=None):   ## This should be moved elsewhere, perhaps into the autoscripts module?
        try:
            maya.mel.eval('source "k_progressiveRendering"; k_progressiveRendering();')
        except:
            traceback.print_exc()        
        
    # def menuGoZShelfButtonSubstitute(self,state):
        # pm.mel.eval(
            # """source "C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushFromMaya.mel";"""
        # )
        
    def menuSaveUserHotkeys(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.saveHotkeys()
        
    def menuRestoreEarlierSavedHotkeys(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.goBackToOlderHotkeys()
        
    def menuSetHotkeysToUserDefaults(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.setHotkeysToDefaults()
        
    def menuSetHotkeysToFactoryDefaults(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.setHotkeysToDefaultsNoUserHotkeys()
        
    def menuSetHotkeysToPolygons(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.setHotkeysToPolygons()
        
    def menuSetHotkeysToUVs(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.setHotkeysToUvs()
        
    def menuSetHotkeysToRendering(self, state=None):
        if int(  self.ini.getItem("enable_hotkeys")  ) == 1:
            self.mmmmTools.hotkeys.setHotkeysToRendering()
            

    def menuEnableAutosave(self, state=None):
        self.mmmmTools.autosaveEnabler.go()

    ## Functions that bring up dialog windows from dialogger
    def menuDisableCapslock(self, state=None):
        self.mmmmTools.capsDisabler.disableCapslock()
        self.ui.dialogger.popupWindowDisableCapslock()
        
    def menuHelp(self, state=None):
        self.ui.dialogger.popupWindowHelp()
        
    def menuAbout(self, state=None):
        self.ui.dialogger.popupWindowAbout()

    def menuActivateHotkeyManager(self, state=None):
        self.ui.dialogger.popupWindowActivateHotkeyManager()    

    def menuAboutTheOpenMayaToolbox(self, state=None):
        self.ui.dialogger.popupWindowOMT()
    #def menuOMTCullingToggle(self, state=None):
        #maya.mel.eval("extras_to_toggleCulling()")

    def menuDownloadExtraScripts(self, state=None):   ## This should be moved elsewhere, perhaps into the autoscripts module?
        self.ui.dialogger.popupWindowDownloadScriptsConfirm()
        
        
        
        
class Ui(object):
    """
    MmmmTools User Interface class.
    This is the main user interface for MmmmTools.
    It creates the main menu entry and any other core
    UI components that are needed.
    """
    def __init__(self, parent):
        self.parent = parent
        self.mmmm = self.parent
        self.ini = self.parent.ini
        self.conf = self.ini.conf
        
        info = u.getMainWindowInfo()
        self.mainWindow = info.mainWindow  ## a pymel object
        self.mainWindowName = info.mainWindowName ## just a str
        
        self.dialogger = UiDialogCreator(parent=self)
        
        try:
            self.mainMenu = MainMenu(self)
        except:
            u.log( "MainMenu could not be created." )
        else:
            self.mainMenu.register()
            self.addUiFromCommander()
    
    def addUiFromCommander(self):
        commander = self.mmmm.commander
        # Not implemented yet
        #          
        #for name, entry in commander.entries.items():
        #
        #    newMenuItem = pm.menuItem(
        #                    label=k,
        #                    command = v + ';',
        #    ) #self[command] )

class UiDialogCreator(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.mmmm = self.parent.mmmm
        self.ini = self.parent.ini
        self.conf = self.ini.conf
        pass
        
    def popupWindowHelp(self):
        cmds.window( title="MmmmTools Help", iconName='About', width=500, height = 300 )
        cmds.columnLayout( adjustableColumn=True )
        
        cmds.text( label=' ', align='center' )
        cmds.text( label="""
        
        MmmmTools help is currently only available online.
        
        Please visit:
        http://mmmmtools.celestinestudios.com
        
        
        """, align='center' )

        cmds.text( label=' ', align='center' )        
        
        cmds.showWindow()

        
    def popupWindowDownloadScriptsConfirm(self):
        self.downloadScriptsConfirmWindow = cmds.window( 'DownloadScriptsConfirm', title='Please save first', iconName='Please save', width=430, height = 200 )
        cmds.columnLayout( adjustableColumn=True )

        cmds.text( label=' ', align="center" )
        cmds.text(align='left' , label="""
        MmmmTools can automatically download scripts from the internet for you.
        
        Please save your work before proceeding, so you are safe        
        in the unlikely event that a problem occurs while downloading.
            
        After you have saved, click the button below. Once the download completes
        information about it will be shown.
        
            """ )

        cmds.button( 'DownloadScripts' , command=self.downloadScripts , label='Download Scripts Now', align='center' )
        
        cmds.showWindow() 
        
        
    def popupWindowDisableCapslock(self):
        self.disableCapslockWindow = cmds.window( 'DisableCapslock', title="Capslock Disable Functionality", iconName='CapsDisable', width=600, height = 450 )
        cmds.columnLayout( adjustableColumn=True )
        
        cmds.text( label=' ', align='center' )
        
        cmds.text( label="""
        
        -- About The Capslock Diable Functionality --
        
        MmmmTools uses it's own version of autohotkey to disable capslock.
        
        *** An Autohotkey icon, an "H" icon, should now show in the system try ***
        The script runs independently of Maya, and won't automatically end when Maya closes.
        
        To turn off the Capslock Disabling functionality, right click on the icon,
        "h" in the system tray, and choose "Exit".
        
        The MmmmTools Capslock Disabling functionality is useful because Maya
        hotkeys don't work the same when capslock in turned on.  Often
        users will push keys after accidentally turning capslock on,
        and the keys will not have the desired effects.  By disabling capslock,
        this problem is solved. It also helps you to more easily type underscores,
        the caps lock key will function as an underscore key while the autohotkey
        script is in use.
        
        Even while using this autohotkey script, you can still toggle caps lock.
        You can turn it on and off by pushing:  Ctrl+Shift+Capslock=
        
        For more info about autohotkey, see: http://www.autohotkey.com/
        
        -- This window can safely be closed. --
        
        """, align='left' )
        
        cmds.text( label=' ', align='center' )        
        cmds.showWindow()

        
    def popupWindowDownloadScriptsConfirm(self):
        self.downloadScriptsConfirmWindow = cmds.window( 'DownloadScriptsConfirm', title='Please save first', iconName='Please save', width=430, height = 200 )
        cmds.columnLayout( adjustableColumn=True )

        cmds.text( label=' ', align="center" )
        cmds.text(align='left' , label="""
        MmmmTools can automatically download scripts from the internet for you.
        
        Please save your work before proceeding, so you are safe        
        in the unlikely event that a problem occurs while downloading.
            
        After you have saved, click the button below. Once the download completes
        information about it will shown.
        
            """ )

        cmds.button( 'DownloadScripts' , command=self.downloadScripts , label='Download Scripts Now', align='center' )
        
        cmds.showWindow() 
        
    #def downloadScripts(self, state=None):
    #    self.mmmmTools.downloader.download()
    #    cmds.deleteUI( self.downloadScriptsConfirmWindow )
    #    self.popupWindowPleaseRestartMaya()
    
    def downloadScripts(self, state=None):
        self.mmmm.downloader.download()
        cmds.deleteUI( self.downloadScriptsConfirmWindow )
        self.popupWindowPleaseRestartMaya()
            
        
    def popupWindowPleaseRestartMaya(self):
        self.restartWindow = cmds.window( 'Restart', title="Restart of Maya Required", iconName='Restart', width=600, height = 450 )
        cmds.columnLayout( adjustableColumn=True )
        
        cmds.text( label=' ', align='center' )
        
        cmds.text( label="""
        
        -- Please read this message and then restart Maya when conveinient. --
        
        MmmmTools has downloaded and installed additional scripts.
        The (Downloaded) functions in the MmmmTools menu should now work.
        
        The scripts downloaded are not actually part of MmmmTools. MmmmTools simply has functions
        that make setting up and using these scripts easier. Here is some more information:
        
        HKLocalTools - By Henry Korol
        http://www.henrykorol.com/Scripts/LocalTools/LTDocInstallation.htm

        FileTextureManager - By Crow Yeh
        http://www.highend3d.com/maya/downloads/mel_scripts/data_management/1012.html
        
        K_ProgressiveRendering - By Sylvain Berger
        http://www.creativecrash.com/maya/downloads/scripts-plugins/rendering/mental-ray/c/k_progressive_rendering--2
        
        -- This window can safely be closed. --
        
        """, align='left' )
        
        cmds.text( label=' ', align='center' )        
        cmds.showWindow()
        
    def popupWindowOMT(self):
        cmds.window( title="About The Open Maya Toolbox", iconName='About OMT', width=500, height = 300 )
        cmds.columnLayout( adjustableColumn=True )
        
        cmds.text( label=' ', align='center' )
        
        cmds.text( label="""
        
        
        
        The Open Maya Toolbox is a collection of open source scripts for Maya.
        The scripts provide several missing features in Maya, and also act
        as substitutes for some of Maya's features that don't work well.
        
        The website provides documentation and even video tutorials, so it is quite easy to learn.
        
        The Open Maya Toolbox was created by Jakob Welner. Joe Crawford integrated it with MmmmTools.
        
        See the website for more information:
        http://jakob.welner.dk/omtwiki/index.php/Main_Page        
        
        """, align='left' )
        
        cmds.text( label=' ', align='center' )        
        cmds.showWindow()
        
    def popupWindowActivateHotkeyManager(self):
        self.activateHotkeyManagerWindow = cmds.window( 'ActivateHotkeyManagerWindow', title='Activate Hotkey Manager?', iconName='Activate?', width=650, height = 340 )
        cmds.columnLayout( adjustableColumn=True )

        cmds.text( label=' ', align="center" )
        cmds.text(align='left' , label="""
        Are you sure you want to activate the Hotkey System?
        
        The Hotkey system in MmmmTools is extremely useful, but it does change the way hotkeys work.
            
        You old hotkeys will be preserved anyway, but as an extra precaution, the original files
        will be backup up as:
          userHotkeys.mel.bak
          userNamedCommands.mel.bak
          userRunTimeCommands.mel.bak
            
        You can simply rename those files, deleting the ".bak" from the end if you
        wish to restore the original hotkeys in full.
            
        Once activated, to setup and save more of your own custom hotkeys, use "Set Hotkeys To Users Default"
        from the MmmmTools menu, then edit your hotkeys, hit save, and then use "Save User Hotkeys" from the
        MmmmTools menu.
        
            """ )

        cmds.button( 'ActivateHotkeyManagerButton' , command=self.popupWindowActivateHotkeyManagerConfirmed , label='Activate Hotkey Manager Now', align='center' )
        
        cmds.showWindow()          
        
    
    def popupWindowActivateHotkeyManagerConfirmed(self, state=None):
        ## **** This functionality should get moved into the hotkey
        ##      module itself
        self.ini.setItem("enable_hotkeys", "1")
        self.mmmm.hotkeys.startHotkeys()
        #self.ini.fileWrite()
        self.ini.setFileByItems()
        try:
            cmds.deleteUI( self.activateHotkeyManagerWindow )
        except:
            traceback.print_exc()
    
    def popupWindowAbout(self):
        print(self.conf.aboutString)
        
        
        cmds.window( title="About MmmmTools", iconName='About', width=500, height = 340 )
        cmds.columnLayout( adjustableColumn=True )
        #cmds.text( label='self.conf.aboutString' )
        #cmds.text( label='Left', align='left' )
        cmds.text( label=' ', align='center' )
        cmds.text( label=self.conf.aboutString, align='center' )
        cmds.text( label='MMMM Makes Maya Marvelous', align='center' )

        cmds.text( label=' ', align='center' )

        cmds.text( label='Please contact Joe Crawford for information.', align='center' )
        cmds.text( label='mmmmtools@celestinestudios.com', align='center' )
        
        cmds.text( label=' ', align='center' )
        
        cmds.text( label='See our website at:', align='center' )
        cmds.text( label='http://celestinestudios.com/mmmmtools', align='center' )
        
        cmds.text( label=' ', align='center' )
        
        cmds.text( label="""Original MmmmTools Code is Licensed Under The GNU GPL version 3 or later.
        
        Contributions to MmmmTools:
        Joint Orient Helper - Originally created by Marina Lucio, maintained by Joe Crawford
        Some "Modeler" tools originally written by David Kenley, maintained by Joe Crawford
        Mr Clean functions written by Braden Wade in addition to Joe Crawford
        
        Other included software is not part of MmmmTools but used under the GPL license:
        Open Maya Toolbox - http://jakob.welner.dk/omtwiki/index.php/Main_Page
        RoadKill - http://www.pullin-shapes.co.uk/page8.htm
        AutoHotkey - http://www.autohotkey.com
        """, align='center' )        
        
        cmds.showWindow()