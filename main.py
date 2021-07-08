##
# Demonstration of loading external file with library functions
# The file structure is 
#blendfile
# ... lib
# 
#
# The file is saved as alpha.py with the function report_alpha

 
#def report_alpha(T):
#    print("calling from alpha")
#    print(T)
    
    

import bpy, os, sys, importlib

dir = os.path.dirname(bpy.data.filepath)+"\lib"
sys.path.append(dir)
import alpha
from alpha import report_alpha
# must be run twice to pick up changes from edits to alpha.py
importlib.reload(alpha)

print(dir)

alpha.report_alpha("fred")
report_alpha("ted")

