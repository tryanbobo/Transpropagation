import arcpy
import sys
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

    #apFc = path + "\RADIO_POINTS_TXST.shp"
    apFc = arcpy.GetParameterAsText(0)
    #rast = path + r"\dem_quad_50cm\dem_quad_50cm.tif"
    rast = arcpy.GetParameterAsText(1)
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
    Gt = arcpy.GetParameter(2)#6 # dBm Transmitter Gain () convert from decibels to a power ratio
    Gr = arcpy.GetParameter(3)#2 #0.0031628 #Watts#2-5 dBd common with mobile phones#Receiver Gain () convert from decibels to a power ratio
    Pt = arcpy.GetParameter(4)#28# 1 Watts or 28dBm (Transmitter Power (Watts))
    #Pr = to value we are solving for is measured in Watts
    c = 299792458 # speed of light in m/s
    #f = arcpy.GetParameterAsText(5) * 1000000000 #2400000000 # need to convert Ghz to Hz
    lambduh = 0.1249 #c/f (c=speed of light in m/s & f=frequency in Hz)
                    # c = 300,000,000 m/s

    friisList = []
    FIDnum = []

    with arcpy.da.SearchCursor(apFc, ["FID"]) as cursor:
        for row in cursor:
            FIDnum.append(row[0])

    for FID in FIDnum:
        try:
            # create separate feature layer for each point in the input feature class
            arcpy.MakeFeatureLayer_management(apFc, "indLyr%s"%FID, "\"FID\" = %s" %FID)
            #arcpy.CopyFeatures_management("indLyr%s"%FID, "WAPLyrOut%s"%FID)
            print("Created layer %s" %FID)
            arcpy.AddMessage("Created layer %s" %FID)
        except Exception:
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            outEucDistance = EucDistance("indLyr%s"%FID, cell_size = rast)
            print("Created Euclidean Distance of layer %s" % FID)
            arcpy.AddMessage("Created Euclidean Distance of layer %s" % FID)
            #outEucDistance.save('dist_%s' %FID)
        except Exception:
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])
            #apply friis ect. transmission equations...

        try:
            outFriis = Gt + Gr + Pt + (20 *Log10(lambduh / (4 * 3.14 * outEucDistance * .3048)))
            print("Created Friis calculation of layer %s" % FID)
            arcpy.AddMessage("Created Friis calculation of layer %s" % FID)
            #outFriis.save("friisOut%s.tif" %FID)
        except Exception:
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            viewShed = Viewshed(rast, "indLyr%s"%FID)
            arcpy.AddMessage("Created Viewshed of layer %s" % FID)
            #viewShed.save("viewShedOut%s" %FID)
        except Exception:
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            friisView = viewShed * outFriis
            friisView.save("friisView%s.tif" %FID)
            arcpy.AddMessage("Intersect Viewshed and Friis output for layer %s" % FID)
            friisList.append(str("friisView%s.tif" %FID))
        except Exception:
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])


    statType = arcpy.GetParameter(5)
    arcpy.AddMessage(statType)
    count = 0
    #statList = statType.split(";")
    for stat in statType:
        count+= 1
        outCellStats = CellStatistics(friisList, stat, "NODATA", "SINGLE_BAND")
        outCellStats.save(arcpy.GetParameterAsText(6) + "_%s" %stat[:3])
        arcpy.AddMessage("Aggregated output propagation outputs: %s" %stat)
    print(friisList)
eucDistance()
