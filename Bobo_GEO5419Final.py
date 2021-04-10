import arcpy
from arcpy import env
from arcpy.sa import *

path = r"C:\Users\tb1302\Documents\GEO5419\Project\data"
dataOut = path + "\dataOut"
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True

def eucDistance():
    apFc = path + "\WAP_StudyArea.shp"
    rast = path + r"\dem_quad_50cm\dem_quad_50cm.tif"
    studyArea = "\StudyArea.shp"

    FIDnum = []
    #cursor = arcpy.SearchCursor(apFc, ["FID"])
    #for row in cursor:
    with arcpy.da.SearchCursor(apFc, ["FID"]) as cursor:
        for row in cursor:
            FIDnum.append(row[0])
        #MakeFeatureLayer_management()
        #out = arcpy.MakeFeatureLayer_management(row[0], "indWAP%s" %i)
        #CopyFeatureLayer_management()
        #arcpy.CopyFeatures_management(out, "WAPout%s" %i)
        #print("Created layer %s" %i)
    for FID in FIDnum:

        arcpy.MakeFeatureLayer_management(apFc, "indLyr%s"%FID, "\"FID\" = %s" %FID)
        #arcpy.CopyFeatures_management("indLyr%s"%FID, "WAPLyrOut%s"%FID)
        print("Created layer %s" %FID)
        outEucDistance = EucDistance("indLyr%s"%FID, cell_size = rast)
        outEucDistance.save('dist_%s' %FID)

eucDistance()


