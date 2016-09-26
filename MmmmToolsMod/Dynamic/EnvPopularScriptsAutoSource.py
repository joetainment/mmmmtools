import pymel.all as pm

from Utils import Utils
u = Utils

def main( caller ):
    """ Takes an MmmmTools instance or another type that has an ini member
    that points to an MmmmTools configuration. This is actually quite specific
    to MmmmTools startup and not a general use funtion.
    """
    conf = caller.ini.conf
    u.log( "Sourcing (running setup for) popular mel scripts." )
    script_filenames = conf.popular_script_filenames_list
    for fn in script_filenames:
        
        try:
            sourceCommand = 'source \\"' + fn + '\\";'
            pm.mel.eval('catchQuiet( eval("' + sourceCommand + '"));')
        except:
            if fn == conf.popular_script_hklt_filename:
                u.log(
                        "HK Local Tools not available for sourcing."
                        " proceeding without it."
                      )
            elif fn == conf.popular_script_goz_filename:
                u.log("""
                Did not source GoZ script.  This most likely means it is not
                installed. If you are a ZBrush user, you may need to use the
                GoZ button in ZBrush to install the GoZ Maya script.
                """)
            else:
                u.log( "Could not source script: " + fn +
                        "  ...proceeding without it." )
        else:
            u.log( "Script sourced: " + fn )