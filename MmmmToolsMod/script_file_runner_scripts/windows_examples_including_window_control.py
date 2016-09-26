import traceback
import pymel.all as pm
import maya.cmds


class WindowOpenAndCloser(object):
    @classmethod
    def deleteAllWindows(cls):
        windows = pm.lsUI(typ='window')
        for win in windows:
            try:
                print( win )                
                if win != 'MayaWindow':
                    pm.deleteUI( win )
                    x=0
            except:
                print( traceback.format_exc() )

    @classmethod
    def hideAllWindows(cls):
        setVisibilityOnAllWindows( False )
    @classmethod
    def showAllWindows(cls):
        setVisibilityOnAllWindows( True )
                
    @classmethod
    def setVisibilityOnAllWindows(cls, vis ):
        windows = pm.lsUI(typ='window')
        for win in windows:
            try:
                pm.window( win, edit=True, visible=vis )
            except:
                print( traceback.format_exc() )
    @classmethod
    def hyperShadeToggle(cls):
        ## disabled unnecessary code only here for reference:
        ## we could lsUI and then check list but we don't have to
        ##
        ##  try effectively does that for ussince the try effectively does that for us        
        # listedWindows = cmds.lsUI(typ='window')

        showFunc, hideFunc = cls.hyperShadeShow, cls.hyperShadeHide
        try:
            isVisible = pm.window('hyperShadePanel1Window', query=True, visible=True)        

            if isVisible:
                hideFunc()
            else:
                showFunc()
        except:
            showFunc()
                        
    @classmethod        
    def hyperShadeClose(cls):
        pm.deleteUI('hyperShadePanel1Window')
