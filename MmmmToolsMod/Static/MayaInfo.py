## core importsimport sys, osimport pymel.all as pmimport maya.cmds as cmdsimport maya.OpenMaya as om## relative imports, fairly coreimport MmmmToolsMod ## needed for unipathdef getMayaPath():        appEnvFile = pm.about(env=True)        pathstr, file = os.path.split(appEnvFile)        upath = MmmmToolsMod.unipath.Path( pathstr ).absolute()        Pather = MmmmToolsMod.Static.Classes.Pather        pather = Pather.Pather( upath )        return pather        def getMainWindowInfo():        info = MmmmTools.Static.Classes.Duck.Duck()        mw = pm.getMelGlobal('string', 'gMainWindow')                setattr( info, 'mainWindowName', mw )        setattr( info, 'mainWindow', ui )        return info        def getMainWindow():    return  pm.getMelGlobal('string', 'gMainWindow')def getPyUi( uiNameString ):    return pm.PyUI( uiNameString )