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

import pymel.all as pm
class AutosaveEnabler(object):
    def __init__(self, go=False):
        if go==True:
            self.go()
    def go(self):
        pm.mel.eval( "optionVar -iv autoSaveEnable true;" )
        pm.mel.eval( "optionVar -iv autoSaveLimitBackups true;" )
