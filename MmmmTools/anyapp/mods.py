import sys as Sys
Mod_self = Sys.modules[__name__]

class Import_error_info(object):
    def __init__(self, msg, name):
        ##self.time = time
        self.msg = msg
        self.name = name

class Importer(object):

    import_errors = []
    import_errors_max_count = 100
    mods_dict = {'Mod_mods':Mod_self}

    ## This object should have
    ## no instance properties/members, only static members
    ## instance methods are ok
    
    @classmethod
    def get_class(cls,name):
        return cls
    
    @classmethod
    def i(cls,name):
        try:
            mod = __import__(name)
        except:
            mod = None
            try:
                traceback = __import__('traceback')
                msg = traceback.format_exc()
            except:
                msg = \
                  "An error occured when importing name"\
                  "name was:\n"\
                  + name\
                  + "name was of type:\n" + str( type(name) )
            cls.import_errors.append(  Import_error_info(msg,name)  )
            if len(cls.import_errors) > cls.import_errors_max_count:
                cls.import_errors.pop(0)
            print( msg )
        cls.mods_dict[name] = mod
        return mod

    def __init__(self):
        pass

    def __call__(self, name):
        return self.get_mod(name)
    
    def get_mod(self, name):
        return self.i(name)
    
    def put_mods_to_object(self,
        obj,
        names=None,
        put_mods_dict_to_object = False,
        mods_dict_name = 'Mods',
        make_lowercase=False,
        ):
        
        if names is None:
            return
        mods_dict = self.mods_dict  
        mod_names_to_get = names
        for mod_name in mod_names_to_get:
            mods_dict[mod_name] = self.get_mod(mod_name)
        for mn, mod in mods_dict.items():
            if make_lowercase:
                mn = mn[0].lower() + mn[1:]
            setattr( obj, "Mod_" + mn, mod )
            
        if put_mods_dict_to_object:
            setattr( obj, mods_dict_name, self.mods_dict )
        
        return
        
importer = Importer()