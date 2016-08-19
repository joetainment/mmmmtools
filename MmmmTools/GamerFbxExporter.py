import pymel.all as pm
import traceback


##  **** Later you can enable the use of user properties!
##    See the unity docs!
##    http://docs.unity3d.com/Documentation/ScriptReference/
##        AssetPostprocessor.OnPostprocessGameObjectWithUserProperties.html

class GamerFbxExporter(object):
    def __init__(self, parentRef):
        self.parent = parentRef
        self.mmmm = self.mmmmTools = self.parent
        
        #self.exportType = "fbx"
        #self.
        #self.ui = LiamExporterUi( parentRef=self )
        #try:
        #    pm.loadPlugin("objExport.mll")
        #except:
        #    pass

    def getPreset(self, presetName = 'mmmmDefault.fbxexportpreset', presetFolder = None):
        presetFolderBase = self.mmmm.platformManager.info.mmmm.mmmm_pather.st.replace('\\','/')
        if presetFolder is None:
            presetFolder = presetFolderBase + '/presets/fbx_export_presets/'
            
        presetStr=presetFolder+presetName
        
        return presetStr

    def addAttributesForExport(self):
        self.addAttributeForExportFile()
        self.addAttributeForExportPath()
    
    def addAttributeForExportFile(self):
        for obj in pm.ls(selection=True, transforms=True):
            try:
                obj.addAttr( "mmmmExportFile", dataType="string")
            except:
                print( "Attribute not added, it might already exist on the selected object.")
                print traceback.format_exc()
    def addAttributeForExportPath(self):
        for obj in pm.ls(selection=True, transforms=True):
            try:
                obj.addAttr( "mmmmExportPath", dataType="string" )  #longname="
            except:
                print( "Attribute not added, it might already exist on the selected object.")
                print traceback.format_exc()
    
    def exportSelection(self):
        originalSelection = pm.ls(selection=True)
        ## Only attempt to export directly from transform nodes!
        objs = pm.ls(selection=True, transforms=True)
        self.exportFbx( objs )
        pm.select( originalSelection) 
           
    def exportAll(self):
        originalSelection = pm.ls(selection=True)
        ## Only attempt to export directly from transform nodes!
        objs = pm.ls( transforms=True )
        self.exportFbx( objs )
        pm.select( originalSelection)

    def exportFbx(self, objsOnWhichToAttemptExport):
        
        objsToExport = []
        
        errors = []
        
        for obj in objsOnWhichToAttemptExport:
            
            attr = getattr(obj, "mmmmExportFile", None)
            if attr:
                aVal = attr.get()
                if not aVal=="":
                    objsToExport.append( obj )
                else:
                    print( "Export information on node not sufficient.")
            else:
                errors.append( "object" + obj.name() + " DID NOT have attr")
        
        
        for obj in objsToExport:
            pm.select( obj, replace=True)
        
            dirPathStr = getattr(obj,'mmmmExportPath').get()
            print( "dirPathStr: " + dirPathStr )            
            fnameStr = getattr(obj,'mmmmExportFile').get()
        
            dirPathStr = dirPathStr.replace( '\\', '/')
            print( "dirPathStr with replacement only: " )
            print( "dirPathStr: " + dirPathStr )
            
            if dirPathStr.endswith('/'):
                sep = ''
            else:
                sep = '/'
            
            isDirpathRelative = (
                dirPathStr.startswith(    './'    )
                or
                dirPathStr.startswith(    '../'   )
            )
            
            print( "dirPathStr before being changed: " )
            print( "dirPathStr: " + dirPathStr )            
            
            if isDirpathRelative:
                workspacePathStr = pm.workspace( q=True, dir=True )
                print( "Exporting relative to: " + workspacePathStr )
                dirPathStr = workspacePathStr  +   dirPathStr
                print( "workspacePathStr   Exporting relative to: " + workspacePathStr )
                print( "dirPathStr: " + dirPathStr )
            
            
            dirPathAndFileAndExtStr = dirPathStr + sep + fnameStr
            print( "Attempting to export object: " + obj.name() )
            print( "exporting to: " + dirPathAndFileAndExtStr )
            
            pm.select(hierarchy=True)
                    
            ## Load the Fbx Preset That should be used
            ##  **** ideally, this should allow using a preset file in a relative folder
            ##       currently just uses from MmmmTools folder
            presetStr = self.getPreset() 
            cmd = 'FBXLoadExportPresetFile -f "' + presetStr + '";'
            #print(cmd)
            pm.mel.eval(
                cmd
            )
            
            fname = dirPathAndFileAndExtStr
            #fname = cmds.file( location=True, query=True )
            #fnameParts = fname.split('.')
            ##  any string then .join will combine a list by the string before .join
            #fname = ".".join( fnameParts[0:-1] )
            #ename = "__FORUDK.fbx"
            #fname = fname + ename
            
            pm.exportSelected(
                fname,
                shader = 1,
                force=True,
                typ = "FBX export",
                            
                #pr = 1,  ##
                #es = 1,
            )
   
    
    def exportAsObj(self):
        pass
    
    
    def getPathOfCurrentFile(self):
        print( pm.file( location=True, query=True ) )
        
        
        return path
    
    def exportAsObj(self):
        pm.exportSelected(
            'd:/deletemeLiamExport.obj',
            shader = 1,
            force=True,
            typ = "OBJexport",           
            #pr = 1,  ##
            #es = 1,
        )
    
    def buildOutputFileNameWithPath( self, newEnding ):
        fname = cmds.file( location=True, query=True )
        fnameParts = fname.split('.')
        ##  any string then .join will combine a list by the string before .join
        fname = ".".join( fnameParts[0:-1] )
        ename = "__FORUDK.fbx"
        fname = fname + ename
        return outputFileNameWithPath
    
    def exportAsFbxForUdk(self):
        originalSelection = pm.ls(selection=True)
               
        cmd = 'FBXLoadExportPresetFile -f "' + PresetFileNameWithPathForUdk + '";'
        #print(cmd)
        pm.mel.eval(
            cmd
        )
        pm.exportSelected(
            fname,
            shader = 1,
            force=True,
            typ = "FBX export",
                        
            #pr = 1,  ##
            #es = 1,
        )
        pm.select( originalSelection)
        
"""
class LiamExporterUi(object):
    def __init__(self, parentRef=None):
        self.parentRef = parentRef
        #self.widgets = {}
        
        self.win = pm.window( title="Liam Exporter" )
        #self.widgets['win'] = self.win
        
        with self.win:
            self.col = pm.columnLayout()
            #self.widgets['col'] = self.col
            
            with self.col:
                self.buttonFbx = pm.button(
                    label="Export Selected As FBX",
                    command=lambda x: self.parentRef.exportAsFbxForUdk(),
                )
                self.buttonObj = pm.button(
                    label="Export Selected As OBJ",
                    command=lambda x: self.parentRef.exportAsObj(),
                )
                #self.widgets['button'] = self.button
                
        self.win.show()
"""
        