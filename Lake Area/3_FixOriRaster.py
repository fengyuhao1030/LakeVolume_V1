import os
import fiona
from osgeo import gdal, gdal_array

lakeRegions = ['0_10N','0_10S','0_30N','0_30S','0_50N','0_50S',
'20E_10N','20E_10S','20E_30N','20E_30S','20E_50N','20E_50S','20E_70N',
'20W_10N','20W_10S','20W_30N','20W_50N','20W_70N',
'40E_10N','40E_10S','40E_30N','40E_30S','40E_50N','40E_70N',
'40W_10S','40W_30S','40W_50N','40W_70N',
'60E_10N','60E_10S','60E_30N','60E_50N','60E_50S','60E_70N',
'60W_10S','60W_30N','60W_30S','60W_50N','60W_50S','60W_70N',
'80E_10N','80E_10S','80E_30N','80E_50N','80E_70N',
'80W_10N','80W_10S','80W_30N','80W_30S','80W_50N','80W_50S','80W_70N','80W_70S',
'100E_10N','100E_10S','100E_30N','100E_30S','100E_50N','100E_50S','100E_70N',
'100W_10N','100W_10S','100W_30N','100W_50N','100W_70N',
'120E_10N','120E_10S','120E_30N','120E_30S','120E_50N','120E_50S','120E_70N',
'120W_10N','120W_30N','120W_50N','120W_70N',
'140E_10S','140E_30N','140E_30S','140E_50N','140E_50S','140E_70N',
'140W_30N','140W_50N','140W_70N',
'160E_30S','160E_50N','160E_50S',
'160W_10S','160W_50N','160W_70N',
'180W_30S','180W_50N','180W_70N']

for i in range(62,len(lakeRegions)):
    lakeRegion = lakeRegions[i]
    inShpFileName = 'E:\\Lake Volume\\Lake Area\\GLWD_Buffer\\Lake_Buffer_Split\\Lake_Buffer_' + lakeRegion + '.shp'
    lakeIDs = []
    with fiona.open(inShpFileName) as inShapeFile:
        for inFeature in inShapeFile:
            lakeID = inFeature['properties']['GLWD_ID']
            lakeIDs.append(lakeID)
    
    inputPath = 'E:\\Lake Volume\\Lake Area\\Occ_Stable\\' + lakeRegion + '\\'
    outputPath = 'E:\\Lake Volume\\Lake Area\\Fix_WaterHistory_Month\\' + lakeRegion + '\\'
    os.mkdir(outputPath)

    count = 1
    for lakeID in lakeIDs:
        stableWaterRasterFile = inputPath + str(lakeID) + '_StableWater.tif'
        if not os.path.exists(stableWaterRasterFile):
            continue
        stableWaterRasterDS = gdal.Open(stableWaterRasterFile)
        stableWaterRasterValues = stableWaterRasterDS.GetRasterBand(1).ReadAsArray()
        stableWaterRasterValues[stableWaterRasterValues == 1] = 2
        stableWaterRasterValues[stableWaterRasterValues == 0] = 1
        for tempYear in range(2003,2020):
            for tempMonth in range(1,13):
                currentRasterFile = inputPath + str(lakeID) + '_' + str(tempYear) + '_' + str(tempMonth) + '.tif'
                currentRasterDS = gdal.Open(currentRasterFile)
                currentRasterValues = currentRasterDS.GetRasterBand(1).ReadAsArray()
                currentRasterValues[currentRasterValues == 0] = stableWaterRasterValues[currentRasterValues == 0]
                currentRasterValues[stableWaterRasterValues == -1] = -1
                outputFileName = outputPath + str(lakeID) + '_' + str(tempYear) + '_' + str(tempMonth) + '.tif'
                gdal_array.SaveArray(currentRasterValues.astype('int16'),outputFileName,'GTiff',currentRasterDS)
        showInfo = str(count) + '_' + str(len(lakeIDs))
        count = count + 1
        print(showInfo)