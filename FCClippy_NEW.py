# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# FCClippy.py
# Created: 05/07/2019
# Updated: 05/15/2019
# Author: Chris Fourroux
# Modified by Mike Murnane on 03/23/2020 for blank spaces in legend layer alias name.
# Usage: FCCClippy <Input_Layers> <co40> <outputLocation>
# <Input_Layers> = multi select Feature Layers that need clipping
# <co40> = single Feature Layer with are to clip
# <outputLocation> = path to output GDB that will contain results.
# Description: Iterates through selected layers in map and clips them to new GDB
# ---------------------------------------------------------------------------


import arcpy, os, re
from datetime import datetime


if __name__ == "__main__":
    try:
        if not arcpy.env.workspace: # if running outside arcmap , set a default
            arcpy.env.workspace = 'Default.gdb'

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        arcpy.AddMessage("Using timestamp " + timestamp)

        # Script arguments
        Input_Layers = arcpy.GetParameterAsText(0)
        if Input_Layers == '#' or not Input_Layers:
            Input_Layers = 'Layer_1;Layer_2' # provide a default value if unspecified

        co40 = arcpy.GetParameterAsText(1)
        if co40 == '#' or not co40:
            co40 = "Clippy.shp" # provide a default value if unspecified

        outputLocation = arcpy.GetParameterAsText(2)
        if outputLocation == '#' or not outputLocation:
            outputLocation = "C:\\Users\\E5570\\Documents\\ArcGIS\\Output Geodatabase.gdb" # provide a default value if unspecified

        clipOut = outputLocation + '\\Clip_shape_' + str(timestamp)
        arcpy.CopyFeatures_management(co40, clipOut)  # copy clip shape to destination
        arcpy.AddMessage("Saved: " + clipOut)

        layer_list = re.split(';', Input_Layers)
        for fc in layer_list:
            fc = fc.replace('\'', '') # replace quotes at beginning and end of some strings
            arcpy.AddMessage("Found: " + fc)
            head, fileName = os.path.split(fc)  # if fc is full path, we need to trim down to just file name
            fileName = fileName.replace('.','_') # '.' doesn't work in a gdb, replace it with '_'
            #arcpy.AddMessage("Unchanged Name: " + fileName)   # Test Modification Message
            fileName = fileName.replace(' ', '_')  # Modification for blank spaces in legend alias ' ' doesn't work in a gdb, replace it with '_'
            arcpy.AddMessage("Name: " + fileName)
            outClip = outputLocation +"\\" + fileName +"_clipped_" + str(timestamp)
            arcpy.Clip_analysis(fc, co40, outClip, "")
            arcpy.AddMessage("Saved: " + outClip)

    except Exception as e:
        # if error at any point, abort!
        arcpy.AddError('{}'.format(e))


