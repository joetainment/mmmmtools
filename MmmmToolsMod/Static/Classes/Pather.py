import MmmmToolsMod.Staticfrom MmmmToolsMod.unipath import Path as Unipathimport copy   
class Pather(object):
    
    @property
    def st(self):
        return str(self)
    @property
    def str_(self):
        return str(self)
    
    def __init__(self, upath=None, relative_to=None):
        if upath is None:
            self.upath = Unipath( relative_to=relative_to)
        else:
            self.upath = Unipath( upath, relative_to=relative_to )
            
    def __call__(self, string=True, absolute=True):
        return self.getPathname( string=string, absolute=absolute )
    
    def isabsolute(self):
        return self.upath.isabsolute()
        
    def get(self):
        return self.upath()
        
    def set_relative_to(self):
        assert 0==1
        
    def set( self, upath, relative_to=None ):
        self.upath = upath
        if not upath.isabsolute():
            if not relative_to is None:
                assert isinstance( relative_to, Unipath )
                self.relative_to = relative_to
            else:
                assert 1 == 0
        else:
            self.relative_to = None
        return self

    def getPathname( string=True, absolute=True ):
        """
            returns the entire file path and file name, can be used to access a file directly
            if string==True, return as string, else as path
            if absolute==True, return absolute path, else relative        
        """
        if absolute:
            upath = self.upath.absolute()
        else:
            upath = self.upath.relative()  ## does this even always work??? **** test this
        
        if string:
            return str(upath)
        else:
            return upath
            
    def makeAbsolute(self):
        self.upath = self.upath.absolute()
        return self
        
    def __add__(self, other ):
        #print( 'Adding paths::::' )
        #print( 'Self upath is:' )
        #print( self.upath )
        #print( 'Other is:' )
        #print( other )
        #print( "Other's type is:" )
        #print( type(other) )
        
    
        new_pather = copy.deepcopy( self )
        if isinstance( other, Pather ):
            assert not other.upath.isabsolute()
            new_pather.upath = Unipath(self.upath, other.upath)
        elif isinstance( other, Unipath ):
            if other.isabsolute():
                assert 1==0
            else:
                new_pather.upath = Unipath(self.upath, other)                
        elif isinstance( other, str ) or isinstance( other, unicode ):
            other = str(other)
            o_upath = Unipath( other )
            #print( "Other as unipath - o_upath is:" )
            #print( o_upath )
            new_pather.upath = Unipath( self.upath, o_upath)
        else:
            assert 1 == 0            
        #print( "New combined path is:" )
        #print( new_pather.upath )
        #print( "New pather upath is:" )
        #print( new_pather.upath )
        #print( "New pather upath's type is:" )
        #print( type(new_pather.upath) )
        return new_pather    
        
        
    def __str__(self):
        return str( self.upath.absolute() )
        
    def str(self):
        return str(self)
        
    def repr(self):
        return( "Pather('" + str(self) + "')" )
        
        