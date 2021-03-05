import os
import glob
import fiona
import rasterio
import rasterio.mask
import numpy as np
from osgeo import gdal, gdal_array
from collections import Counter

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

for i in range(44,45):
    lakeRegion = lakeRegions[i]
    outputPath = 'E:\\Lake Volume\\Lake Area\\Occ_Stable\\' + lakeRegion + '\\'
    os.mkdir(outputPath)
    lakeShpFileName = 'E:\\Lake Volume\\Lake Area\\GLWD_Buffer\\Lake_Buffer_Split\\Lake_Buffer_' + lakeRegion + '.shp'
    lakeIDs = []
    with fiona.open(lakeShpFileName,'r') as inShapeFile: 
        for tempYear in range(2003,2020):
            for tempMonth in range(1,13):
                inRasterFile = 'E:\\Lake Volume\\Lake Area\\WaterHistory_Month\\' + lakeRegion + '\\LB_' + lakeRegion + '_' + str(tempYear) + '_' + str(tempMonth) + '.tif'
                inRasterDS = rasterio.open(inRasterFile)
                for inFeature in inShapeFile:
                    tempShape = [inFeature['geometry']]
                    lakeID = inFeature['properties']['GLWD_ID']
                    outRasterDS, outTransform = rasterio.mask.mask(inRasterDS,tempShape,crop = True)
                    outRasterFile = outputPath + str(lakeID) + '_' + str(tempYear) + '_' + str(tempMonth) + '.tif'
                    outRasterMeta = inRasterDS.meta.copy()
                    outRasterMeta.update({'driver':'GTiff','height':outRasterDS.shape[1],'width':outRasterDS.shape[2],'transform':outTransform})
                    with rasterio.open(outRasterFile,'w',**outRasterMeta) as dest:
                        dest.write(outRasterDS)
                showInfo = str(tempYear) + '_' + str(tempMonth)
                print(showInfo)
        for inFeature in inShapeFile:
            lakeID = inFeature['properties']['GLWD_ID']
            lakeIDs.append(lakeID)
    os.chdir(outputPath)
    dataList = glob.glob('*.tif')
    count = 1
    for lakeID in lakeIDs:
        currentRasterFiles = []
        for tempFileName in dataList:
            findIndex = tempFileName.find('_')
            if int(tempFileName[0:findIndex]) == lakeID:
                currentRasterFiles.append(tempFileName)
        # Occurence
        flag = 0
        validCount = 0
        for j in range(0,len(currentRasterFiles)):
            currentRasterFile = currentRasterFiles[j]
            rasterArray = gdal_array.LoadFile(currentRasterFile)
            rasterSummary = Counter(rasterArray.flatten())
            contaminatedProp = rasterSummary[0]/(rasterSummary[0] + rasterSummary[1] + rasterSummary[2])
            if contaminatedProp > 0.95:
                continue
            else:
                validCount = validCount + 1
                currentRasterDS = gdal.Open(currentRasterFile)
                currentRasterValues = currentRasterDS.GetRasterBand(1).ReadAsArray()
                if flag == 0:
                    resultValue = currentRasterValues.astype('int16')
                    resultObservation = (currentRasterValues > 0).astype('int16')
                    flag = 1
                else:
                    resultValue = resultValue + currentRasterValues.astype('int16')
                    resultObservation = resultObservation + (currentRasterValues > 0).astype('int16')
            if lakeID < 200:
                print(j)
        if validCount == 0:
            continue
        resultValue[resultValue == 0] = -9999
        resultObservation[resultObservation == 0] = -9999
        resultOccurence = (resultValue - resultObservation)/resultObservation
        resultOccurence[resultValue == -9999] = -1
        outputFileName = str(lakeID) + '_Occurence.tif'
        gdal_array.SaveArray(resultOccurence.astype('float32'),outputFileName,'GTiff',currentRasterDS)
        # Stable water
        countNums = []
        for j in range(50,101):
            if j == 100:
                lowLimit = 1
                upLimit = 1
            else:
                lowLimit = j/100 - 0.005
                upLimit = j/100 + 0.005
            findIndex_1 = (resultOccurence >= lowLimit).astype('int16')
            findIndex_2 = (resultOccurence <= upLimit).astype('int16')
            findIndex = findIndex_1 + findIndex_2
            findIndex = (findIndex >= 2).astype('int16')
            countNums.append(sum(sum(findIndex)))
        findIndex = list(np.where(countNums > np.mean(countNums)*0.17)[0])
        if len(findIndex) == 0:
            occThreshold = 0.5
        else:
            occThreshold = findIndex[0]*0.01 + 0.5
        stableWater = resultOccurence
        stableWater[resultOccurence > occThreshold] = 1
        stableWater[resultOccurence <= occThreshold] = 0
        stableWater[resultValue == -9999] = -1
        outputFileName = str(lakeID) + '_StableWater.tif'
        gdal_array.SaveArray(stableWater.astype('int16'),outputFileName,'GTiff',currentRasterDS)
        currentRasterDS = None
        # Show info
        showInfo = str(count) + '_' + str(len(lakeIDs))
        count = count + 1
        print(showInfo)