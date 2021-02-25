import numpy as np
import os
import arcpy
from arcpy import env
env.overwriteOutput = True

parcelSHP = arcpy.GetParameterAsText(0) 
outputFolder = arcpy.GetParameterAsText(1)
outputSHP = arcpy.GetParameterAsText(2) 

if '.shp' not in outputSHP: outputSHP += '.shp'
outputSHP = os.path.join(outputFolder, outputSHP)

#how many random classes
n = int(arcpy.GetParameterAsText(3)) #5

#make copy of original file and add random field
arcpy.management.CopyFeatures(parcelSHP, outputSHP)
arcpy.management.AddField(outputSHP, 'rand', 'SHORT')

#go through new field and add n random classfications
with arcpy.da.UpdateCursor(outputSHP, ('rand')) as cursor:
    for row in cursor:
        row[0] = np.random.randint(n)
        cursor.updateRow(row)
    
del cursor

