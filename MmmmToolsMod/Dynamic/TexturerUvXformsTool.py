import pymel.all as pm



class TexturerUvXformsTool( object ):
    def __init__(self, parentRef=None, auto_ui=False):
        self.parentRef = parentRef
        if auto_ui:
            self.ui_go()
    def ui_go(self):
        self.ui = TexturerUvXformsToolUi(parentRef=self)
        
    def move_uvs( self, u, v ):
        pm.polyEditUV( u=u, v=v )
        
    def scale_uvs( self, s=None, u=None, v=None, pu=0,pv=0 ):
        if not s is None:
            u = s
            v = s
        pm.polyEditUV( su=u, sv=v, pu=pu, pv=pv )
        


class TexturerUvXformsToolUi(object):
    def __init__(self, parentRef=None):
        self.parentRef = parentRef
        #print( 'parent is:')
        #print( self.parentRef )
        self.win = pm.window("UV Xform Tools")
        with self.win:
            self.lay =  pm.formLayout()
            with self.lay:
                labels_x = 0
                self.move_label = pm.text( "Move UVs 1 Space Over" )
                x = 0
                y = 0
                self.lay.attachForm( self.move_label, "left",labels_x )
                self.lay.attachForm( self.move_label, "top", y )
                
                x_orig = 20
                y_orig = 20
                x = x_orig
                y = y_orig
                x_offset_step = 80                
                
                self.move_b1 = pm.button( label="move up", command=lambda x: self.parentRef.move_uvs(0,1) )
                self.move_b2 = pm.button( label="move down", command=lambda x: self.parentRef.move_uvs(0,-1) )
                self.move_b3 = pm.button( label="move left", command=lambda x: self.parentRef.move_uvs(-1,0) )                
                self.move_b4 = pm.button( label="move right", command=lambda x: self.parentRef.move_uvs(1,0) )
                

                self.lay.attachForm( self.move_b1, "left",x )
                self.lay.attachForm( self.move_b1, "top", y )
                x=x+x_offset_step
                self.lay.attachForm( self.move_b2, "left",x )
                self.lay.attachForm( self.move_b2, "top", y )
                x=x+x_offset_step
                self.lay.attachForm( self.move_b3, "left",x )
                self.lay.attachForm( self.move_b3, "top", y )
                x=x+x_offset_step                
                self.lay.attachForm( self.move_b4, "left",x )
                self.lay.attachForm( self.move_b4, "top", y )
                                

                x_orig = 20
                y_orig = 100
                x = x_orig
                y = y_orig
                offset_step_y = 25
                
                self.scale_label = pm.text( "Scale UVs" )
                self.lay.attachForm( self.scale_label, "left",labels_x )
                self.lay.attachForm( self.scale_label, "top", y - 20 )
                
                
                
                self.shrink_b0 = pm.button( label="0.5", command=lambda x: self.parentRef.scale_uvs(s=0.5) )
                self.shrink_b1 = pm.button( label="0.9", command=lambda x: self.parentRef.scale_uvs(s=0.9) )
                self.shrink_b2 = pm.button( label="0.99", command=lambda x: self.parentRef.scale_uvs(s=0.99) )
                self.shrink_b3 = pm.button( label="0.999", command=lambda x: self.parentRef.scale_uvs(s=0.999))
                
                x_orig = 20
                x = x_orig
                y = y_orig
                offset_step_y = 25
                

                self.lay.attachForm( self.shrink_b0, "left",x )
                self.lay.attachForm( self.shrink_b0, "top", y )


                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.shrink_b1, "left", x )
                self.lay.attachForm( self.shrink_b1, "top", y )
                
                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.shrink_b2, "left", x )
                self.lay.attachForm( self.shrink_b2, "top", y )
                
                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.shrink_b3, "left", x )
                self.lay.attachForm( self.shrink_b3, "top", y )
                
                
                
                self.grow_b0 = pm.button( label="2", command=lambda x: self.parentRef.scale_uvs(s=2) )
                self.grow_b1 = pm.button( label="1.1", command=lambda x: self.parentRef.scale_uvs(s=1.1) )
                self.grow_b2 = pm.button( label="1.01", command=lambda x: self.parentRef.scale_uvs(s=1.01))
                self.grow_b3 = pm.button( label="1.001", command=lambda x: self.parentRef.scale_uvs(s=1.001))
                
                
                x_orig = 80
                x = x_orig
                y = y_orig
                offset_step_y = 25
                

                self.lay.attachForm( self.grow_b0, "left",x )
                self.lay.attachForm( self.grow_b0, "top", y )


                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.grow_b1, "left", x )
                self.lay.attachForm( self.grow_b1, "top", y )
                
                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.grow_b2, "left", x )
                self.lay.attachForm( self.grow_b2, "top", y )
                
                x=x+0
                y=y+offset_step_y
                self.lay.attachForm( self.grow_b3, "left", x )
                self.lay.attachForm( self.grow_b3, "top", y )
                
                
                
                
                
if __name__ == "__main__":
    t_ui = TexturerUvXformsTool( auto_ui=True )