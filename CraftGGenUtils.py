"""      
CraftGGenUtils Module
Author: Arnaud Cassone

This extension provides utility functions for the GroundGen Plugin.

"""

class CraftGGenUtils:
    def __init__(self):
        """Initialize CraftGGen utility class"""
        pass
    
    def get_op(self, path):
        """Get operator by path"""
        return op(path)

    def SetCloneParameters(self, op):
        """Set clone parameters for a given operator"""
        try:
            if op.par.Autosave is not None:
                op.par.Autosave.destroy()
            if op.par.Save is not None:
                op.par.Save.destroy()
        except:
            pass
        
        # append help button
        op.customPages[1].appendPulse('Help')

        return 
