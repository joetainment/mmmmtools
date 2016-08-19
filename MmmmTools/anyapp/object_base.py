from utils import Utils as Utils
import traceback as Traceback
import os as Os
import sys as Sys


"""
This class has very abtract functions to deal with basic things such as inheritance, debugging, etc.
The idea is simply to have something a little more useful than the default python  'object'
See class help.
"""
class Object_base(object):
    """
    Use this class as a base for other types of *non-lightweight* classes.  You can automatically call super class inits etc by using init_bases().
    It also implements a basic options dict that can intelligently merge keyword arguments and pass them to super classes.
    This gets around pythons problem of not passing the default non keyword arguments that weren't specified.
    """
    def __init__(self, *args, **kargs):
        kargs = self.set_kargs_defaults( kargs, [
            [ 'debug', False ],
        ])
        self.opts_merge( kargs )
        self.debug( "Object_base.__init__ running!" )
        
    def debug( self, *args, **kargs ):
        if self.opts['debug'] == True:
            Utils.debug_print( *args, **kargs )

        
    def init_env(self):
        #### **** This stuff needs to get put somewhere else, it doesn't belong in the Object_base
        self.running_module__file_name_with_path = pm1 = Os.path.abspath( __file__ )
        self.running_module__file_name_no_path = pm2 = Os.path.split(self.running_module__file_name_with_path)[-1]
        self.running_module__file_path_only = pm3 = Os.path.split(self.running_module__file_name_with_path)[0]
        
        self.running_script__file_name_with_path = ps1 = Os.path.abspath( Sys.argv[0] )
        self.running_script__file_name_no_path = ps2 = Os.path.split(self.running_script__file_name_with_path)[-1]
        self.running_script__file_path_only = ps3 = Os.path.split(self.running_script__file_name_with_path)[0]    
        
    def set_kargs_defaults( self, kargs, defaults ):
        Utils.set_kargs_defaults( kargs, defaults )
        self.opts_merge(kargs)
        return kargs

    def opts_merge(self, kargs):
        try:
            self.opts
        except:
            self.opts = {}  
        self.opts = Utils.opts_merge( kargs, self.opts )

    def init_object_base(self, *args, **kargs):
        bases = self.init_bases_create_init_completed_bases_list( *args, **kargs )
        name = Object_base.__name__
        if not name in bases:
            bases.append( name )
        Object_base.__init__(self, *args, **kargs)
    
    def init_bases_create_init_completed_bases_list(self,*args,**kargs):
        try:
            tmp = self.init_completed_bases_list
        except:
            self.init_completed_bases_list = [ self.__class__.__name__ ]
        return self.init_completed_bases_list
        
    
    def init_bases(self, *args, **kargs):
        ## The Object_base class always gets initialized first, since just about anything else
        ## might depend on it.
        self.init_object_base(*args,**kargs)        

        bases = self.init_completed_bases_list
        mro = self.__class__.__mro__

        for i,m in enumerate( mro ):
            if i > 0 and (not i == len(mro)-1):
                cls = mro[i]
                cname = cls.__name__
                if not cname in bases:
                    #self.debug( cls )
                    #print( "About to init: ")
                    #print( mro[i].__name__ )
                    #print( 'bases is:' )
                    #print(bases)
                    bases.append( cname ) ## this has to be before the call to __init__
                    mro[i].__init__( self, *args, **kargs )
                        ## this __init__ call must come *after*
                        ## adding the class name to the bases
                        ## list!
                    
        """
        try:
            tmp = self.init_bases_tracking_list
        except:
            self.init_bases_tracking_list = []
        self.opts_merge( kargs )
        try:
            tmp = self.init_bases_dict
        except:
            self.init_bases_dict = {}
        
        try:
            selfRef.init_depth = selfRef.init_depth + 1
        except:
            selfRef.init_depth=0
        """
            
        """
        print( "selfRef.init_depth is: " )            
        print( selfRef.init_depth )
        
        print( "self and selfRef are:" )
        print( self )
        print( selfRef )
        """
        """
        if selfRef.init_depth==0:
        
            mro_list = list(selfRef.__class__.__mro__)
            print( "mro_list is:" )
            for l in mro_list:
                print l
            mro_list.reverse()
            #### Cleaup up mro_list ####
            if type(mro_list[0]) == type(object):
                mro_list.pop(0)
            
            for i in range(len(mro_list)):
                class_to_search_for_super = mro_list[i]
                class_string = str(class_to_search_for_super)

                ## Make sure we haven't already called the init
                if not class_string in self.init_bases_dict.keys():
                    ## couldn't use self.__class__ as first variable because
                    ## if so, the __init__ function gets called with the
                    ## wrong type for self. many other things tried,
                    ## but didn't work.  Thus, this way seems to work best.
                    excepts = []
                    try:
                        sup = super( class_to_search_for_super , selfRef )
                        #print( "Trying to call with self.opts and then kargs" )
                        try:
                            #if not sup.__init__ in self.init_bases_tracking_list:
                                sup.__init__(*args,**self.opts)
                            #self.init_bases_tracking_list.append(sup.__init__)                                
                        except:
                            excepts.append(  Traceback.format_exc()  )
                            #print( "had to call it without self.opts" )
                            try:
                                #if not sup.__init__ in self.init_bases_tracking_list:                          
                                sup.__init__(*args,**kargs)                        
                                #    self.init_bases_tracking_list.append(sup.__init__)                                    
                            except:
                                excepts.append(  Traceback.format_exc()  )
                                #print( "had to call it without kargs")
                                #if not sup.__init__ in self.init_bases_tracking_list:                                              
                                sup.__init__(*args)
                                #    self.init_bases_tracking_list.append(sup.__init__)                              
                    except:
                        excepts.append(  Traceback.format_exc()  )
                        if self.opts['debug'] == True:
                            for v in excepts:
                                print( v )
                ## Add this to the dict of inits that have been run, so we don't call it again
                self.init_bases_dict[ class_string ] = True
        """
    
    ## The function here was an old test function that should no longer be needed.  It is here for reference purposes only.
    #def init_bases_old(self, selfRef, *args, **kargs):
    #    try:
    #        selfRef.init_depth = selfRef.init_depth + 1
    #    except:
    #        selfRef.init_depth=0
    #    ## couldn't use self.__class__ as first variable because if so, the __init__ function gets called with the wrong type for self
    #    ## many other things tried, but didn't work.  Thus, this way seems to work best.
    #    super( list(selfRef.__class__.__mro__)[selfRef.init_depth], selfRef ).__init__(*args,**kargs)             
