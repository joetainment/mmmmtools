def getEntries():

    namedCommands = []

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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCutUvs'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        polyPerformAction polyMapCut e 0;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate 

    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCutUvsAlternate'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'k'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        polyPerformAction polyMapCut e 0;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmSewUvs'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        polyPerformAction polyMapSew e 0;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate    
    
            
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCalcAndStoreUvSizing'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        python("mmmmTools.texturer.grabUvToWorldRatioOfSelection();")
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate     

    
    
    
    
    
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmApplyStoredUvSizing'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
        python("mmmmTools.texturer.applyGrabbedUvToWorldRatioToSelection();")
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmApplyNumericalUvSizing'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'
    nameCommand['ctl'] = True
    nameCommand['alt'] = True
    nameCommand['mel'] = """
        python("mmmmTools.texturer.applyNumericalUvToWorldRatioToSelection();")
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
    
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmApplyStoredUvSizingAlternate'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'i'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
        python("mmmmTools.texturer.applyGrabbedUvToWorldRatioToSelection();")
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate

    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCalcAndStoreUvSizingAlternate'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'i'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        python("mmmmTools.texturer.grabUvToWorldRatioOfSelection();")
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate          
    
    

    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmUnfoldLegacy'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "u"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                unfold -i 5000 -ss 0.001 -gb 0.5 -gmb 0.5 -pub 0 -ps  0 -oa  0 -us off;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmUnfold'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'u'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python("mmmmTools.texturer.unfold3dOnlySelected()");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmUnfoldMultipleObjects'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'U'
    nameCommand['ctl'] = True
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python("mmmmTools.texturer.unfold3dMultipleObjects()");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
                    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmUnfold'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'u'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python("mmmmTools.texturer.unfold3dOnlySelected()");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmLayoutWithoutScale'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'l'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
       polyMultiLayoutUV -lm 0 -sc 0 -rbf 2 -fr 1 -ps 0.2 -l 3 -gu 1 -gv 1 -psc 0 -su 1 -sv 1 -ou 0 -ov 0;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
     
     
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmLayoutWorldPrescale'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'L'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
       polyMultiLayoutUV -lm 0 -sc 1 -rbf 2 -fr 1 -ps 0.2 -l 2 -gu 1 -gv 1 -psc 2 -su 1 -sv 1 -ou 0 -ov 0;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
             
             
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmLayoutNoPrescale'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'l'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
       polyMultiLayoutUV -lm 0 -sc 1 -rbf 2 -fr 1 -ps 0.2 -l 2 -gu 1 -gv 1 -psc 0 -su 1 -sv 1 -ou 0 -ov 0;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate


    return namedCommands