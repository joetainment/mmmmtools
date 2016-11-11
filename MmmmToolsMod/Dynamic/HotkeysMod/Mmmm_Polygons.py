def getEntries():


















    namedCommands = []





    

        
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
          
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmOrthographicToggle'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '@'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """python(  "mmmmTools.u.camOrthoToggle()"  );"""
    namedCommands.append(nameCommand)       















    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCycleManipXformConstraint'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '`'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python("MmmmToolsMod.Static.Manipulators.cycleManipXformConstraint()");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
                     
                                          
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCycleSelectByFaceCenters'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '~'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python("MmmmToolsMod.Static.Manipulators.cycleSelectByFaceCenters()");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
                     
                     
                     
                     
                     
                     
                     
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    

    nameCommand = {}
    nameCommand['name'] = 'mmmmConnectComponents'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'k'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        ConnectComponents;
                        // qnexOpt -e manipType connect;
                        //// used to be: 
                        """
    namedCommands.append(nameCommand)

    
    




    nameCommand = {}
    nameCommand['name'] = 'mmmmInsertEdgeLoopTool'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'k'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    
    nameCommand['mel'] = """
                        SplitEdgeRingTool;
                        """
    namedCommands.append(nameCommand)
    

    



    nameCommand = {}
    nameCommand['name'] = 'mmmmConnectAndSelectEdges'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'K'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        polySplitRing -ch on -splitType 1 -weight 0.5 -smoothingAngle 180;
                        ////  need to implement mmmmConnectAndSelectEdges
                        """
    namedCommands.append(nameCommand)



    
    
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
    nameCommand['name'] = 'mmmmVolumeSelectVerts'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'L'
    nameCommand['mel'] = """
                        python( "mmmmTools.selector.volumeSelect()" );
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #Release!
    nameCommand = {}
    nameCommand['doRelease'] = True
    nameCommand['name'] = 'mmmmExtrude'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'm'
    nameCommand['mel'] = """
                        print " ";
                        """
    namedCommands.append(nameCommand)
    


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCollapse'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['mel'] = """
                        polyCollapseEdge;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate

    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmReverseNormals'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['alt'] = True        
    nameCommand['mel'] = """
                        ReversePolygonNormals;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmConformNormals'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'N'
    nameCommand['alt'] = True        
    nameCommand['mel'] = """
                        ConformPolygonNormals;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate

    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmUnlockNormals'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['alt'] = True
    nameCommand['ctl'] = True        
    nameCommand['mel'] = """
                        polyNormalPerVertex -ufn true;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmToggleShowVertexNormals'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'N'
    nameCommand['alt'] = True
    nameCommand['ctl'] = True        
    nameCommand['mel'] = """
                        ToggleVertexNormalDisplay;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmToggleShowFaceNormals'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'N'
    nameCommand['ctl'] = True        
    nameCommand['mel'] = """
                        ToggleFaceNormalDisplay;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmRetoperProject'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'o'  # didn't use unmodified one because it is a useful marking menu
    nameCommand['alt'] = True
    nameCommand['mel'] = """
        python( "MmmmToolsMod.Dynamic.Modeler.ModelerRetoper.ModelerRetoper.getInstance().projectSelection()" );
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmRetoperSetReference'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'O'  # didn't use unmodified one because it is a useful marking menu
    nameCommand['alt'] = True
    nameCommand['mel'] = """
        python( "MmmmToolsMod.Dynamic.Modeler.ModelerRetoper.ModelerRetoper.getInstance().setReference()" );
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmQuadDraw'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'p'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False        
    nameCommand['mel'] = """
                            dR_quadDrawTool;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate        

    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmSculptGeometryTool'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'U' # regular u is the sculpt marking menu
    nameCommand['mel'] = """
                        SculptGeometryTool;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmLocalTools'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '8'
    nameCommand['mel'] = """
                        catchQuiet(  HKLTOptionBox()  );
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmHKLocalToolsTakeReference'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '9'
    nameCommand['mel'] = """
                        HKLocalToolsAction();
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmExtract'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = ')'
    nameCommand['mel'] = """
                        ExtractFace;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCombine'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '0'
    nameCommand['mel'] = """
                        CombinePolygons;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmDeleteEdgeAndVertex'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '='
    nameCommand['mel'] = """
                        performPolyDeleteElements;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate    


    #This section is meant to be duplicated and altered. Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmHarden'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = ';'
    nameCommand['mel'] = """
                        SoftPolyEdgeElements 0;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmBridgeEdge'
    nameCommand['annotation'] = nameCommand['name']
    #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = ','
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        BridgeEdge;
                        """
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
    #End of section to duplicate
    

    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmMultiCut'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'       
    nameCommand['mel'] = """
                        dR_multiCutTool;
                        """               
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
    namedCommands.append(nameCommand)
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
        python(  "MmmmToolsMod.Dynamic.Modeler.ModelerGridTools.ModelerGridTools.grow(log=True, setManip=True)"  );
                        """
                        
    namedCommands.append(nameCommand)
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
            python(  "MmmmToolsMod.Dynamic.Modeler.ModelerGridTools.ModelerGridTools.shrink(log=True, setManip=True)"  );
                        """
    namedCommands.append(nameCommand)
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
            python(  "MmmmToolsMod.Dynamic.Modeler.ModelerGridTools.ModelerGridTools.putSelectedVertsOnGrid()"  );
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
            
            
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmGridSnapSelectedObjs'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '['
    nameCommand['ctl'] = True
    nameCommand['alt'] = True
    nameCommand['mel'] = """
            python(  "MmmmToolsMod.Dynamic.Modeler.ModelerGridTools.ModelerGridTools.putSelectedObjsOnGrid()"  );
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate        
    
    
    return namedCommands