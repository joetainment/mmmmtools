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




## This __init__.py files needs to exist in order for python to recognize that this is a module.  It is also run as soon as the module is imported.

## This string is for Python Documentation, but is very incomplete.
"""
MmmmTools - Usability Improvements for Maya

See the module __init__.py source code files, which includes
notes on the conventions used in MmmmTools.

#### Notes ###

Conventions used:

    indentation with space, 4 spaces per tab (python standard)

    
    several short variable names are commonly used for the same thing
    often shortcuts are created locally, for example:
    u is used for utils (very simple common functions in Utils)
        u.log("log this")
    U is also for utils
        U should only be used as a module wide thing.
        this is actually better and more accurate since U is a class
        and thus should be uppercase. Most code using 'u' should become 'U'.
        If its a member, use u, when it's module wide, use U
    objs for simple obj lists
        for obj in objs:
    obj for object, usually from objs list
        for obj in objs:
    i,j,i1,i2,j1,j2 for numerical iterators
        for i in range(10):    
    v for values
        for v in listOfValues
    k for keys
        for k,v in dictOfItems.items():
    s for self
        s = self
        This is often used in functions to shorten the code

    d for data, usually a dictionary
    
    
    

    
    upper camel case
        modules, classes, static methods and members
    lower camel case or lower case with underlines
        local variable and instance members and methods 

    We try to use camelCase because that's how Maya works by default, even though Python often uses
    underscores instead.    
    
     
    UI conventions:
    UI should be written as a separate class that would be used as a member of the main class.
    argument named auto_ui to tell a class whether or not to automatically start the ui
    if auto_ui is true, the class automatically runs the go_ui function
    function named go_ui that starts the ui
     
        
    Longer, descriptive names are used non locally, but often short names are used locally
        This makes the code way easier to type and read.
        Generally, when a short "local" variable is used, if will be defined just a little bit earlier
        (except for u, which is the Utils class that is used so often it has a standard short variable name

    The main class from most modules is named the same as the module itself
        Use of an example module and an example class would be as follows:
            from Example import Example
            example = Example()
    
    
    The maya conventions are used for the Maya modules:
        import maya.cmds as cmds
        import pymel.all as pm
        
        This is done even though it is inconsistent because it's important to
        remain consistent with standard documentation for maya and pymel
        
    Try to split complex statements (lines) up into a series of simpler
    statements to make them easier to follow.
    This is usually preferred unless a single line
    is actually easier to understand and follow

    Comments are often added to explain the syntax and usage so that
    beginners can look at the code and understand it quickly.
    MmmmTools is intended to teach students by example.
    
    
    Commonly used classes:
    
        Duck, a simple class inheriting from Object
        Object, a simple class inheriting from object
            object does allow setattr so even if you add no members or methods
            it is useful to derive a class from it, such as Object or Duck

To Do - Roadmap and Planning:

    Grid tools:
      Snap to grid in x
      Snap to grid in y
      Snap to grid in z

    Hotkeys
       Pivot Fixer Hotkey
       Pivot To Components Hotkey
       Cursor functions
         Cursor to component/selection hotkey
         Cursor to object
         Cursor to grid
         Cursor to pivot
         
         Selection To Cursor
         Pivot to cursor
         
       Move pivot to cursor
       
    Organizer
      Script to set project to pasted path (replace backslashes if necessary)
      Script to       
       

    GenericScriptable python node
    Programmable node - node with properties to hold a string contains
        code which runs on each callback (one string property per callback)
        This essentially creates the most flexible node possible and allows
        the contents to be stored in the scene itself
        
        
        

    Notes Manager - Use annotation objects for notes
    
    Expression Manager - Run expressions via python

    Set project by path from clipboard, or by entered text
        perhaps text box can be filled with clipboard text
        automatically

    Renamer - Write custom object renamer, with support for regular
              expressions
                Prefix
                Suffix
                Numbering
                Padding
                
              
    Selector - Write Selector tools
                Filter selection would select subsets of components
                    lights, cameras, geo,  etc
                Select shapes from selection (add to, subtract, replace)
                Select by name, with wildcard and regular expression support
                Shows quick select sets, add ability to select them and modify
                   current selection by add, subtract, replace
                Conditional selection
                    property   operator   number

    Create physically accurate rendering
        A tool to automatically setup Mental ray to give accurate renders
        
    UDK export tools
                    
    Write custom connect components that selects the new components!
    Quick select sets seem to be able to remember the old components
    so just make a quickselect set of the old components
    then select every new components that isn't in that quick select set.
    Then OpenMayToolbox connect won't be as important.
    
    Cleanup hotkeys code involving file paths and copying/moving
    
    Rewrite roadkill launcher using popen
    
    SelectTextureBorderEdges has old style code (maya.cmds etc)
        modernize it to use pymel and new Utils
            
"""


## Imports from Python Standard Library
import traceback as traceback
import sys

## Imports from Maya
import pymel.all as pm
import maya.cmds as cmds

## Imports from MmmmTools
import unipath


## The next part is a work around to a super annoying Maya python bug
## because the second time it runs, it imports differently...
try:
    try:
        reload( sys.modules['MmmmTools.Utils'] )
    except:
        pass
    ModUtils = sys.modules['MmmmTools.Utils']
except:
    from . import Utils as ModUtils
Utils = ModUtils.Utils
UiUtils = ModUtils.UiUtils
    


Pather = ModUtils.Pather

## Setup shortcut variables
u = U = Utils



u.log( 'Mmmmtools module about to initialize.' )

try:
    import MmmmBaker
except:
    print( format_exc() )


from collections import OrderedDict

try:
    import PySide.QtCore as Mod_QtCore
    import PySide.QtGui as Mod_QtGui    
    try:
        import MmmmTools.anyapp
        Mod_anyapp = MmmmTools.anyapp
        Object_base = Mod_anyapp.Mod_object_base.Object_base
    
        class MmmmAnyapp(Mod_anyapp.Mod_app_base.App_base):
            def __init__(self,*args,**kargs):
                kargs = self.set_kargs_defaults( kargs, [
                    [ 'created_through_MmmmTools', True ],
                    [ 'ui_class', MmmmAnyappUi ],
                ])    
                Mod_anyapp.Mod_object_base.Object_base.init_bases(self, *args, **kargs)    
        class MmmmAnyappUi(Mod_anyapp.Mod_app_base.App_base_ui):
            def __init__(self,*args,**kargs):
                kargs = self.set_kargs_defaults( kargs, [
                    [ 'created_through_MmmmTools', True ],
                    [ 'ui_parent_window', UiUtils.getMayaWindowAsWrappedInstance() ],
                ])    
                Mod_anyapp.Mod_object_base.Object_base.init_bases(self, *args, **kargs)    
    except:
        print(  traceback.format_exc()  )
    
except:
    pass   ## unfortunately, there's nothing we can do if PySide isn't available


    

    
    

## Make a list of which MmmmTools modules will be imported, they will be imported by string name
## The order of modules in this list is important
mmmm_modules_to_import =[
    'PlatformManager', ## 1st - make sure paths are calculated 
    'Configuration',  ## 2nd - configuration and ini file    
    'Env',  ## 3rd - helps platform manager using ini info    
    'Hotstrings',
    'Ui',
    'Downloader',   
    'Hotkeys',
    'RimLight',
    'Renamer',
    'SelectTextureBorderEdges',
    'AutosaveEnabler',
    'Downloader',
    'Rigger',
    'Modeler',
    'Texturer',
    'Renderer',
    'Gamer',
    'SelectTextureBorderEdges',
    'FileTextureReloader',
    'HotBoxToggler',
    #'Threads',
    'CapsDisabler',
    'Scripter',
    'Selector',
    'Renamer',
    'DesignFileLoader',
]



## Import modules dynamically.
## This ensures that exceptions are nicely handled,
## and also ensures that we can easily reload
## modules and see any errors given as tracebacks.
for m in mmmm_modules_to_import:
    ## If we already have the module reload it, showing the traceback if it fails
    if m in globals():
        try:
            reload( globals()[m] )  ## This reloads an already loaded module
        except:
            u.log( "Could not reload module: ", m  )
    else:
        try:
            ## import the module by name, and get the same named class from the module
            ## same as:  from MmmmTools.Example import Example
            mod =__import__('MmmmTools.' + m) ##  Get the MmmmTools module that matches the name m
            cls = getattr( mod  , m   )   ##  Get the same named class from the module
            globals()[m] = cls
        except:
            u.log( "Could not reload module: ", m )
            print( traceback.format_exc() )


####################
## Classes
####################


class MmmmTools(object):
    mmmmToolsInstance = None
    """
    MmmmTools Main class.
    When one of these is created, mmmmTools starts running.
    You can also call it in many ways after its been created.
    """
    @property
    def ini(self):  #self.ini will just be used as a shortcut
        return self.configuration
    @property
    def conf(self):  #self.ini will just be used as a shortcut
        return self.configuration.conf
    
    def __init__(self):
        """
        Setup the actual instance of the MmmmTools class
        Create instances of all the main parts of
        MmmmTools
        
        Examples:
        
        PlatformManager will give us all the 
           information we need about the OS, computer, etc
         Configuration contains all ini based and most hardcoded
           settings and paths etc, and also the ini file information
         Env is similar to the platform manager, and assists it
           but env depends on self.configuration
        """
        
        MmmmTools.mmmmToolsInstance = self
        self.u = u
        self.utils = u
        self.uiUtils = UiUtils
        self.designFileLoader = DesignFileLoader
        self.prompt = UiUtils.prompt  ## comes from imported module
        
        ## we will instantiate all these classes!
        ##     self attr name         class to instantiate
        classesToInstantiate = [
            ('platformManager',       PlatformManager.PlatformManager),
            ('configuration',         Configuration.Configuration),
            ('env',                   Env.Env),
            ('ui',                    Ui.Ui),
            ('downloader',            Downloader.Downloader),
            ('hotstrings',            Hotstrings.Hotstrings),
            ('hotkeys',               Hotkeys.Hotkeys),
            ('rimLight',              RimLight.RimLight),
            ('renamer',               Renamer.Renamer),
            ('rigger',                Rigger.Rigger),
            ('gamer',                 Gamer.Gamer),
            ('modeler',               Modeler.Modeler),
            ('texturer',              Texturer.Texturer),
            ('renderer',              Renderer.Renderer),
            ('hotboxToggler',         HotBoxToggler.HotBoxToggler),
            ('capsDisabler',          CapsDisabler.CapsDisabler),
            ('selectTextureBorderEdges',
                SelectTextureBorderEdges.SelectTextureBorderEdges),
            ('fileTextureReloader', FileTextureReloader.FileTextureReloader),
            ('autosaveEnabler',  AutosaveEnabler.AutosaveEnabler),
            ('scripter', Scripter.Scripter),
            ('selector', Selector.Selector),
        ]
        
        ## For each attribute name  paired with the class, instantiate it
        ## and attach it to self using setattr
        ## log errors
        for v in classesToInstantiate:
            attr = v[0]  ## attribute name string
            cls = v[1]  ## class
            ## **** make this into a more general purpose function!
            try:
                try:
                    try:
                        it = cls(self) ## instance
                    except:
                        u.log(
                          "Class couldn't be instantiated with "
                          "parent ref. About to try without parent ref.")
                        assert 0==1
                except:
                    it = cls() ## instance with no parent ref
            except:
                it = None
                u.log( "MmmmTools could not initialize: " + str( cls ) )
            setattr( self, attr, it )
        
        
        try:
            self.hotkeys.go()
        except:
            u.log( "Hotkeys could no be started." )
        
        
    def getInput( self, message="Enter Input", title="Enter Input" ):
        result = cmds.promptDialog(
                        title=title,
                        message=message,
                        button=['OK', 'Cancel'],
                        defaultButton='OK',
                        cancelButton='Cancel',
                        dismissString='Cancel')
        try:
            text = cmds.promptDialog(query=True, text=True)
        except e:
            text = ''
            
        return text            
    
    def loadPluginsByIni(self):
        try:
            if int(  self.ini.getItem("load_plugin_mayatomr")  ) == 1:
                cmds.loadPlugin('Mayatomr')
        except:
            print('Mental Ray for Maya was either already loaded or cannot be loaded.')
        try:
            if int(  self.ini.getItem("load_plugin_objexport")  ) == 1:
                cmds.loadPlugin('objExport')
        except:
            print('ObjExport plugin was either already loaded or cannot be loaded.')
    
    def mprint( msg=None, mode='print' ):
        if mode=='print':
            try:
                print( msg )  ##
            except e:
                print( e )
        else:
            print( 'Other modes are not yet supported for mprint.')
            
    def mmmmBaker( self ):
        m = MmmmBaker.MmmmBakerUi()
        
def GetInstance():    return MmmmTools.mmmmToolsInstance
            
u.log( 'Mmmmtools module initialization complete.' )

