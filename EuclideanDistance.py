
import arcpy
def #  NOT  IMPLEMENTED# Function Body not implemented

def Model1():  # Model1

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")

    EastCampWAPs = "EastCampWAPs"

    for Selected_Features, Value in #  NOT  IMPLEMENTED(EastCampWAPs, [], False):

        # Process: Euclidean Distance (Euclidean Distance) 
        Value = "17"
        EDis_Value_ = fr"C:\Users\tb1302\Documents\GEO5418\ProjectFiles\5418Project\5418Project.gdb\EDis{Value}"
        arcpy.gp.EucDistance_sa(in_source_data=Selected_Features, out_distance_raster=EDis_Value_, maximum_distance=None, cell_size="C:\\Users\\tb1302\\Documents\\ArcGIS\\Default.gdb\\Int_txst_50c1_ProjectRaster", out_direction_raster=Output_direction_raster, distance_method="PLANAR", in_barrier_data="", out_back_direction_raster=Out_back_direction_raster)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(cellSize="MAXOF", extent="599542.22 3305380.97 605624.72 3310630.97", mask="EucDist1", 
                          outputCoordinateSystem="PROJCS['NAD_1983_StatePlane_Texas_South_Central_FIPS_4204_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1968500.0],PARAMETER['False_Northing',13123333.33333333],PARAMETER['Central_Meridian',-99.0],PARAMETER['Standard_Parallel_1',28.38333333333333],PARAMETER['Standard_Parallel_2',30.28333333333333],PARAMETER['Latitude_Of_Origin',27.83333333333333],UNIT['Foot_US',0.3048006096012192]]", scratchWorkspace=r"C:\Users\tb1302\Documents\GEO5418\ProjectFiles\5418Project\5418Project.gdb", workspace=r"C:\Users\tb1302\Documents\GEO5418\ProjectFiles\5418Project\5418Project.gdb"):
        Model1()
