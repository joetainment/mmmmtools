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
import traceback, sys, collections
## Imports from Maya
import pymel.all as pm
import maya.cmds as cmds

## Imports from MmmmTools
import UtilsMod  #relative in same folder

#### Dynamic Modules Import ################
############################################
## Make a list of which MmmmTools modules will be imported, they will be imported by string name
## The order of modules in this list is important
## All these modules are *relatively pathed*
mmmm_modules_to_import =[    
    'PlatformManager', ## 1st - make sure paths are calculated 
    'Configuration',  ## 2nd - configuration and ini file    
    'Env',  ## 3rd - helps platform manager using ini info 
    'Commander',
    
    'Rigger',
    'Modeler',
    'Selector',
    'Texturer',
    'Renderer',
    'Gamer',
    'Scripter',
    'Viewer',
    
    'Ui', 
    'Hotstrings',
    'Hotkeys',
    'RimLight',
    'Renamer',
    'SelectTextureBorderEdges',
    'AutosaveEnabler',

    'SelectTextureBorderEdges',
    'FileTextureReloader',
    'HotBoxToggler',
    'DesignFileLoader',
    'Downloader',
    ####'Threads',
    #'CapsDisabler', 
]
importCode = """
try:
    reload(*module*)
except:
    try:
        import *module*
    except:
        print( traceback.format_exc() )
"""
for m in mmmm_modules_to_import:
    exec( importCode.replace('*module*', m ) , globals(), locals() )
#### End of Dynamic Modules Import #############################
################################################################
    
    
    UtilsMod.Utils.log( 'MmmmtoolsMod module about to initialize.' )






#### Anyapp Imports #########################
#############################################
#### Note, this is currently disabled
#### until proper 2017 support can be added back in.
# """
# try:
    # try:
        # import PySide.QtCore as Mod_QtCore
        # import PySide.QtGui as Mod_QtGui    
    # except:
        # import PySide2.QtCore as Mod_QtCore
        # import PySide2.QtGui as Mod_QtGui    
    
    # try:
        # import MmmmToolsMod.anyapp
        # Mod_anyapp = MmmmToolsMod.anyapp
        # Object_base = Mod_anyapp.Mod_object_base.Object_base
    
        # class MmmmAnyapp(Mod_anyapp.Mod_app_base.App_base):
            # def __init__(self,*args,**kargs):
                # kargs = self.set_kargs_defaults( kargs, [
                    # [ 'created_through_MmmmTools', True ],
                    # [ 'ui_class', MmmmAnyappUi ],
                # ])    
                # Mod_anyapp.Mod_object_base.Object_base.init_bases(self, *args, **kargs)    
        # class MmmmAnyappUi(Mod_anyapp.Mod_app_base.App_base_ui):
            # def __init__(self,*args,**kargs):
                # kargs = self.set_kargs_defaults( kargs, [
                    # [ 'created_through_MmmmTools', True ],
                    # [ 'ui_parent_window', UtilsMod.UiUtils.getMayaWindowAsWrappedInstance() ],
                # ])    
                # Mod_anyapp.Mod_object_base.Object_base.init_bases(self, *args, **kargs)    
    # except:
        # print(  traceback.format_exc()  )
    
# except:
    # pass   ## unfortunately, there's nothing we can do if PySide isn't available
# """
#### End of Anyapp Imports #########################
####################################################
    


    
    

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
        self.u = UtilsMod.Utils
        self.utils = self.u
        self.uiUtils = UtilsMod.UiUtils
        self.designFileLoader = DesignFileLoader
        self.prompt = UtilsMod.UiUtils.prompt  ## comes from imported module
                ## Initialize all the different sub systems of the MmmmTools instance        self.platformManager = PlatformManager.PlatformManager(self)        self.configuration = Configuration.Configuration(self)        self.env = Env.Env(self)
        
        self.commander = Commander.Commander(self)
        
        
        self.ui = Ui.Ui(self)
        self.hotstrings = Hotstrings.Hotstrings(self)
        self.hotkeys = Hotkeys.Hotkeys(self)        self.selector = Selector.Selector(self)        self.rigger = Rigger.Rigger(self)
        self.modeler = Modeler.Modeler(self)
        self.texturer = Texturer.Texturer(self)
        self.renderer = Renderer.Renderer(self)
        self.scripter = Scripter.Scripter(self)        self.gamer = Gamer.Gamer(self)        self.viewer = Viewer.Viewer(self)
        
        self.downloader = Downloader.Downloader(self)
        self.rimLight = RimLight.RimLight(self)
        self.renamer = Renamer.Renamer(self)
        
        self.fileTextureReloader = FileTextureReloader.FileTextureReloader(self)
        self.hotboxToggler = HotBoxToggler.HotBoxToggler(self)
        self.selectTextureBorderEdges = SelectTextureBorderEdges.SelectTextureBorderEdges(self)
        self.autosaveEnabler = AutosaveEnabler.AutosaveEnabler(self)
        
        try:
            self.hotkeys.go()
        except:
            self.u.log( "Hotkeys could no be started." )
        
        
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
        
def GetInstance():    ## MmmmTools is the class defined in this module    return MmmmTools.mmmmToolsInstance
            
UtilsMod.Utils.log( 'Mmmmtools module initialization complete.' )

