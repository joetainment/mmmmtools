import maya.OpenMayaUI as omui
import PySide.QtGui as QtGui
#import PyQt4.QtGui as QtGui

import PySide.QtCore as QtCore
#import PyQt4.QtCore as QtCore
import shiboken
        
def QtWidgetRecurse(widget, maxDepth=1,filter=None, callback=None, _privateDepth=0):
    depth = _privateDepth
    
    ## as of python 3.3+,
    ##  SimpleNamespace() would work
    ##  but maya still uses old python
    ctx = type('Duck', (object,), {})
    setattr( ctx, 'widget', widget )
    setattr( ctx, 'depth', depth )
    setattr( ctx, 'maxDepth', maxDepth )
    setattr( ctx, 'filter', filter )    
    setattr( ctx, 'callback', callback )
    assert( type(depth)==type(1) )
    

    
    try:
        toolTip = widget.toolTip()
    except:
        toolTip = ''
    
    assert filter==None
    if filter==None:
        if callback==None:    
            print(
                '\t' * (depth+1)
                + widget.objectName()
                + "  " + str( type(widget) )
                + "  " + toolTip
            )
        else:
            callback(ctx)

        if depth <= maxDepth:
            for child in widget.children():
                QtWidgetRecurse(child, _privateDepth=depth+1,
                    maxDepth=maxDepth, callback=callback
                )

            
def callbackExample( ctx ):
    widget = ctx.widget
    if widget.objectName() =='toolBar7':
        if type(widget)==QtGui.QLayout:
            layout = widget
            button = QtGui.QPushButton()
            layout.insertWidget( 3, button )
            button.setText( 'test' )
            #button.setParent( widget.parent() )
            button.show()
            #widget.parent().hide()
            
mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mainWindow= shiboken.wrapInstance(long(mayaMainWindowPtr), QtGui.QWidget)   ## mayaMainWindow

QtWidgetRecurse(mainWindow,maxDepth=8, callback=callbackExample )

"""
Look into more examples from here:
https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/Maya-SDK/files/GUID-66ADA1FF-3E0F-469C-84C7-74CEB36D42EC-htm.html
"""




"""
        
        if child.objectName()=='MainCommandLine':
            #print(    help( type(child)  )    )
            for child in child.children():
                child.hide()
                print( child.geometry() )
                print( child.objectName() )
                try:
                    print( child.toolTip() )
                except:
                    print('none')
                    
                
"""