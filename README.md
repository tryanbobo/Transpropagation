# Transpropagation
**Version 1.0.0**

## Contents
1. [About](#About)
2. [Requirements](#Requirements)
3. [Installation](#Installation)
4. [How it Works](#How-it-works)
5. [Inserting Friis Values](#Inserting-Friis-Values)
6. [Contributors](#Contributors)


## About
Transpropagation is a flexible, custom tool created using ArcGIS’s Arcpy python module. The user interface is created to allow operators to select multiple variables associated with the Friis Transmission Equation as well as multiple aggregate outputs. The aim of this project is to introduce the Transpropagation ArcGIS tool for modeling outside wireless signal propagation and radio signal transmission power. With the ever-growing Internet of Things, reliable network access has become essential in a wide range of computational tasks. Outdoor wireless access is no exception. Wireless access points (WAPs) are radio devices that provide a cost-effective solution for offering network access to many devices; from monitoring vehicle inventory or facility operations to providing internet access to an end user. There is a vast amount of literature and many proprietary solutions for WSP, but often the technology is locked behind a paywall or created using niche software. The significance of this project lies in its ability to provide large scale, customizable WSP modeling that is built atop an established ArcGIS python tool framework (ESRI 2021). 

## Requirements
Access to ESRI's ArcMap or ArcGIS Pro

The two required input parameters include Input Radio Points Feature and an Input DEM.
##### [Back to Contents](#contents)

## Installation
In the Catalog window, ArcToolbox window, or ArcCatalog, navigate to the tool and select it.
##### [Back to Contents](#contents)

## How it works
The user interface is created to allow operators to select multiple variables associated with the FTE as well as multiple aggregate outputs. The two required input parameters include Input Radio Points Feature and an Input DEM. 

![UI](UI.JPG)

The geoprocessing used in the tool include Euclidean Distance, Viewshed, Cell Statistics, and Raster Calculator. The propagation output for each point is derived using a Search Cursor iterating through each radio features FID and adds it to a list. This list is then processed through a for loop. Since the majority of analysis is done on each radio point individually, or a subsequent output associated with it, the bulk of the geoprocessing occurs under this same for loop. Additionally, String formatting is used for each tool utilized to name every output layer using its FID as a unique identifier. First, the MakeFeatureLayer tool is applied so that each radio point is separated into its own Feature Layer. The Euclidean Distance tool is then run on each radio point. This values will be used in the Friis calculation. 

The ArcGIS Viewshed tool was applied to each feature layer extracted taking into consideration the OFFSETA value. The OFFSETA values are populated for each feature of the radio dataset based on each points height values, allowing a more accurate propagation output. Additional options such as, OFFSETB, AZUMUTH1, RADIUS1, etc., are available for users to apply if necessary.The viewshed raster output is binary, where 1 is areas with wave propagation and 0 are areas not reached by the signal. At this point the viewshed output is intersected to the corresponding FTE equation considered above by multiplying the two together. 

The intersected raster outputs for each point feature are then aggregated using Cell Statistics. This process allows users to choose the statistic type and creates an aggregated output for each choice. 


##### [Back to Contents](#contents)

## Inserting Friis Values

Custome Friis Values can be intered directly into the tool . 


![img_2](img_2.png)

*where:* 

Pt is the output power to the transmitting antenna in dBm 

Gt is the antenna gain or the transmitting antenna in dBi, 

Gr is the antenna gain of the receiving antenna in dBi, 

λ is the speed of light divided by the broadcasting frequency of the transmitting antenna.

R is distance between the transmitting and receiving antennas in meters, and 4 is a constant. Pr then is what we are solving for, and output received for each cell, the output power of the transmitting radio.*

##### [Back to Contents](#contents)


## Contributors
Ryan Bobo (tb1302) is the sole contributor at this time