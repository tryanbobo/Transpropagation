import arcpy
from arcpy import env
from arcpy.sa import *
import math


arcpy.env.workspace = path
arcpy.env.overwriteOutput = True

path = r"C:\Users\tb1302\Documents\GEO5419\Project\data"
dataOut = path + "\dataOut"
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        print("Checked out \"Spatial\" Extension")
    else:
        raise LicenseError
except LicenseError:
    print("Spatial Analyst license is unavailable")
except:
    print(arcpy.GetMessages(2))

def eucDistance():

    apFc = path + "\WAP_StudyArea.shp"
    rast = path + r"\dem_quad_50cm\dem_quad_50cm.tif"
    studyArea = "\StudyArea.shp"
    Gt = 28
    Gr = 3
    Pt = 2.2
    lambduh = .0559

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
        #outEucDistance =
        #how do you make units global for multiple users???
        outEucDistance = EucDistance("indLyr%s"%FID, cell_size = rast)
        print("Created Euclidean Distance of layer %s" % FID)
        #outEucDistance.save('dist_%s' %FID)

        #apply friis ect. transmission equations...
        #if user input picking different eqs
        # Example Friis EQ: 28 * 3 * 2.2 *  Square(.0559 / (4 * 3.14 *  Raster("distMint")))
        # Convert WATTS to dBm: 10 * Log10(1000*"rssW")
        outFriis = Gt * Gr * Pt * Square(lambduh / 4 * math.pi * outEucDistance)
        outFriis.save("friisOut%s" %FID)

eucDistance()


