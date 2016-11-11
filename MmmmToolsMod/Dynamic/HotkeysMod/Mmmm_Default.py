def getEntries():
    namedCommands = []

    """
    Define the set of default hotkeys.  These hotkeys are actually used in the other sets as well.
    """
    
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
    
    return namedCommands