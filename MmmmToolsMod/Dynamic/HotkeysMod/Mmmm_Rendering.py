def getEntries():
    namedCommands = []

    #Home, End,  9, semicolon are free
    #Pageup, PageDown are good to use in this mode too


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmShowHypershadeWindow'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'm'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        HypershadeWindow;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCreateAndAssignBlinn'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '0'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        createAndAssignShader blinn "";
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCreateAndAssignBlinn2'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'n'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        createAndAssignShader blinn "";
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate



    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmCreateAndAssignBlinn2'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'p'
    nameCommand['ctl'] = True
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        python(  "mmmmTools.utils.hyperGraphAsActivePanelShowShapesToggle()"  );
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate




    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmGraphMaterialsOnSelectedObjects'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = ','
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "graphMaterials");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmAddSelectedToGraph'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '.'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "addSelected");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmRemoveSelectedFromGraph'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '.'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "removeSelected");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmRearrangeGraph'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = 'm'
    nameCommand['ctl'] = False
    nameCommand['alt'] = True
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "rearrangeGraph");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmShowUpAndDownstream'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate


    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmShowUpstream'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = '/'
    nameCommand['ctl'] = True
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "showUpstream");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmShowDownstream'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "?"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        hyperShadePanelGraphCommand("hyperShadePanel1", "showDownstream");
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmToggleClearBeforeGraphing'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = ";"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                        optionVar -intValue hsClearBeforeGraphing `menuItem -query -checkBox hyperShadePanel1Window|TearOffPane|hyperShadePanel1|hyperShadePanelMenuOptionsMenu|clearBeforeItem`;

                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmMakeLightLinks'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "h"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                            lightlink -make -useActiveLights -useActiveObjects;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmBreakLightLinks'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "j"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
    lightlink -break -useActiveLights -useActiveObjects;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmIPR'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "i"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                            RenderViewWindow;
                            catchQuiet( `renderWindowMenuCommand keepImageInRenderView renderView` );
                            IPRRenderIntoNewWindow;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmRender'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "9"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                            RenderViewWindow;
                            catchQuiet( `renderWindowMenuCommand keepImageInRenderView renderView` );
                            RenderIntoNewWindow;
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    #This section is meant to be duplicated and altered #
    #Edit the name, key and mel parts#
    nameCommand = {}
    nameCommand['name'] = 'mmmmGetSelectionByMaterial'
    nameCommand['annotation'] = nameCommand['name'] #Automatically makes it the same as the name to save customizing time.
    nameCommand['key'] = "'"
    nameCommand['ctl'] = False
    nameCommand['alt'] = False
    nameCommand['mel'] = """
                            hyperShade -objects `ls -sl`; 
                        """
    namedCommands.append(nameCommand)
    #End of section to duplicate
    
    
    
    return namedCommands