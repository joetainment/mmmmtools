from . import unipath as Mod_unipath
Unipath = Mod_unipath.Path

class Utils(object):
    @staticmethod
    def dict_to_list( d ): ## d is a dict
        assert type(d)==type({})
        ks = d.keys()
        ks = sorted(ks)
        l = [ d[k] for k in ks ]
        assert type(l)==type([])
        return l
        
    @staticmethod    
    def dict_merge( d1, d2 ):
        if d1 is None and d2 is None:
            return {}
        elif d1 is None:
            return dict( d2.items() )
        elif d2 is None:
            return dict( d1.items() )
            
        return dict( d1.items() + d2.items() )
        
    @staticmethod    
    def opts_merge( kargs, opts):
        if kargs is None:
            kargs = {}
        #print( type(opts) )
        #print( type(kargs) )
        return Utils.dict_merge( kargs, opts )
        
    @staticmethod
    def set_kargs_defaults( kargs , defaults ):
        for v in defaults:
            kargs.setdefault(v[0], v[1])
                ## setdefault description from docs:
                    ## a[k] if k in a, else x (also setting it)
                ## Similar to:
                    ##kargs[ v[0] ] = kargs.get( v[0], v[1] )
                        ## from docs:  a[k] if k in a, else x
        return kargs
        
    @staticmethod
    def debug_print( *args, **kargs ):
        for v in args:
            print( v )

            
    @staticmethod
    def newDuck():
        return Duck()
    
    @staticmethod
    def copyMemberRefsByName( source, target, names ):
        for v in names:
            try:
                target.__dict__[v] = source.__dict__[v]
            except:
                u.log( "Unable To Copy named member ref for name: " + str(v) )
                
        

    
        
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
        #Utils.log( 'Adding paths::::' )
        #Utils.log( 'Self upath is:' )
        #Utils.log( self.upath )
        #Utils.log( 'Other is:' )
        #Utils.log( other )
        #Utils.log( "Other's type is:" )
        #Utils.log( type(other) )
        
    
        new_pather = Copy.deepcopy( self )
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
            #Utils.log( "Other as unipath - o_upath is:" )
            #Utils.log( o_upath )
            new_pather.upath = Unipath( self.upath, o_upath)
        else:
            assert 1 == 0
        #Utils.log( "New combined path is:" )
        #Utils.log( new_pather.upath )
        
        #Utils.log( "New pather upath is:" )
        #Utils.log( new_pather.upath )
        #Utils.log( "New pather upath's type is:" )
        #Utils.log( type(new_pather.upath) )
        return new_pather    
        
        
    def __str__(self):
        return str( self.upath.absolute() )
        
    def str(self):
        return str(self)
        
    def repr(self):
        return( "Pather('" + str(self) + "')" )
        
    
        

class Duck(object):
    """
    A mostly empty class that is just used for organization.
    To store various variable in it's __dict__
    We can't use object directly, so we need to make something that
    inherits from it.
    """
    pass        
        
                