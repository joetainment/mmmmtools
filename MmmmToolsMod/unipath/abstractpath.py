"""unipath.py - A two-class approach to file/directory operations in Python.

Full usage, documentation, changelog, and history are at
http://sluggo.scrapping.cc/python/unipath/

(c) 2007 by Mike Orr (and others listed in "History" section of doc page).
Permission is granted to redistribute, modify, and include in commercial and
noncommercial products under the terms of the Python license (i.e., the "Python
Software Foundation License version 2" at 
http://www.python.org/download/releases/2.5/license/).

Note that this version has been modified from the official
release by Joe Crawford for the MmmmTools project.

"""


import os

from MmmmToolsMod.unipath.errors import UnsafePathError

__all__ = ["AbstractPath"]

# Use unicode strings if possible
_base_no_relative_to = os.path.supports_unicode_filenames and unicode or str

class _base( _base_no_relative_to ):
    ## The code was unnecessary and caused problems on linux. Kept for info.
        #__slots__ = ['_relative_to']
            ## **** technically this isn't immutable,
            ## but as long as we don't abuse it by changing it,
            ## python will still allow us to use _base an an immutable
            ## for things like keys etc
        #def __new__(*args, **kargs):
        #    super(currentclass, cls).__new__(cls[, ...])
    @property
    def relative_to(self):
        return self._relative_to
        
        
class AbstractPath(_base):
    """An object-oriented approach to os.path functions."""
    pathlib = os.path
    auto_norm = False

    #### Special Python methods.
    def __new__(class_, *args, **kw):
        norm = kw.pop("norm", None)
        relative_to = kw.pop('relative_to', None )
        relative_allowed = ('relative_allowed', True )
        #fix relative_to
        ## when things are paths they should have slashes on the end!
        ## put them there
        if relative_allowed:
            try:
                relative_to = relative_to.fix_path_to_end_in_sep()
            except:
                if not relative_to is None:
                    if not relative_to.endswith( os.sep ) and len(relative_to)>0:        
                        relative_to = relative_to + os.sep
        else:
            relative_to = None
        
        if norm is None:
            norm = class_.auto_norm
        if kw:
            kw_str = ", ".join(kw.iterkeys())
            raise TypeError("unrecognized keyword args: %s" % kw_str)
        nargs = []
        for arg in args:
            if isinstance( arg, class_ ):
                if not arg.relative_to is None:
                    if relative_to is None and relative_allowed == True:
                        relative_to = arg.relative_to
            nargs.append( arg )
        

        ## This is an extra guard, for good measure
        if not relative_allowed:
            relative_to = None
        
        newpath = class_._new_helper(nargs, relative_to=relative_to)

        if isinstance(newpath, class_):
            newpath._relative_to = relative_to
            return newpath
            
        if norm:
            newpath = class_.pathlib.normpath(newpath)
            # Can't call .norm() because the path isn't instantiated yet.
                
        to_return = _base.__new__(class_, newpath)
        to_return._relative_to = relative_to
        return to_return

    def __add__(self, more):
        try:
            resultStr = _base.__add__(self, more)
        except TypeError:  #Python bug
            resultStr = NotImplemented
        if resultStr is NotImplemented:
            return resultStr
        return self.__class__(resultStr)
 
    @classmethod
    def _new_helper(class_, args, relative_to=None):
        pathlib = class_.pathlib
        # If no args, return "." or platform equivalent.
        if not args:
            if not relative_to is None:
                return relative_to
            else:
                return pathlib.curdir
        # Avoid making duplicate instances of the same immutable path
        if len(args) == 1 and isinstance(args[0], class_) and \
            args[0].pathlib == pathlib and relative_to==None:
            return args[0]
        legal_arg_types = (class_, basestring, list, int, long)
        args = list(args)
        for i, arg in enumerate(args):
            if not isinstance(arg, legal_arg_types):
                m = "arguments must be str, unicode, list, int, long, or %s"
                raise TypeError(m % class_.__name__)
            if isinstance(arg, (int, long)):
                args[i] = str(arg)
            elif isinstance(arg, class_) and arg.pathlib != pathlib:
                arg = getattr(arg, components)()   # Now a list.
                if arg[0]:
                    reason = ("must use a relative path when converting "
                              "from '%s' platform to '%s': %s")
                    tup = arg.pathlib.__name__, pathlib.__name__, arg
                    raise ValueError(reason % tup)
                # Fall through to convert list of components.
            if isinstance(arg, list):
                args[i] = pathlib.join(*arg)
        return pathlib.join(*args)
        
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, _base(self))

    def norm(self):
        return self.__class__(self.pathlib.normpath(self))

    def expand_user(self):
        return self.__class__(self.pathlib.expanduser(self))
    
    def expand_vars(self):
        return self.__class__(self.pathlib.expandvars(self))
    
    def expand(self):
        """ Clean up a filename by calling expandvars(),
        expanduser(), and norm() on it.

        This is commonly everything needed to clean up a filename
        read from a configuration file, for example.
        """
        newpath = self.pathlib.expanduser(self)
        newpath = self.pathlib.expandvars(newpath)
        newpath = self.pathlib.normpath(newpath)
        return self.__class__(newpath)

    #### Properies: parts of the path.

    @property
    def parent(self):
        """The path without the final component; akin to os.path.dirname().
           Example: Path('/usr/lib/libpython.so').parent => Path('/usr/lib')
        """
        return self.__class__(self.pathlib.dirname(self))
    
    @property
    def name(self):
        """The final component of the path.
           Example: path('/usr/lib/libpython.so').name => Path('libpython.so')
        """
        return self.__class__(self.pathlib.basename(self))
    
    @property
    def stem(self):
        """Same as path.name but with one file extension stripped off.
           Example: path('/home/guido/python.tar.gz').stem => Path('python.tar')
        """
        return self.__class__(self.pathlib.splitext(self.name)[0])
    
    @property
    def ext(self):
        """The file extension, for example '.py'."""
        return self.__class__(self.pathlib.splitext(self)[1])

    #### Methods to extract and add parts to the path.

    def split_root(self):
        """Split a path into root and remainder.  The root is always "/" for
           posixpath, or a backslash-root, drive-root, or UNC-root for ntpath.
           If the path begins with none of these, the root is returned as ""
           and the remainder is the entire path.
        """
        P = self.__class__
        if hasattr(self.pathlib, "splitunc"):
            root, rest = self.pathlib.splitunc(self)
            if root:
                if rest.startswith(self.pathlib.sep):
                    root += self.pathlib.sep
                    rest = rest[len(self.pathlib.sep):]
                return P(root), P(rest)
                # @@MO: Should test altsep too.
        root, rest = self.pathlib.splitdrive(self)
        if root:
            if rest.startswith(self.pathlib.sep):
                root += self.pathlib.sep
                rest = rest[len(self.pathlib.sep):]
            return P(root), P(rest)
            # @@MO: Should test altsep too.
        if self.startswith(self.pathlib.sep):
            return P(self.pathlib.sep), P(rest[len(self.pathlib.sep):])
        if self.pathlib.altsep and self.startswith(self.pathlib.altsep):
            return P(self.pathlib.altsep), P(rest[len(self.pathlib.altsep):])
        return P(""), self

    def components(self):
        # @@MO: Had to prevent "" components from being appended.  I don't
        # understand why Lindqvist didn't have this problem.
        # Also, doesn't this fail to get the beginning components if there's
        # a "." or ".." in the middle of the path?
        root, loc = self.split_root()
        components = []
        while loc != self.pathlib.curdir and loc != self.pathlib.pardir:
            prev = loc
            loc, child = self.pathlib.split(prev)
            #print "prev=%r, loc=%r, child=%r" % (prev, loc, child)
            if loc == prev:
                break
            if child != "":
                components.append(child)
            if loc == "":
                break
        if loc != "":
            components.append(loc)
        components.reverse()
        components.insert(0, root)
        return [self.__class__(x) for x in components]

    def ancestor(self, n):
        p = self
        for i in range(n):
            p = p.parent
        return p

    def child(self, *children):
        # @@MO: Compare against Glyph's method.
        for child in children:
            if self.pathlib.sep in child:
                msg = "arg '%s' contains path separator '%s'"
                tup = child, self.pathlib.sep
                raise UnsafePathError(msg % tup)
            if self.pathlib.altsep and self.pathlib.altsep in child:
                msg = "arg '%s' contains alternate path separator '%s'"
                tup = child, self.pathlib.altsep
                raise UnsafePathError(msg % tup)
            if child == self.pathlib.pardir:
                msg = "arg '%s' is parent directory specifier '%s'"
                tup = child, self.pathlib.pardir
                raise UnsafePathError(msg % tup)
            if child == self.pathlib.curdir:    
                msg = "arg '%s' is current directory specifier '%s'"
                tup = child, self.pathlib.curdir
                raise UnsafePathError(msg % tup)
        newpath = self.pathlib.join(self, *children)
        return self.__class__(newpath)

    def norm_case(self):
        return self.__class__(self.pathlib.normcase(self))
    
    def isabsolute(self):
        """True if the path is absolute.
           Note that we consider a Windows drive-relative path ("C:foo") 
           absolute even though ntpath.isabs() considers it relative.
        """
        return bool(self.split_root()[0])
