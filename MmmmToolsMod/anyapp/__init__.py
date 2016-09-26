"""
anyapp


this is the modules init file


Eventually it is intended that this project will be released under GPL, LGPL,
dual licensed either v2 or v3 at the users options
GPL text should eventually go here

main module
"""

from __future__ import absolute_import

## Get a reference to this running module
## (this needs sys so we import it)
import sys as Sys
Mod_self = Sys.modules[__name__]

## Import other standard modules
import time as Mod_time
import threading as Mod_threading
import subprocess as Mod_subprocess
import os as Os
import traceback as Mod_traceback

## Import 3rd party modules, from system locations only
##    imports of PySide are guarded so that the app
##    can run without ui mode is PySide isn't available
try:
    import PySide.QtGui as QtGui
except:
    QtGui = None
    print(  Mod_traceback.format_exc()  )
try:
    import PySide.QtCore as QtCore
except:
    QtCore = None
    print(  Mod_traceback.format_exc()  )    
    
    

## Import anyapp components
##    these are parts of this package itself
from . import app_base as Mod_app_base
from . import utils as Mod_utils
from . import object_base as Mod_object_base
from . import climan as Mod_climan

## Setup module wide variables for important
##   parts of the modules
App_base = Mod_app_base.App_base
App_base_ui = Mod_app_base.App_base_ui
Object_base = Mod_object_base.Object_base
Utils = Mod_utils.Utils
Pather = Mod_utils.Pather
Climan = Mod_climan.Climan




##   End of module code!  Everything else that matters is done in the sub-modules!
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################






#################
## Obsolete code that may be repurposed in the future
##   This section using mods was removed until mods can handle relative imports better!
"""
                ## Setup a system to simplify use of other modules
                from . import mods as Mod_mods
                print(  dir(Mod_mods)  )
                Impinst = Mod_mods.Importer()
                Impinst.put_mods_to_object( 
                    Mod_self,
                    put_mods_dict_to_object=True,
                    names=[
                        ## Here's where we specify which modules will be setup!
                        'os','sys','random','time','traceback','anyapp.api_helper'
                    ]
                )
"""
############






##########################
## Notes
"""
Notes:


to do list:

  Make the app base get a bunch of info about the system that its running on,
  and paths with the pather class etc

  Organize the sequence of events better for creating a gui, and in particular,
  using the QMainWindow class, which is quite useful.
  
  Use the gridLayout by default.  It's fucking awesome and can easily
  do everything the Box layout can
 



"""

