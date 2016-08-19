import pymel.all as pm
import traceback
from collections import namedtuple as NamedTuple



class Duck(object):
    pass

class MmmmQuickMenus( object ):
    ## __init__ runs as soon as we start the cube maker
    ## we almost always put a reference to self in
    ##
    def __init__(self):
        self.setupNamedTuples()
        self.setupPresets()
        self.setupEntries()
        self.setupCmds()

    
    def setupEntries(self):
        entries = self.entries = Duck()
        e = self.entryCls
        c = self.colors
        entries.a1 = e('a1 Hypershade', 'mat ed', c.yellow, 'HypershadeWindow;'  )
        entries.a2 = e('a2 Retoper', 'retopo', c.blue, lambda x: self.retoper( )  )        
        entries.a3 = e('a3 GridTools', 'grid-T', c.green, lambda x:  self.gridTools( )     )               
        entries.a4 = e('a4 Hello World', 'Hi', c.purple, lambda x: self.helloWorld()  )      

        entries.b1 = e('b1 Cube 64xyz2sxyz', 'c64', c.green, 'polyCube -w 64 -h 64 -d 64 -sx 2 -sy 2 -sz 2;' )
        entries.b2 = e('b2 Mesh > SmoothPolygons', 'smooth', c.green, 'SmoothPolygon;'  )        
        entries.b3 = e('b3 Fix Transforms', 'xf', c.green, lambda x: self.fixXforms( )         )        
        entries.b4 = e('b4 Fix Transforms2', 'xf2', c.green, lambda x: self.fixXforms( )         )     

## instance
## scale neg 1 in x        
## mirror tools
##  a button for each light type
##  make at camera look at
##  make at camera location facing same dir as camera
##  loadplugs
##
## *** buttons for individual smaller interfaces!
## spPaint3D
##    auto download it, you have permission!
##
##  selector stuff, is useful but barely used because of menu
##  export desktop deleteme.obj
##  import desktop deleteme.obj
##     same for fbx and ma   files
##
##  save uv snapshot to desktop deleteme.png
##
##
##  export  users public baking   low and cage as obj   fbx   ma
##  go to texture of selected obj/component/mat (col, refl, bump, etc)
##
##  save shelf to desktop
##  load shelf
##
##  set joe vray opts
##
##  connect colorR instead of alpha to displacement node

        
        
    def helloWorld(self):
        print( "Hello World!" )

    def setupNamedTuples(self):
        self.entryCls = NamedTuple('Entry', ['name','text','color', 'cmd'] )
                      
    def setupPresets(self):
        
        ## define things like colors, pathers useful numbers, etc
        self.colors = Duck()
        self.colors.red = ( 1.0,0.0,0.0 )
        self.colors.green = ( 0.0,1.0,0.0 )
        self.colors.blue = ( 0.1,0.2,1.0 )  ## Looks terrible as pure blue
        self.colors.yellow = ( 1.0,1.0,0.0 )
        self.colors.magenta = ( 1.0,0.0,1.0 )
        self.colors.cyan = ( 0.0,1.0,1.0 )
        self.colors.orange = ( 1.0,0.5,0.0 )
        self.colors.purple = ( 0.5,0.0,1.0 )         

    
    def setupCmds(self):
        
        self.title = "MmmmQM"       
        
        wids = self.widgets = Duck()
        win = wids.win = pm.window( title=self.title )
        win.show()
        win.setWidth( 210 )      
        ## "with" puts the tabbed stuff in the window!
        with win:
         scr = wids.scr = pm.scrollLayout(verticalScrollBarAlwaysVisible=True)
         with scr:
          #lay = wids.lay = pm.formLayout()
          col = wids.col = pm.columnLayout()
          with col:
            n = {}  ## we will collect all new widgets here!
            
            try:
                pm.text( "pop up windows" )
                rowA = wids.rowA = pm.rowLayout( numberOfColumns=10 )
                with rowA:
                  self.makeAndAddButton( n, self.entries.a1 )
                  self.makeAndAddButton( n, self.entries.a2 )
                  self.makeAndAddButton( n, self.entries.a3 )
                  self.makeAndAddButton( n, self.entries.a4 )
            except:
                print( traceback.format_exc()  )
              
            try:
                pm.text( "more..." )
                rowB = wids.rowB = pm.rowLayout( numberOfColumns=10 )
                with rowB:
                  self.makeAndAddButton( n, self.entries.b1 )
                  self.makeAndAddButton( n, self.entries.b2 )
                  self.makeAndAddButton( n, self.entries.b3 )
                  self.makeAndAddButton( n, self.entries.b4 )
            except:
                print( traceback.format_exc()  )                  
            
            try: 
                rowC = wids.rowC = pm.rowLayout( numberOfColumns=10 )
                with rowC:
                  self.makeAndAddButton( n, self.entries.c1 )
                  self.makeAndAddButton( n, self.entries.c2 )
                  self.makeAndAddButton( n, self.entries.c3 )
                  self.makeAndAddButton( n, self.entries.c4 )
            except:
                print( traceback.format_exc()  )
            
            try:  
                rowD = wids.rowD = pm.rowLayout( numberOfColumns=10 )
                with rowD:
                  self.makeAndAddButton( n, self.entries.d1 )
                  self.makeAndAddButton( n, self.entries.d2 )
                  self.makeAndAddButton( n, self.entries.d3 )
                  self.makeAndAddButton( n, self.entries.d4 )                
            except:
                print( traceback.format_exc()  )
              
      
        for k in sorted(   n.keys()  ):
            v = n[k]
            k = k.lower().replace( " ", "_" ).replace(">","_")
            setattr( wids, k, v )
                          
              

    def makeAndAddButton(self, widgetListToAddTo, entry):
              n = widgetListToAddTo
              name = entry.name
              text = entry.text
              cmd = entry.cmd
              eColor = entry.color
              w = len(text)*8
              
              print( type(cmd)  )
              c = str(cmd)
              #c = 'print "hello world";'
              print( c )
              if type(entry.cmd)==type(','):
                  tmp = n[name] = pm.button( text, bgc=eColor,
                              annotation=name[3:],
                              width=w, height=16,
                              command = lambda x: pm.mel.eval( c )
                  )
              else:
                  tmp = n[name] = pm.button( text, bgc=eColor,
                              annotation=name[3:],
                              width=w, height=16,
                              command = cmd
                  )
                           
                
              

    def gridTools(self):
        mmmmTools.modeler.runGridTools()
    def retoper(self):
        mmmmTools.modeler.runRetoper()
    
        
        
    def fixXforms(self):
        ## Get the first selected object
        objs = pm.ls(selection=True)
        
        for obj in objs:
            pm.parent( obj, world=True )

        for obj in objs:        
            ## Unparent the object
            
            ## Move the pivot to the origin
            pm.move ( obj.scalePivot , [0,0,0] )
            pm.move ( obj.rotatePivot , [0,0,0] )
            ## Freeze transforms
            pm.makeIdentity(
                obj,
                apply = True,
                normal = 0,
                preserveNormals = True
            )
            ## Note that the options for makeIdentity were simply
            ## from the Mel script history or freeze transform
            
            ## Delete the history
            pm.delete (ch = True )        
        
        
          
        

c = MmmmQuickMenus()  ## This actually starts the script!
