from __future__ import absolute_import

## Get a reference to this running module
## (this needs sys so we import it)
import sys as Mod_sys
Mod_self = Mod_sys.modules[__name__]

## Import standard modules    
import time as Mod_time
import threading as Mod_threading
import traceback as Mod_traceback
import subprocess as Mod_subprocess
import os as Mod_os

from collections import OrderedDict



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
from . import utils as Mod_utils
Utils = Mod_utils.Utils
from . import object_base as Mod_object_base
Object_base = Mod_object_base.Object_base
        
class App_base(Object_base):
    def __init__(self, *args, **kargs):
        #print( 'Any_app_base __init__ running!!!' )        
        kargs = self.set_kargs_defaults( kargs, [
            [ 'ui',True ],
            [ 'print_to_console',True ],
            [ 'print_to_console_even_with_ui',False ],
            [ 'init_bases',True ],
            [ 'ui_class', App_base_ui ]
        ])
        Object_base.init_bases(self, *args, **kargs)
        
        #print( self.__class__.__mro__ )

        ##super( self.__class__, self ).__init__(*args, **kargs)
        ##super(type(self)).__init__(*args, **kargs)

        if self.opts['debug'] == True: print( kargs['ui'] )
        self.opts_merge( kargs )
        self.ui_class = kargs[ 'ui_class' ]
        
        ##if self.__class__.__name__ == 'App_base': self.init_bases( self )
        
        self.init_ui_base()
        self.init_env()
        
      
        
    def get_karg( self, karg, kargs ):
        if karg in kargs:
            return kargs[karg]
        else:
            return None
    def get_attr( self, attr ):
        try:
            return getattr( self, attr )
        except:
            return None
        

    def deleteme(self):
        s.init_env()
        s.dynamic_classes = {}
        s.output( "##Output" )
        
        #self.opt_check( 'ui', on_true=self.init_ui )
    
    def go(self):
        if self.opts.get('ui', False):
            self.go_ui()
        else:
            self.go_no_ui()

    def go_no_ui(self):
        ## This should run even when debugging is off, so it just uses print
        self.debug( "This app does nothing useful when ui is not enabled." )
    
    def go_ui(self):
        #print( 'go_ui is running!' )
        try:
            self.ui.go()
        except:
            ## This should run even when debugging is off, so it just uses print
            self.debug( "No GUI available. This app does nothing useful when ui is not enabled." )
        
    
    def init_ui_base(self,  *args, **kargs):
        #### This should probably by overwritten by the using class
        self.init_ui()
            
    def init_ui(self, *args, **kargs):
            make_default_ui = self.opts.get( 'make_default_ui', False )
            try:
                self.ui
            except:
                self.ui = self.ui_class( self, *args, **self.opts )
            
            
    
    def init_opts(  self ):
        pass
    
        

        
    def opt_check(self, opt, on_true=None, on_false=None, default_value=None):
        s = self
        o = str(opt)
        if o in s.opts:
            ov = s.opts[o]
            if ov:
                if on_true!=None:
                    on_true.call()
            else:
                if on_false!=None:
                    on_false.call()
        else:
            if default_value:
                s.opts[o] = default_value
    def opt_get(self, opt):
        s = self
        o = str(opt)
        if o in s.opts:
            return o
        else:
            return None

        
        
    def output(self, out):
        try:
            self.ui.output( out )
            #### The next lines aren't working...  **** Fix this ****
            #if opt.get('print_to_console_even_with_ui'):
            #    print(out)
        except:
            if self.opts.get('print_to_console'):
                #print(out)
                pass
       
    def make_class(self, class_name, base_classes=(object,), methods_and_members=dict()  ):
        x = type( str(class_name), base_classes, methods_and_members )
        self.dynamic_classes[class_name] = x
        return x
        
        
     

            
class App_base_ui(Object_base):
    ## We use the names formLayout and mainWindow because
    ## that is what Qt tends to call things by default
    @property
    def mainWindow(self):
        return self.widgets.get('mainWindow', None)
        
    @property
    def mainLayout(self):
        return self.widgets.get('mainLayout', None)
        
    @property
    def formLayout(self):
        return self.widgets.get('formLayout', None)

        
        

    def __init__(self, parentRef, make_default_ui=False, *args, **kargs):
        kargs = self.set_kargs_defaults( kargs, [
            [ 'ui_parent_window', None],        
            [ 'ui_title', 'AnyApp' ],
            [ 'ui_widgets' , None ],
            [ 'ui_width', None ],
            [ 'ui_height', None ],
            [ 'ui_dict', None ],
        ])
        Object_base.init_bases(self, *args, **kargs)        
        #self.opts_merge( kargs )   ## this is now part of set_kargs_defaults
        
        s = self
        s.parentRef = parentRef
        s.init_env()
        qapp_existing_instance = QtCore.QCoreApplication.instance()
        if qapp_existing_instance  is not  None:
            s.qapp = qapp_existing_instance
        else:
            s.qapp = QtGui.QApplication(Mod_sys.argv)
            ## it seems like you can't inherit anything from QApplication, must be used directly
        
        
        s.widgets = { }
        s.init_widgets( )
        
        if make_default_ui==True:
            self.make_default_ui( *args, **kargs )
        
        
        ##if self.__class__.__name__ == 'App_base_ui':
        ##    self.init_bases(self, *args, **kargs)
        ##    print( 'App_base_ui.__init__ called self.init_bases' )
        
        ##print( 'App_base_ui.__init__ ran' )
    
    
    def create_mainWindow( self, *args, **kargs ):
        ui_parent_window = self.opts.get( 'ui_parent_window' , None )
        ui_title = self.opts.get( 'ui_title' , None )
        ui_width = self.opts.get( 'ui_width' , None )
        ui_height = self.opts.get( 'ui_height' , None )
    
    
        if ui_parent_window  is not  None:
            dialog = QtGui.QDialog(ui_parent_window)
        else:
            dialog = QtGui.QDialog( )
            
        if ui_title  is not  None:
            dialog.setWindowTitle( ui_title )   
        
        if ui_width  is not None:
            dialog.resize(  ui_width, dialog.size().height()  ) 
        if ui_height  is not None:
            dialog.resize(  dialog.size().width(), ui_height  )
        
        self.widgets['mainWindow'] = dialog
        
        return dialog

    def create_default_layout( self, target_widget=None ):
        w = self.widgets
        if target_widget is None:
            target_widget = self.mainWindow
        formGroupBox = w['formGroupBox'] = QtGui.QGroupBox("")
        formLayout = w['formLayout'] = QtGui.QFormLayout()
        formGroupBox.setLayout(formLayout)
        mainLayout = w['mainLayout'] = QtGui.QVBoxLayout()
        mainLayout.addWidget(formGroupBox)
        if target_widget  is not  None:
            target_widget.setLayout( formLayout )
        return mainLayout
    
    def create_lineEdit(self, name=None, text=None, label=None,
        no_label=False, add_to_layout=True
        ):
        
        assert  name  is not  None
        assert  text  is not  None
        
        if label is None:
            label = ''
        
        
    
    def create_button( self, name=None, text=None, label=None, no_label=False,
        add_to_layout=True, clicked=None
        ):
        
        self.create_widget( widget_type='button', name=name, text=text, 
            label=label, no_label=no_label, add_to_layout=add_to_layout, clicked=clicked
        ) 
        
    def create_lineEdit( self, name=None, text=None, label=None, no_label=False,
        add_to_layout=True, clicked=None
        ):
        
        self.create_widget( widget_type='lineEdit', name=name, text=text, 
            label=label, no_label=no_label, add_to_layout=add_to_layout, clicked=clicked
        )
    
    def create_widget(self, widget_type=None, name=None, text=None, label=None, no_label=False,
        add_to_layout=True, clicked=None,
        ):
        assert  name  is not  None
        assert  text  is not  None
        assert  widget_type  is not  None
        
        if label is None:
            label = ''
            
        ## Big problem right here is there is no way to find the add
        ## label in the widgets dict ****
        
        if widget_type=='lineEdit':
            widget = QtGui.QLineEdit(text=text)
        elif widget_type=='button':
            if clicked is None:
                widget = QtGui.QPushButton(text=text)
            else:
                widget = QtGui.QPushButton(text=text, clicked=clicked)
                
        if add_to_layout:
            if no_label:
                self.formLayout.addRow( widget )
            else:
                self.formLayout.addRow( label, widget )
        
        self.widgets[name] = widget
        return widget
        
    
    def add_widgets_from_dict( self, ui_dict ):
        if ui_dict  is not  None:
            assert isinstance( ui_dict, dict )        
            w = self.widgets
            keys = ui_dict.keys()
            formLayout = w['formLayout']
            for k in keys:
                entry = ui_dict[k]
                if isinstance( entry, dict ):
                    assert len( entry.items() ) == 2  ## the sub dict should have exactly two items
                    self.add_row_from_dict( entry )
                else:
                    ## At this point, we expect entry to be a widget!
                    formLayout.addRow( entry )
                    #print( "widget added: " + k )
                    w[k] = entry
        return self
                
    #def addRowFromList(self, listRef ):
    #    ## We want this to fail in the event that the list doesn't have two items
    #    ##    This first one can be a string if we want
    #    w1 = listRef[0]
    #    w2 = listRef[1]
    #    self.formLayout.addRow( w1, w2 )
    
                
    def show(self):
        w = self.widgets.get('mainWindow', None)
        if w is not  None:
            w.show()
        return self
    
    def make_ui_from_dict( self, dict, *args, **kargs ):
        if self.mainWindow is None:
            self.create_mainWindow()
        if self.formLayout  is  None:
            self.create_default_layout()
        self.add_widgets_from_dict(dict)
        return self

    
    def make_default_ui(self, window_title=None, form_title='', *args, **kargs ):
        ui_parent_window = kargs.get( 'ui_parent_window' , None )
        ui_width = kargs.get( 'ui_width' , None )        
        ui_height = kargs.get( 'ui_height' , None )
        ui_title = kargs.get( 'ui_title' , None )
        widgets_to_add_dict = kargs.get( 'ui_widgets', None )
        w = self.widgets
        
        self.add_widgets_from_dict
        
            
        ## Make the main window widget, functions auto add new widgets to self.widgets
        ## the try test is here because anyapp got updated and we want to support calls to the
        ## old function
        try:
            w['mainWindow'] = self.create_mainWindow_dialog(
                ui_parent_window = ui_parent_window,
                ui_title = ui_title,
                ui_width = ui_width,
                #ui_height = ui_height,
            )
        except:
            w['mainWindow'] = self.create_mainWindow(
                ui_parent_window = ui_parent_window,
                ui_title = ui_title,
                ui_width = ui_width,
                #ui_height = ui_height,
            )        
        self.create_default_layout( )
        self.add_widgets_from_dict( widgets_to_add_dict )
        #self.make_default_ui_ovr()
        self.show()
        
        return self
    
    #def make_default_ui_ovr
        
    def output(self, *args, **kargs ):
        try:
            out = self.widgets['outputTextEdit']
            scroll = out.verticalScrollBar()
            for v in args:
                out.setPlainText( out.toPlainText() + str(v) + '\n'  )    
                scroll.setValue( scroll.maximum()  )
                
        except:
            print "Could not print using outputTextEdit widget."
            for v in args:
                print( v )
                pass

    def init_widgets(self, *args, **kargs):
        self.init_widgets_ovr( *args, **kargs)
        return self
        
    def init_widgets_ovr(self, *args, **kargs):
        ## Override this to create widgets for your ui
        ##
        return self
        
    def go(self, *args, **kargs):
        try:
            self.qapp.exec_()
        except:
            print(    traceback.format_exc()    )

        

class App_base_example(App_base):
    def __init__(self, *args, **kargs):
        ##self.init_bases(self, *args, **kargs )
        ##super( self.__class__, self ).__init__(*args, **kargs)
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example Init"
        self.debug( c + "   " + "self type:" + str(type(self))  )
              
class App_base_example2a(App_base_example):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example2a Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  )        
           
class App_base_example2b(App_base_example):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example2b Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  ) 

class App_base_example3a(App_base_example2a, App_base_example2b):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example3a Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  )
        
class App_base_example3b(App_base_example2a, App_base_example2b):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example3b Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  )
                
class App_base_example4(App_base_example3b, App_base):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example4 Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  )
        
class App_base_example5(App_base_example3a, App_base_example4):
    def __init__(self, *args, **kargs ):
        Object_base.init_bases(self, *args, **kargs)
        c = "App_base_example5 Init  :)  "
        self.debug( c + "   " + "self type:" + str(type(self))  )
        
        
        
        



def main( ui=True ):
    app = App_Base_example5( debug=True )
    sys.exit( app.go() )
    
if __name__ == "__main__":
    main()

def notes_as_strings():
    pass
    """                    
    def runCode(self):
        #print('running')
        #o1 = self.textb2.get(1.0, Tk.END)
        o1 = self.ui.textb2.getText()
        o2 = self.ui.textb3.getText()
        try:
            #print( help(self.textb1)  )
            #print( o1  )
            #print( o2  )
            code = str(  self.ui.textb1.getText()  )  ## why do they use 1.0 ???
            exec code in locals(), globals()
        except:
            self.output( Traceback.format_exc() )
        
    def runRsync(self):
        try:
            self.runRsyncPhase2()
        except:
            out = Traceback.format_exc()
            out += "\nAn error occurred when performing the rsync operation.\n"
            out += "Please check your paths and try again."            
            self.output( out )
            
        
    def runRsyncPhase2(self):
        print Mod_os.getcwd()
        
        
        prog = "rsync.exe"
        prog = prog.replace('/', '\\')        
        opts = "-rv --fake-super --modify-window 3 --no-group"
        
        cyg = '/cygdrive/'
        
        
        ## Get the src and dest from the filters
        src = self.ui.textb2.getText().replace('\\', '/')
        dest = self.ui.textb3.getText().replace('\\', '/')
        
        ## Get rid of anything after a newline character        
        src = src.partition('\n')[0]
        dest = dest.partition('\n')[0]        
                
        ##Get rid of the drive colons
        if ':' in src:
            src = src.replace(':', '')
            if len(src):
                while src[0] == '/':
                    src = src[1:]
            src = cyg+src ## Put a cygdrive on front            
        else:
            assert src[0:2]=='//'
            
        if ':' in dest:
            dest=dest.replace(':', '')
            if len(dest):
                while dest[0] == '/':
                    dest = dest[1:]
            dest = cyg+dest ## Put a cygdrive on front
        else:
            assert dest[0:2]=='//'
        
        
        ##Add trailing slashes for folders
        if src[-1] != '/':
            src = src+'/'
        if dest[-1] != '/':
            dest = dest+'/' 

        ## Surround src and dest with quotes
        src = '"' + src + '"'
        dest = '"' + dest + '"'
        
        p=' '
        
        cmd = prog + p + opts + p + src + p + dest
        print( prog )
        print(src)
        print(dest) 
        print( cmd )
          

        Mod_os.chdir( self.parentRef.running_script__file_path_only )        
        self.parentRef.running_script__file_path_only
        
        
        r = Subprocess.call( cmd, shell=True )
        
        out = "rsync complete, errors reported are likely just due to lack of POSIX priviledges compatibility"
        print( out )
        
        self.output( out  )
        
        pass
      
        for i in outer_frames:
            info = Inspect.getframeinfo(i) ##returns Traceback(filename, lineno, function, code_context, index)
            print "info is:"
            print info
            func_name = info[2]
            context = info[3]
            print "\nContext is:"
            print context
            print "\nContext type is:"
            print type(context)
            #func = info[2] 
            print "\nFunc is:"
            print func_name

        #print type(func)
        #print "\nFunc class is:"
        #print func['__class__']
        #print "Dir is:\n"
        #print dir(func)

        
        #func = func_code
        #print( Inspect.stack()[1][3] )
        
        #frame = self.__class__.im_class
        #print( frame )
        #print(  stack()  )
        #s = self
        #s.opts_by_class = {}
        #s.opts_by_class[ str(self.__class__) ] = kargs   
    
    

    u = self.ui
    x = u.__dict__.keys()
    for i in x:
        j = getattr( self.ui, i )
        try:
            j['background'] = 'red'
        except:
            pass

    self.output( self.ui.button1['background'] )
    self.ui.button_code['background'] = 'blue'
      

    print( "example mro")
    print( self.__class__.__mro__ )
    print( "example bases")
    print( self.__class__.__bases__ )
    print( '\n\n\n' )
    mro = self.__class__.__mro__
    bases = self.__class__.__bases__



    Notes:

    Or, How to use variable length argument lists in Python.

    The special syntax, *args and **kwargs in function definitions is used to pass a variable number of arguments to a function. The single asterisk form (*args) is used to pass a non-keyworded, variable-length argument list, and the double asterisk form is used to pass a keyworded, variable-length argument list. Here is an example of how to use the non-keyworded form. This example passes one formal (positional) argument, and two more variable length arguments.

    def test_var_args(farg, *args):
        print "formal arg:", farg
        for arg in args:
            print "another arg:", arg

    test_var_args(1, "two", 3)
    Results:

    formal arg: 1
    another arg: two
    another arg: 3

    Here is an example of how to use the keyworded form. Again, one formal argument and two keyworded variable arguments are passed.

    def test_var_kwargs(farg, **kwargs):
        print "formal arg:", farg
        for key in kwargs:
            print "another keyword arg: %s: %s" % (key, kwargs[key])

    test_var_kwargs(farg=1, myarg2="two", myarg3=3)
    Results:

    formal arg: 1
    another keyword arg: myarg2: two
    another keyword arg: myarg3: 3

    Using *args and **kwargs when calling a function
    This special syntax can be used, not only in function definitions, but also when calling a function.

    def test_var_args_call(arg1, arg2, arg3):
        print "arg1:", arg1
        print "arg2:", arg2
        print "arg3:", arg3

    args = ("two", 3)
    test_var_args_call(1, *args)
    Results:

    arg1: 1
    arg2: two
    arg3: 3
    Here is an example using the keyworded form when calling a function:

    def test_var_args_call(arg1, arg2, arg3):
        print "arg1:", arg1
        print "arg2:", arg2
        print "arg3:", arg3

    kwargs = {"arg3": 3, "arg2": "two"}
    test_var_args_call(1, **kwargs)
    Results:

    arg1: 1
    arg2: two
    arg3: 3
    
    
    
    Relative Imports:    http://docs.python.org/tutorial/modules.html   sec. 6.4.2
        Starting with Python 2.5, in addition to the implicit relative imports described above, you can write explicit relative imports with the from module import name form of import statement. These explicit relative imports use leading dots to indicate the current and parent packages involved in the relative import. From the surround module for example, you might use:

        from . import echo
        from .. import formats
        from ..filters import equalizer    
    

    ## Random old widgets code, just for an example
    
        #srcLabel = w['srcLabel'] = QtGui.QLabel("Source:")
        #srcLineEdit = w['srcLineEdit'] = QtGui.QLineEdit()
        #destLabel = w['destLabel'] = QtGui.QLabel("Destination:")
        #destLineEdit = w['destLineEdit'] = QtGui.QLineEdit()
        #optsLabel = w['optsLabel'] = QtGui.QLabel("Additional Options:")
        #optsLineEdit = w['optsLineEdit'] = QtGui.QLineEdit()
        
        #formLayout.addRow(srcLabel, srcLineEdit )
        #formLayout.addRow(destLabel, destLineEdit )
        #formLayout.addRow(optsLabel, optsLineEdit )
            
        
            
    
    
    
    """