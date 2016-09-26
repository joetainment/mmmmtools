## This example shows how to create a basic class using MmmmTools in Maya
##
##   The example will create a window in Maya will a couple buttons to perform basic functions.
##
##   Normally it is better to use two custom classes, one for the feature functions
##   and other for the ui.  That improved method is shown in the another example


from collections import OrderedDict
import pymel.all as pm
import PySide.QtGui as QtGui
import MmmmTools




## Create our Anyapp class
##   If running in Maya, this Anyapp will be sort of a sub-app to Maya
##   If not running in Maya, this Anyapp will form its own application.
##   Our own class is based on the Anyapp App_base class
class YourAnyappInMaya(MmmmTools.MmmmAnyapp):
    def __init__(self,*args,**kargs):
        ## Setting up default options for keyword arguments
        ##   Instead of setting the argument defaults in the arguments to init, 
        ##   we set them using the self.set_kargs_defaults function and passing 
        ##   it kargs so that new defaults can be added to kargs.
        ##   The pattern is really easy to follow and add lots of flexibility to
        ##   the system note that superclass options can be
        ##   overridden by passing keyword args to our class.
        ##
        ##   The next line and its indented section illustrates this pattern:        
        kargs = self.set_kargs_defaults( kargs, [
            [ 'ui_title', 'Your Window Title' ],
            [ 'ui_width',  350 ],
        ])
        
        ## An easy way to add a bunch of widgets to our UI
        ## just put them in a dict and add that dict to kargs
        ## as ui_widgets.  Annyapp looks for this later!
        ## By using OrderedDict, we make sure they stay in the
        ## vertical order on screen        
        your_ui_widgets = OrderedDict()
        your_ui_widgets['cubeButton'] = QtGui.QPushButton( 'Make a cube!' )
        your_ui_widgets['cubeButton'].clicked.connect(
            lambda: self.makeCube()
        )
        your_ui_widgets['sphereButton'] = QtGui.QPushButton( 'Make a sphere!' )
        your_ui_widgets['sphereButton'].clicked.connect(
            lambda: self.makeSphere()
        )
        kargs['ui_widgets'] = your_ui_widgets
        
        ## This initializes all the Anyapp super classes,
        ## which takes the options in kargs and applies them
        ## if make_ui has been set True in kargs
        ## it will now create the default ui
        ## and populate it with ui_widgets
        ## if ui_widgets are found in kargs
        MmmmTools.Object_base.init_bases(self, *args, **kargs)

        
    def makeCube(self):
        pm.polyCube()
        
    def makeSphere(self):
        pm.polySphere()
        

app = YourAnyappInMaya( make_default_ui=True )

pass