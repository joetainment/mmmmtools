## MmmmTools   -  Usability Improvements For Maya
## Copyright (C) <2008>  Joseph Crawford
##
## This file is part of MmmmTools.
##
## MmmmTools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MmmmTools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
################################################
## More information is available:
## MmmmTools website - http://celestinestudios.com/mmmmtools
################################################

## Python doc string
"""MmmmToolsUtils - Common Simple Functions For Use In MmmmTools
"""

####################
## Imports
####################
import traceback
import os
import sys
import copy as Copy


import unipath

Unipath = unipath.Path



class Utils(object):
    logModeDefault = 'file'
    logImportanceDefault = 15
    logMinImportance = 10
    
    @classmethod
    def log( cls, *args, **kargs ):
        if kargs.setdefault( 'mode', cls.logModeDefault )=='print':
            im = kargs.setdefault( 'importance', cls.logImportanceDefault )
            if im >= cls.logMinImportance:
                for v in args:
                    print( v )
                trc = traceback.format_exc()
                if trc != 'None\n':  ## The traceback module tacks
                                     ## a newline on format_exc
                    print( "Traceback:")
                    print( trc )
                
    


        
        