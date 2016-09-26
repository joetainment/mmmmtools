#### This code came from here:
####  http://maya-tricks.blogspot.ca/2009/04/python.html

import maya.OpenMaya as OM
import math
#from pymel.core import *
import pymel.all as pm



class SelectorVolumeSelect(object):
    #### The code for pyRayIntersect and testIntersect came from:
    ####  http://maya-tricks.blogspot.ca/2009/04/python.html
    @classmethod
    def pyRayIntersect(cls, mesh, point, direction=(0.0, 1.0, 0.0)):
      OM.MGlobal.selectByName(mesh,OM.MGlobal.kReplaceList)
      sList = OM.MSelectionList()
      #Assign current selection to the selection list object
      OM.MGlobal.getActiveSelectionList(sList)
    
      item = OM.MDagPath()
      sList.getDagPath(0, item)
      item.extendToShape()
    
      fnMesh = OM.MFnMesh(item)
      raySource = OM.MFloatPoint(point[0], point[1], point[2], 1.0)
      rayDir = OM.MFloatVector(direction[0], direction[1], direction[2])
      faceIds = None
      triIds = None
      idsSorted = False
      testBothDirections = False
      worldSpace = OM.MSpace.kWorld
      maxParam = 999999
      accelParams = None
      sortHits = True
      hitPoints = OM.MFloatPointArray()
      #hitRayParams = OM.MScriptUtil().asFloatPtr()
      hitRayParams = OM.MFloatArray()
      hitFaces = OM.MIntArray()
      hitTris = None
      hitBarys1 = None
      hitBarys2 = None
      tolerance = 0.0001
      hit = fnMesh.allIntersections(raySource, rayDir, faceIds, triIds, idsSorted, worldSpace, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTris, hitBarys1, hitBarys2, tolerance)
    
      result = int(math.fmod(len(hitFaces), 2))
    
      #clear selection as may cause problem if the function is called multiple times in succession
      OM.MGlobal.clearSelectionList()
      return result

    @classmethod
    def defaultFunc(cls):
        cls.selectVertsByVolume()
    
    @classmethod
    def volumeSelect(cls, faces=False ):
      sel = pm.ls(sl=1)
    
      if len(sel) < 2:
          print( "You must have at least two objects selected" )
          return []
    
      checkInsideObj = sel.pop()
      #checkInsideObj = sel[1]
      
      allIn = []
           
      for container in sel:

            
          allVtx = pm.ls(str(checkInsideObj)+'.vtx[*]',fl=1)

          start = pm.timerX()
        
          for eachVtx in allVtx:
              location = pm.pointPosition(eachVtx,w=1)
              test = cls.pyRayIntersect(container,location,(0,1,0))
        
              if(test):
                  allIn.append(eachVtx)
                  
      elapsedTime = pm.timerX(startTime = start)
      print "time :",elapsedTime
      pm.select(allIn,replace=1)
      if faces==True:
          pm.mel.eval( 'ConvertSelectionToContainedFaces;' )
      return pm.ls(selection=True)

    

"""
class SelectorVolumeSelectApp(MmmmTools.MmmmAnyapp):
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
            [ 'ui_title', 'Mmmm Volume Selector  (see button tooltips...)' ],
            [ 'ui_width',  350 ],
            #[ 'ui_parent_window', MmmmTools.UiUtils.getMayaWindowAsWrappedInstance() ] ,
        ])
        
        ## An easy way to add a bunch of widgets to our UI
        ## just put them in a dict and add that dict to kargs
        ## as ui_widgets.  Annyapp looks for this later!
        ## By using OrderedDict, we make sure they stay in the
        ## vertical order on screen        
        your_ui_widgets = OrderedDict()
        wstr = "selectVertsButton"              
        your_ui_widgets[wstr] = QtGui.QPushButton( 'Select Verts' )
        your_ui_widgets[wstr].setToolTip( 'Selects verts in last selected by volumes of other selected objects.' )        
        your_ui_widgets[wstr].clicked.connect(
            lambda: SelectorVolumeSelect.volumeSelect()
        )       
        wstr = "selectFacesButton"
        your_ui_widgets[wstr] = QtGui.QPushButton( 'Select Faces' )
        your_ui_widgets[wstr].setToolTip( 'Selects faces in last selected by volumes of other selected objects.' )        
        your_ui_widgets[wstr].clicked.connect(
            lambda: SelectorVolumeSelect.volumeSelect(faces=True)
        )
        kargs['ui_widgets'] = your_ui_widgets
        
        ## This initializes all the Anyapp super classes,
        ## which takes the options in kargs and applies them
        ## if make_ui has been set True in kargs
        ## it will now create the default ui
        ## and populate it with ui_widgets
        ## if ui_widgets are found in kargs
        MmmmTools.Object_base.init_bases(self, *args, **kargs)
        
#setattr( mmmmTools.selector, "volumeSelector", MmmmVolumeSelector() )
#mmmmTools.selector.volumeSelector.selectVertsByVolume()

#volumeSelectorApp = MmmmVolumeSelectorApp( make_default_ui=True )
"""      
