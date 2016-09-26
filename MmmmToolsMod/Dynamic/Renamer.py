import math, sys, os
import re as Regex

import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.all as pm

class Renamer(object):
    def __init__(self,parentRef=None):        self.parent = parentRef

class RenamerRegexTool( object ):
    def __init__(self,parentRef=None, auto_ui=True, autorun=False):
        self.parent = parentRef
        self.mmmm = self.parent
        self.auto_go_ui = auto_ui
        if autorun:
            self.go_ui()
    def go_ui(self):
        if self.ui:
            self.ui = RenamerRegexToolUi(parentRef=self, autorun=True)
    
    def rename(self, toName=None, fromName=None, count=0):
        re = Regex
        objs = pm.ls(selection=True)
        
        for obj in objs:
            nameOld = obj.name()
            nameNew = re.sub( fromName, toName, nameOld, count=count )
            obj.rename( nameNew )


class RenamerRegexToolUi( object ):
    def __init__(self,parentRef=None, autorun=False):
        self.parent=parentRef
        if autorun:
            self.makeUi()
    def makeUi(self):
        self.window = pm.Window(title="Mmmm Renamer")
        with self.window:
            self.col = pm.ColumnLayout( )
            with self.col:
                self.row = pm.RowLayout( numberOfColumns=2  )
                with self.row:
                    self.textFrom = pm.Text( label="Rename regex - from:" )
                    self.textFieldFrom = pm.textField()
                self.row2 = pm.RowLayout( numberOfColumns=2 )
                with self.row2:
                    self.textTo = pm.Text( label="Rename regex - to:" )
                    self.textFieldTo = pm.textField()
                self.row3 = pm.RowLayout( numberOfColumns=2 )
                with self.row3:
                    self.textCount = pm.Text( label = "Count:" )
                    self.intFieldCount = pm.IntField( )
                self.row4 = pm.RowLayout( numberOfColumns=2 )
                with self.row4:
                    self.textRename = pm.Text( label="     " )
                    self.buttonRename = pm.Button(
                        label="Rename Selected",
                        command=lambda x: self.parent.rename(
                            toName=self.textFieldTo.getText(),
                            fromName=self.textFieldFrom.getText(),
                            count=self.intFieldCount.getValue()
                        )
                    )
                self.textHelp = pm.Text( label="""
                
                This is a regular expression based renaming tool.
                It is designed to be extremely powerful, not extremely easy.
                --------------------------------
                
                Count is the maximum number of occurances to replace.
                When count is zero, replacement will be unlimited.
                
                * matches 0 or more (greedy)
                + matches 1 or more (greedy)
                ? matches 0 or 1 (greedy)
                ?* matches 0 or more (non-greedy)
                ?+ matches 1 or more (non-greedy)
                ?? matches 0 or 1 (non-greedy)
                
                
                ^ start of line
                $ end of string
                
                .  any character other than newline
                
                \w any alphanumeric character
                \W any non-alphanumeric character
                \d  any numerical digit
                \D  any non decimal character
                \s  any whitespace
                \S  any non-whitespace
                
                
                |   OR operator:  A|B, will match either A or B.
                
                """)
                
        self.window.show()
    