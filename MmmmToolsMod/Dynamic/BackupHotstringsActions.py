"""
HotstringsActions module, and easy to edit python file that allows
hotstring commands to be spefied, along with the desired MEL
commands that should be executed when the hotstring is entered.
"""
actions = {'default':"""   hotkeyEditor; print "Default Action is Hotkey Editor. """}

## Major actions for MmmmTools Development
actions['mmmm'] = """
python("import MmmmTools");
python("reload(MmmmTools)");
python("import MmmmTools");
python("mmmmTools = MmmmTools.MmmmTools()");
"""


actions['savekeys'] = """
python("mmmmTools.hotkeys.saveHotkeys()");
"""   

actions['help'] = """
python("mmmmTools.hotstrings.help()");
"""



# w  is for windows, like hypershade, outliner, etc
actions['w'] = """
print "we = texture editor, ww = hypershade, etc...";
tearOffPanel "Hypershade" "hyperShadePanel" true;
"""

actions['wu'] = """
tearOffPanel "UV Texture Editor" "polyTexturePlacementPanel" true;
"""
actions['ws'] = """
tearOffPanel "Hypershade" "hyperShadePanel" true;
"""
actions['wr'] = """
tearOffPanel "Render View" "renderWindowPanel" true;
"""
actions['wq'] = """
hyperGraphWindow "" "DAG";
"""
actions['wqq'] = """
hyperGraphWindow "" "DG";
"""
actions['wa'] = """
SpreadSheetWindow;
"""


actions['wc'] = """
optionVar -iv "connectWindowActive" 1; connectWindow;
"""
actions['wss'] = """
SpreadSheetWindow;
"""
actions['w2'] = """
tearOffPanel "Component Editor" "componentEditorPanel" true;
"""
actions['wd'] = """
tearOffPanel "Dope Sheet" "dopeSheetPanel" true;
"""
actions['wg'] = """
tearOffPanel "Graph Editor" "graphEditor" true;
"""
actions['wx'] = """
expressionEditor EE "" "";
"""
actions['wz'] = """
buildPanelPopupMenu clipEditorPanel1;
"""
actions['wv'] = """
tearOffPanel "Visor" "VisorPanel" true;
"""
actions['wcc'] = """
lockingKeyableWnd
"""
actions['w1'] = """
tearOffPanel "Outliner" "outlinerPanel" false;
"""
actions['wo'] = """
tearOffPanel "Outliner" "outlinerPanel" false;
"""





actions['wrr'] = """
mentalrayApproxEditor;
"""
actions['wf'] = """
expressionEditor EE "" "";
"""
# next is plugin manager
actions['wp'] = """
pluginWin;
"""
actions['ws'] = """
tearOffPanel "Hypershade" "hyperShadePanel" true;
"""





#m is for materials
actions['m'] = """
print "mm = Blinn,  ml = lambert, etc...";
createAndAssignShader blinn "";
"""
actions['mm'] = """
createAndAssignShader blinn "";
"""
actions['ml'] = """
createAndAssignShader lambert "";
"""
actions['mf'] = """
shadingNode -asUtility samplerInfo;
shadingNode -asTexture ramp;
"""
        
#s is for select
actions['s'] = """
select -cl;
"""
actions['sc'] = """
PolygonSelectionConstraints;
"""
actions['sr'] = """
SelectEdgeRing;
"""
actions['se'] = """
SelectEdgeLoop;
"""
actions['sb'] = """
SelectBorderEdgeTool;
"""
actions['sh'] = """
select -hi;
"""
actions['sa'] = """
SelectAll;
"""
actions['si'] = """
InvertSelection;
"""
actions['sal'] = """
SelectAllLights;
"""
actions['sag'] = """
SelectAllGeometry;
"""
#add select by painting




#d is for delete
actions['d'] = """
DeleteHistory;
"""
actions['de'] = """
performPolyDeleteElements;
"""                    






#c is for create
actions['c'] = """
CreatePolygonCube;
"""
actions['ci'] = """
toggleCreateNurbsPrimitiveAsTool;
toggleCreatePolyPrimitiveAsTool;
"""
actions['cs'] = """
CreatePolygonSphere;
"""
actions['ccy'] = """
CreatePolygonCylinder;
"""
actions['cns'] = """
CreateNURBSSphere;
"""
actions['cp'] = """
CreatePolygonTool;
"""

#cc is for create curves                    
actions['cc'] = """
CVCurveTool;
"""
actions['ccv'] = """
CVCurveTool;
"""
actions['cce'] = """
EPCurveTool;
"""
actions['ccx'] = """
PencilCurveTool;
"""                    
    
#cl is for create lights
actions['cl'] = """
CreateSpotLight;
"""
actions['cls'] = """
CreateSpotLight;    
"""
actions['clp'] = """
CreatePointLight;
"""
actions['clv'] = """
CreateVolumeLight;
"""
actions['cld'] = """
CreateDirectionalLight;
"""
actions['cla.'] = """
CreateAreaLight;
"""
actions['cla'] = """
CreateAmbientLight;
"""                            
actions['clr'] = """
python("mmmmTools.rimLight.create()");
"""


actions['cm'] = """
DistanceTool;
"""


#e is for edit
actions['ei'] = """
instance; scale -1 1 1;
"""
actions['eq'] = """
SlideEdgeTool;
"""
#the next command connects selected edges with a new edge loop
actions['e'] = """
SplitPolygonTool;    
"""
actions['ee'] = """
polySplitRing -ch on -splitType 1 -weight 0.5 -smoothingAngle 0 -fixQuads 1;    
"""
actions['ew'] = """
polyMergeToCenter;
"""
actions['eww'] = """
PolyMerge;
"""
actions['er'] = """
SplitEdgeRingTool;
"""
actions['ec'] = """
polyCollapseEdge;
"""

actions['et'] = """
PolyExtrude;
"""
actions['ebr'] = """
BridgeEdge;
"""
actions['eb'] = """
BevelPolygon;
"""
actions['ef'] = """
FillHole;
"""
actions['ed'] = """
DuplicateFace;
"""
actions['es'] = """
SculptGeometryTool;
"""
actions['ex'] = """
ExtractFace;
"""
actions['ess'] = """
SeparatePolygon;
"""
actions['ecl'] = """
SeparatePolygon;
"""
actions['ess'] = """
SeparatePolygon;
"""
actions['e3'] = """
tearOffPanel "Component Editor" "componentEditorPanel" true;
"""
#add mirron geometra



#n is for normals
actions['n'] = """
polySoftEdgeWin;
"""    
actions['ns'] = """
SoftPolyEdgeElements 1;
"""                    
actions['nh'] = """
SoftPolyEdgeElements 0;
"""            
actions['nr'] = """
ReversePolygonNormals;
"""        
actions['nu'] = """
polyNormalPerVertex -ufn true;
"""



#t is for transforms
actions['tf'] = """
performFreezeTransformations(0);
"""
actions['tc'] = """
CenterPivot;
"""
actions['th'] = """
HKLTOptionBox();
"""
actions['tk'] = """
HKLocalToolsAction();
"""
actions[']'] = """
HKLocalToolsAction();
"""




#v is for views        
actions['vx'] = """
//This mel script toggles the xray mode for the current panel 


//gets current selected panel

$currentPanel = `getPanel -withFocus`;

$state = `modelEditor -q -cameras $currentPanel`;

modelEditor -edit -cameras (!$state) $currentPanel;



//get the state of xray mode (either on or off)

$state = `modelEditor -q -xray $currentPanel`;

//set it to the opposite state

modelEditor -edit -xray (!$state) $currentPanel;    
"""
#vr is for refresh            
actions['vrt'] = """
reloadTextures();

"""
actions['vrp'] = """
psdUpdateTextures;
"""    






#u is for utilities
actions['uf'] = """
FileTextureManager;
"""

actions['ftm'] = """
FileTextureManager;
"""        

#HK Local Tools is in the transform section
#add rename script (Henson's?)
#add multirename



#o is for OMToolBox
actions['ol'] = """
OMT_to_selectLoop;
"""
actions['or'] = """
OMT_to_selectRing;
"""
actions['oc'] = """
OMT_to_connectComponents;
"""




#o is for nodes (Mostly render nodes)
actions['nl'] = """
shadingNode -asShader lambert;
"""
actions['nao'] = """
mrCreateCustomNode -asTexture "" mib_amb_occlusion;
"""
actions['nf'] = """
shadingNode -asTexture file;
"""
actions['nbc'] = """
shadingNode -asUtility blendColors;
"""
actions['nlu'] = """
shadingNode -asUtility luminance;
"""
actions['nra'] = """
shadingNode -asTexture ramp;

"""
actions['nrc'] = """
shadingNode -asUtility remapColor;
"""
actions['nrh'] = """
shadingNode -asUtility remapHsv;
"""
actions['nrv'] = """
shadingNode -asUtility remapValue;
"""
actions['nsi'] = """
shadingNode -asUtility samplerInfo;
"""
actions['nr'] = """
shadingNode -asUtility reverse;
"""
actions['n2d'] = """
shadingNode -asUtility place2dTexture;
"""
actions['n3d'] = """
shadingNode -asUtility place3dTexture;
"""
actions['nlu'] = """
shadingNode -asTexture layeredTexture;
"""
actions['nps'] = """
shadingNode -asTexture psdFileTex;
"""
actions['np'] = """
shadingNode -asUtility projection;
"""
actions['nsl'] = """
shadingNode -asUtility surfaceLuminance;
"""
actions['nmi'] = """
mrCreateCustomNode -asShader "" mia_material;
"""


#add:  isolatate selection (joe's script) , make planar tools,  basic mappings,  align to world/origin, average verticies, make and break light links, delete constraint, 3d paint tool
# spin edge, Wedge 


actions['selectTextureBorderEdges'] = """
python("selectTextureBorderEdges.selectTextureBorderEdges();")
"""