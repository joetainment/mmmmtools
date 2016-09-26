## First we show a prompt window
## it returns results typed by the user
## and returns None if the user cancels
## or enters nothing

userChosenName = MmmmTools.UiUtils.prompt(
 title="Cube Creator",
 msg="""
Enter a name for a new cube:
        
A number on the end will be added if
the name already exists.

Also, a valid Maya name string must be used,
for example, it must start with a letter,
not a number.
"""
)

## We only proceed if the user entered
## something in and hit OK
if userChosenName!=None:
    cubeList = pm.polyCube()
    cubeXform = cubeList[0]
    cubeXform.rename( userChosenName )



    
    

    
## The section below is just for informative purposes.    
"""
The section below is just for informative purposes.
In case you want to know what the prompt function does,
it looks like this:


def prompt( msg='', opts=None, typeToReturn=None, returnEmptyStringAsNone=True, **kargs ):
    if opts is None:
        opts = kargs

    opts.setdefault( 'message', msg )
    opts.setdefault( 'title', 'Maya' )
    opts.setdefault( 'button', [ 'OK', 'Cancel'] )   
    opts.setdefault( 'dismissString', 'Cancel' )        

    result = pm.promptDialog(**opts)
    if result == 'OK':
        text = pm.promptDialog(query=True, text=True)
    else:
        text =  None
    
    if returnEmptyStringAsNone:
        ## at this point text should always be in string-like form
        ## it won't be an int or float or something yet
        ## so it's safe to test it this way
        if not text:  
            text = None
    
    if not text is None:
        if typeToReturn == 'string':
            text = str(text)
        if typeToReturn == 'float':
            text = float(text)
        elif typeToReturn=='int':
            text = int(text)
        return text
    else:
        return text
"""
pass