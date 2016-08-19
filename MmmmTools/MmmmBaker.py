## xnormal baking tool
import os
import sys
import math
import time
import subprocess
import traceback
import shutil

import pymel.all as pm
import maya.cmds as cmds

import xml.etree.ElementTree as XmlTree



            

class MmmmBaker(object):
    def __init__(self, autorun=False):
        if autorun==True:
            self.bake( )
    def bake( self, modelsPath="", highSuffix="", xnormalExe="", xmlFiles="", cageSuffix="", typeSuffixes="", cageOffset=None ):
        
        try:
            cmds.progressWindow( endProgress=True )
        except:
            pass  #print( "..." )
        cmds.progressWindow(isInterruptable=1)

        
        if highSuffix=="":
            highSuffix="_hi"
        
        if cageSuffix=="":
            cageSuffix= "_cage"
        
        if cageOffset==None:
            cageOffset=2.0
        
        if typeSuffixes=="":
            typeSuffixes=['normals','heights','vcols', 'occlusion', 'curvature', 'cavity']
        typeOfTypeSuffixes = type(typeSuffixes)
        if typeOfTypeSuffixes==type( "a_string" ) or typeOfTypeSuffixes==type( u"a_unicode_string" ):
            typeSuffixes = typeSuffixes.split(",")

        
        xnormal_exe = xnormalExe.replace("\\","/")
        folder_with_high_models = modelsPath.replace("\\","/")
        xml_files = xmlFiles.split(',')

        objExt = ".obj"
        
        ## Set pythons current working directory
        os.chdir( folder_with_high_models )
        
        ## Get the selected objects, store as both an original selection
        ## and a copy of the original selection, objs
        osel = pm.ls(selection=True)
        objs = osel[:]
        
        scriptIsCanceled = False
        
        cancelCheckSleepTimeStartup = 0.5
        cancelCheckSleepTime = 0.01
        
        for obj in objs:
            time.sleep( cancelCheckSleepTimeStartup )
            if cmds.progressWindow(query=1, isCancelled=1):
                print( "Script canceled by user,   eg. escape key." )
                scriptIsCanceled = True
                break
            try: ## try each obj
                ## Select the object and set up some basic variables,
                ## such as the name and the python cwd
                pm.select( obj )                
                obj_name = obj.name()
                cwd = os.getcwd()
                cwdUni = unicode(cwd)
                
                ## Triangulate before export
                print( obj )
                tri_op = pm.polyTriangulate( obj )
                
                ## Export lo,  triangulated
                export_target_including_file_and_path = os.getcwd().replace("\\","/") + "/" + obj_name + objExt
                pm.select( obj )
                pm.exportSelected(
                    export_target_including_file_and_path,sh = 1, pr = 1, typ = "OBJexport", es = 1, force=True
                )
                
                print( obj )
                
                try:
                    cageOffsetCustom = obj.mmmmBakerCageOffset.get()
                except:
                    cageOffsetCustom = cageOffset
                    print( "no custom cage offset found, using default" )
                
                trans_op = pm.polyMoveVertex( obj, localTranslateZ=cageOffsetCustom )
                
                ## Export Cage
                export_target_including_file_and_path = \
                    os.getcwd().replace("\\","/") + "/" + obj_name + cageSuffix + objExt
                pm.select( obj )                    
                pm.exportSelected( export_target_including_file_and_path,
                    sh = 1, pr = 1, typ = "OBJexport", es = 1, force=True
                )
                
                ## Cleanup cage offset and triangulation
                pm.delete( trans_op )
                pm.delete( tri_op )
                
                
                            #if obj_name.endswith( lo_suffix ):
                            #    high_name = obj_name.replace( lo_suffix, highSuffix )
                            #else:
                high_name = obj_name + highSuffix
                    

                for i, xml_file in enumerate(xml_files):
                    time.sleep( cancelCheckSleepTime )                
                    if cmds.progressWindow(query=1, isCancelled=1):
                        scriptIsCanceled=True
                        print( "Script canceled by user,   eg. escape key." )
                        break
                    
                    pm.select( obj )
                    pm.mel.eval(  "ConvertSelectionToUVs;" )
                    uvs = pm.ls(selection=True, flatten=True)
                    coUV =  pm.polyEditUV( uvs, query=True )
                    coU, coV = coUV[::2], coUV[1::2]
                    pm.select(obj)
                    
                    
                    """"
                    for c in coU:
                        if c >= 0.0 and c < 1.0:
                            udim1001=True  
                        if c >= 1.0 and c < 2.0:
                            udim1002=True    
                        if c >= 2.0 and c < 3.0:
                            udim1003=True    
                        if c >= 3.0 and c < 4.0:
                            udim1004=True
                    """

                            
                    dictOfUsedUvRanges = {}
                    for cIndex in xrange( len(coU) ):
                        tu = coU[cIndex]
                        tv = coV[cIndex]
                        tuInt = math.floor( tu )
                        tvInt = math.floor( tv )
                        
                        dictOfUsedUvRanges[ tuInt,tvInt ] = int( 1000 + (tuInt+1) + (tvInt*10) )
                        
                    #print(   "length of dictionary:")
                    #print(   len(  dictOfUsedUvRanges.keys()  )    )
                    #break
                    
                    
                    for keyRange, udim   in dictOfUsedUvRanges.items():
                        uInKey = keyRange[0]
                        vInKey = keyRange[1]
                        uOffset = uInKey * -1.0
                        vOffset = vInKey * -1.0
                        if uOffset==0.0:
                            uOffset=0.0  #in case of negative 0.0, fucking hell!
                        if vOffset==0.0:
                            vOffset=0.0  #in case of negative 0.0, fucking hell!
                            
                        
                        
                        # do something similar for vOffset.
                        ## edit xml export with uOffset and uOffset here!
                        
                    
                        """"
                        if udim1001==True: uOffsets.append( 0.0 )
                        if udim1002==True: uOffsets.append( -1.0 )
                        if udim1003==True: uOffsets.append( -2.0 )
                        if udim1004==True: uOffsets.append( -3.0 )
                        

                        
                        
                        for uOffset in uOffsets:
                        """
                        
                        time.sleep( cancelCheckSleepTime )
                        if cmds.progressWindow(query=1, isCancelled=1):
                            scriptIsCanceled=True
                            print( "Script canceled by user,   eg. escape key." )
                            break
                        xml_file_abs = os.path.join( cwdUni, xml_file )
                        print( xml_file_abs )
                        xml_file_modified = u'tmp_mmmmBaker.xml'
                        xml_file_modified_abs = os.path.join( cwdUni, xml_file_modified )
                        
                        xml_in_mem = ''
                        with open( xml_file_abs, 'r' ) as fh:
                            xml_in_mem = fh.read()
                        
                        xml_in_mem = xml_in_mem.replace(
                             'UOffset="0.', 'UOffset="' + str(uOffset)
                        )
                        xml_in_mem = xml_in_mem.replace(
                             'VOffset="0.', 'VOffset="' + str(vOffset)
                        )
                        
                        uOffsetAsInt = int( -1 * uOffset)
                        vOffsetAsInt = int( -1 * uOffset)
                        
                        
                        folder_with_high_models__no_trailing_slash = \
                            folder_with_high_models
                        if folder_with_high_models__no_trailing_slash.endswith("/"):
                            folder_with_high_models__no_trailing_slash =\
                                folder_with_high_models__no_trailing_slash[:-1]
                        xml_in_mem = xml_in_mem.replace(
                             "C:\\Users\\Public\\mmmmBaker",
                             folder_with_high_models.replace("/","\\")
                        )                        
                        
                        root = XmlTree.fromstring(xml_in_mem)
                        
                        ## Print the entire xml tree for reference'
                        #print( XmlTree.tostring( root ) )
                        
                        ## find used udims on objects
                        ## find u offset and v offset for low objects
                        ## set up a list to run a for loop for to
                        ## handle each udim found
                        
                        ## find low object
                        ## find cage object
                        ## find use cage option
                        #
                        ## find hi objects
                        ## find output

                        with open( xml_file_modified_abs, 'w' ) as fh:
                            fh.write( xml_in_mem )
                    
                        print( obj )
                        ##print( xml_in_mem )
                        print( uOffsetAsInt, vOffsetAsInt )    
                    
                    
                        try:
                            lo_to_copy_for_replacement = obj_name + objExt
                            cage_to_copy_for_replacement = obj_name + cageSuffix + objExt
                            hi_to_copy_for_replacement = obj_name + highSuffix + objExt
                                
                            shutil.copy2(lo_to_copy_for_replacement, "replaceme_lo" + objExt)
                            shutil.copy2(hi_to_copy_for_replacement, "replaceme_hi" + objExt)
                            shutil.copy2(cage_to_copy_for_replacement, "replaceme_cage" + objExt)

                            print( "xnormal subprocess starting...")
                            print(    xnormal_exe + " " + str(xml_file_modified)    )
                            subprocess.check_call( [ xnormal_exe, str(xml_file_modified)  ] )
                            print( "xnormal subprocess complete!  Continuing...")
                            for typeSuffix in typeSuffixes:
                                try:
                                    baked_name = "replaceme_" + typeSuffix + ".exr"
                                    proper_name = obj_name + "_" + "xml"+str(i).zfill(2) + "_" + "udim" + str( udim ) + "_" + typeSuffix + ".exr"
                                    shutil.copy2( baked_name, proper_name )
                                except:
                                    print(    traceback.format_exc()    )
                            
                        except:
                            print( traceback.format_exc() )

            except: ## except each obj
                print( traceback.format_exc() )
                
        pm.select( osel )
        
        ## Do something here to attempt to combine/composite textures together.
        ## Until then, just tell the user to use the photoshop action
        ## which should be provided with MmmmTools
        ## Add some explaination for how to use the action
        
        cmds.progressWindow( endProgress=True )
        if not scriptIsCanceled:
            print( "Baking complete!")
            print( "Baked (or at least attempted to bake) " + str( len(objs) ) + " objects." )
        
        


class MmmmBakerUi(object):
    def __init__(self, autorun=True):
        if autorun==True:
            self.run()
    def run(self):
        self.win = pm.window( title="Mmmm Baker Tool" )
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.spacers = []
                self.xnormalPathTextLabel = pm.text("Path and filename of xNormal executable:")
                self.xnormalPathTextField = pm.textField( width = 500, text="C:/Program Files/S.Orgaz/xNormal 3.19.2/x64/xNormal.exe" )
                self.spacers.append(  pm.text(" ")  )
                
                self.modelsPathTextLabel = pm.text("Path where models are:")
                self.modelsPathTextField = pm.textField( width = 500, text="C:/Users/Public/mmmmBaker" )
                self.modelsPathTextLabel2 = pm.text(
                    "(Warning, if changed, requires custom xnormal settings xml which points to new path.)"
                )                
                self.spacers.append(  pm.text(" ")  )
                
                self.highSuffixTextLabel = pm.text( 'High Suffix, on models for xnormals "high" model files, no extension' )
                self.highSuffixTextField = pm.textField( width = 500, text="_hi" )
                self.spacers.append(  pm.text(" ")  )
                
                #self.highSuffixTextLabel = pm.text( "Suffix on files: (not extension)" )
                #self.cageSuffixTextField = pm.textField( width = 500, text="_cage" )
                
                self.xmlFilesTextLabel = pm.text( "Xml files to bake, comma separated list:" )
                self.xmlFilesTextLabel2 = pm.text( "(xnormal settings files, should be in the same folder as models)" )
                self.xmlFilesTextField = pm.textField( width = 500, text="xnormal_settings_for_mmmmbaker_example.xml,xnormal_settings_for_mmmmbaker_example2.xml" )
                self.goButton = pm.button(  label="Go!  (Bake selected models) )", command=lambda x: self.go()  )
                
                
    def go(self):
        mmmmBaker = MmmmBaker(  )
        print(      self.modelsPathTextField.getText()     )
        
        m = self.modelsPathTextField.getText()
        xn = self.xnormalPathTextField.getText()
        xmls = self.xmlFilesTextField.getText()
        hs = self.highSuffixTextField.getText()
        xmls = self.xmlFilesTextField.getText()
        mmmmBaker.bake(
            modelsPath=m, xnormalExe=xn,
            xmlFiles=xmls, highSuffix=hs,
        )
        #    ## don't include the cages or types because the ui doesn't need to do that
        #    ##      cageSuffixcageSuffix=cs, typeSuffixes=ts,

