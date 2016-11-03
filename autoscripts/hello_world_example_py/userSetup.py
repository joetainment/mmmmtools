## note that the userSetup file .py can't do anything much
## because it won't have a unique name in terms of all modules
## loaded by Maya's Python interpreter.
## Keep in mind, modules aren't identified by absolute location
## so using or python autoscripts, your modules names
## would have to be globally unique in terms
##
## Beware of naming conflicts!
import sys

## Reloading of modules is somewhat flacky when using these autoscripts.
## You have to reload them slightly more carefully than might normally be needed
## since it's possible that you can't "reload" even though the module has been loaded
## because of the fact that this code is being run by exec and this
## userSetup.py isn't a real module

try:
    reload( hello_world_example_python_module )
except:
    ## needs to see if the module exists already, and if so
    ## reload it
    if 'hello_world_example_python_module' in sys.modules:
        hello_world_example_python_module = sys.modules['hello_world_example_python_module']
        reload( hello_world_example_python_module )
    else:
        import hello_world_example_python_module

