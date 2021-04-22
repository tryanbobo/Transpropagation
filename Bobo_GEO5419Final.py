import arcpy
from arcpy.sa import *
from ExtractData import LicenseError


path = r"C:\Users\tb1302\Documents\GEO5419\Project\data"
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True


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

    #apFc = path + "\WAP_StudyArea.shp"
    apFc = path + "\RADIO_POINTS_TXST.shp"
    rast = path + r"\dem_quad_50cm\dem_quad_50cm.tif"
    studyArea = "\StudyArea.shp"
    ############################Radio Variables############################
    #specs for ruckus T610(used at TXST): Gt = 6dBm, Pt = 28dBm
    #Frequency
        #ISM (2.4-2.484GHz)
        #U-NII-1 (5.15-5.25GHz)
        #U-NII-2A (5.25-5.35GHz)
        #U-NII-2C (5.47-5.725GHz)
        #U-NII-3 (5.725-5.85GHz)
    #Gain:
        # Up to 6dBm
    Gt = 6 #0.0079432823472#6 #Watts or 6 dBm #Transmitter Gain () convert from decibels to a power ratio
    Gr = 2 #0.0031628 #Watts#2-5 dBd common with mobile phones#Receiver Gain () convert from decibels to a power ratio
    Pt = 28# 1 Watts or 28dBm (Transmitter Power (Watts))
    #Pr = to value we are solving for is measured in Watts
    c = 299792458 # speed of light in m/s
    f = 2400000000
    lambduh = 0.1249 #c/f # = c/f (c=speed of light in m/s & f=frequency in Hz)
                    # c = 300,000,000 m/s


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

        #outFriis = Gt * Gr * Pt * Square(lambduh / 4 * math.pi * (outEucDistance * .3048))
        outFriis = Gt + Gr + Pt + (20 *Log10(lambduh / (4 * 3.14 * outEucDistance * .3048)))
        print("Created Friis calculation of layer %s" % FID)
        #outFriis.save("friisOut%s.tif" %FID)
        # Convert WATTS to dBm: 10 * Log10(1000*"rssW")
        #convertdBm = 10 * Log10(1000*outFriis)
        #convertdBm.save("friisOutdBm%s" %FID)
        #print("Converted Watts to dBm for layer %s" % FID)

        viewShed = Viewshed(rast, "indLyr%s"%FID)
        #viewShed.save("viewShedOut%s" %FID)

        friisView = viewShed * outFriis
        friisView.save("friisView%s.tif" %FID)
        friisList = []
        friisList.append(str(friisView))
    outCellStats = CellStatistics(friisList, "MEAN", "NODATA", "SINGLE_BAND")
    outCellStats.save("CellStats.tif")
eucDistance()
