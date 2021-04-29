import arcpy
import sys
from arcpy.sa import *
from ExtractData import LicenseError

path = r"C:\Users\tb1302\Documents\GEO5419\Project\data"
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True

#Check out Spatial Extension
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

def transProp():

    # User defined radio points layer input
    apFc = arcpy.GetParameterAsText(0)
    # User defined DEM input
    rast = arcpy.GetParameterAsText(1)

    ### User defined Friis Transmission Equation Variables
    # dBi: Transmitter Gain
    Gt = arcpy.GetParameter(2)
    # dBi: Receiver Gain
    Gr = arcpy.GetParameter(3)
    #dBm: Transmitter power output
    Pt = arcpy.GetParameter(4)
    #Pr = to value we are solving for is measured in Watts
    c = 299792458 # speed of light in m/s
    f = (arcpy.GetParameter(5) * 1000000000) #Frequency -- convert Ghz to Hz
    lambduh = c/f #speed of light in m/s & f=frequency in Hz

    # Empty list to hold the output name after joining Friis output and Vewshed
    friisList = []
    # Empty list to hold FID -- used for iterating through individual features
    FIDnum = []
    # Call search cursor with FID field
    with arcpy.da.SearchCursor(apFc, ["FID"]) as cursor:
        for row in cursor:
            # Append Each FID to FIDnum list
            FIDnum.append(row[0])
    # Iterate through FIDs
    for FID in FIDnum:
        try:
            # Create separate feature layer for each point in the input feature class
            arcpy.MakeFeatureLayer_management(apFc, "indLyr%s"%FID, "\"FID\" = %s" %FID)
            # arcpy.CopyFeatures_management("indLyr%s"%FID, "WAPLyrOut%s"%FID)
            print("Created layer %s" %FID)
            arcpy.AddMessage("Created layer %s" %FID)
        except Exception:
            # Error handling
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            # Apply Euclidean Distance to each point individually
            outEucDistance = EucDistance("indLyr%s"%FID, cell_size = rast)
            arcpy.AddMessage("Created Euclidean Distance of layer %s" % FID)
            #outEucDistance.save('dist_%s' %FID)
        except Exception:
            # Error handling
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            # Apply Friis Equation using user input and each Euclidean Distance output converted to meters
            outFriis = Gt + Gr + Pt + (20 *Log10(lambduh / (4 * 3.14 * (outEucDistance * .3048))))
            arcpy.AddMessage("Created Friis calculation of layer %s" % FID)
            #outFriis.save("friisOut%s.tif" %FID)
        except Exception:
            # Error handling
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            # Perform Viewshed Analysis for each feature layer derived from the input feature class
            viewShed = Viewshed(rast, "indLyr%s"%FID)
            arcpy.AddMessage("Created Viewshed of layer %s" % FID)
            # ViewShed.save("viewShedOut%s" %FID)
        except Exception:
            # Error handling
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

        try:
            # Multiply Viewshed and Friis outputs -- Viewshed has a boolean output resuting in an intersect with Friis output
            friisView = viewShed * outFriis
            friisView.save("friisView%s.tif" %FID)
            arcpy.AddMessage("Intersect Viewshed and Friis output for layer %s" % FID)
            # Append output name to aggregate layers with CellStatistics
            friisList.append(str("friisView%s.tif" %FID))
        except Exception:
            # Error handling
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])

    # User input for statistic type used in CellStatistics
    statType = arcpy.GetParameter(6)
    arcpy.AddMessage(statType)
    # loops through user defined statistic type
    for stat in statType:
        # Perform CellStatistics for each statistic type
        outCellStats = CellStatistics(friisList, stat, "NODATA", "SINGLE_BAND")
        # Save output
        outCellStats.save(arcpy.GetParameterAsText(7) + "_%s" %stat[:3])
        arcpy.AddMessage("Aggregated output propagation outputs: %s" %stat)

transProp()
