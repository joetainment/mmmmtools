class UvSnapshotUi(object):
    def __init__(self):
        self.win = pm.window( "UvSnapshot Ui" )
        with self.win:
            self.col = pm.columnLayout()
            
            with self.col:
                self.warningLabel = pm.text( "THIS SCRIPT IS NOT WORKING YET - DONT USE IT\n\n\n" )
            
                self.nameLabel = pm.text( "Name:" )
                self.nameField = pm.textField( "snapshot" )
                
                self.rangeLabel = pm.text( "Range:" )
                
                self.rangeField = pm.intField( )
                self.rangeFieldX = pm.intField( )
                self.rangeFieldY = pm.intField( )
                
                self.exportButton = pm.button( "Export Snapshots!" )
        self.win.show()
        
    def exportSnapshot(self):    
        user_range = self.rangeField.getValue()
        user_range_x = self.rangeFieldX.getValue()
        user_range_y = self.rangeFieldY.getValue()
        """
        for i in range (0, user_range ):
            x=str(1001+i);
            cmds.uvSnapshot( o=True, uMin=i, uMax=i+1, vMin=0, vMax=1, xr=4096, yr=4096, n="D:/Texturing200/002_Mari_Challenge/Substance/Textures/UV_Snapshots/" + name + x +".iff" );
            y=str(1011+i);
            cmds.uvSnapshot( o=True, uMin=i, uMax=i+1, vMin=1, vMax=2, xr=4096, yr=4096, n="D:/Texturing200/002_Mari_Challenge/Substance/Textures/UV_Snapshots/" + name + y +".iff" );        
        """    
x = UvSnapshotUi()