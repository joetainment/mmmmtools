## Add some code to change the default workspace that gets created after setting a project
##
## Create simple maya project with no subfolders
## "Set simple project with no subfolders"
##
##
##
## Use this regex to fix the workspace.mel file:
##find:
##" ".*";
##replace with:
##" "";
##
##
## Turns lines like this ... 
##workspace -fr "scene" "scenes";
##
##into lines like this...
##workspace -fr "scene" "";
##
##
##
print "Imported non-implemented organizer module successfully."

"""
## This module represents several upcoming features for MmmmTools.
## They are all 'commented' out currently.

## Strip Workspace of all folders
import pymel.all as pm
location = raw_input()
pm.mel.eval( 'setProject("' + location.replace('\\','/') + '");' )
w = pm.Workspace(list=True)
for key in w.fileRules.keys():
    print key
    #print w.fileRules[key]
    pm.workspace( removeFileRuleEntry=key )
    pm.workspace( fileRule=[key, ""] )
w.save()
"""