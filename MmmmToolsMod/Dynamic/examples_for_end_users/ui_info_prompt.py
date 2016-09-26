### This file demonstrates how to make a simple prompt window
### with information appear.
import MmmmTools


yourWindowTitle="""Your Window Title Goes Here"""

yourMessage="""
This is a message to the user.

It can span several lines if you like.

It can contain long paragraphs, but doesn't have to.  Generally in your python code, this should be written as a triple quoted string assigned to a varible outside any function. Then the indentation won't be wrong.  When you call the infoPrompt function, simply use the variable as the msg argument.

"""


MmmmTools.UiUtils.infoPrompt( msg = yourMessage, title = yourWindowTitle )
pass