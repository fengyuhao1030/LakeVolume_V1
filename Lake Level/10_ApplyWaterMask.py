import os
import glob
import math
import numpy as np
import pandas as pd
from dbfread import DBF
from osgeo import gdal,gdal_array

os.chdir('E:\\Lake Volume\\Lake Level\\GLAH14_SJ')
outputPath = 'E:\\Lake Volume\\Lake Level\\GLAH14_SJ_SJ'
fileNames = glob.glob('*.dbf')

latBreaks = np.linspace(-90,70,9)
lonBreaks = np.linspace(-180,160,18)
for fileName in fileNames:
    dbfTable = DBF(fileName,load = True)
    lakeInfo = []
    for record in dbfTable:
        tempLakeInfo = [int(record['GLWD_ID']),record['LAT_DEG'],record['LONG_DEG']]
        lakeInfo.append(tempLakeInfo)
    lakeInfo = np.array(lakeInfo)
    lakeInfo = np.array(list(set([tuple(t) for t in lakeInfo])))

    resultMatrix = []
    for i in range(0,len(lakeInfo)):
        tempLakeInfo = lakeInfo[i]
        tempID = int(tempLakeInfo[0])
        tempLat = tempLakeInfo[1]
        tempLon = tempLakeInfo[2]
        for latBreak in latBreaks:
            for lonBreak in lonBreaks:
                if (tempLat >= latBreak) and (tempLat < latBreak + 20) and (tempLon >= lonBreak) and (tempLon < lonBreak + 20):
                    llLat = latBreak
                    llLon = lonBreak
        if llLat < 0:
            latMark = 'S'
        elif llLat > 0:
            latMark = 'N'
        else:
            latMark = ''
        if llLon < 0:
            lonMark = 'W'
        elif llLon > 0:
            lonMark = 'E'
        else:
            lonMark = ''
        searchFolder = 'E:\\Lake Volume\\Lake Area\\Occ_Stable\\' + str(int(abs(llLon))) + lonMark + '_' + str(int(abs(llLat))) + latMark
        inRasterFileName = searchFolder + '\\' + str(tempID) + '_StableWater.tif'
        if not (os.path.exists(inRasterFileName)):
            continue
        inRasterDS = gdal.Open(inRasterFileName)
        inRasterArray = inRasterDS.GetRasterBand(1).ReadAsArray()
        ulx, xres, xskew, uly, yskew, yres  = inRasterDS.GetGeoTransform()

        for record in dbfTable:
            recLakeID = int(record['GLWD_ID'])
            recLaserLat = record['Y']
            recLaserLon = record['X']
            if recLakeID == tempID:
                yLocation = math.floor((uly - recLaserLat)/xres)
                xLocation = math.floor((recLaserLon - ulx)/xres)
                if inRasterArray[yLocation,xLocation] == 1:
                    resultMatrix.append([record['X'],record['Y'],record['ElevTP'],record['ElevEGM'],record['SatCorr'],record['EillpCorr'],record['GLWD_ID'],record['LAT_DEG'],record['LONG_DEG']])
        
        showInfo = str(i) + '_' + str(len(lakeInfo))
        print(showInfo)
    
    # Output
    ouputFileName = outputPath + '\\' + fileName[:-4] + '.csv'
    columnName = ['X','Y','ElevTP','ElevEGM','SatCorr','EillpCorr','GLWD_ID','LAT_DEG','LONG_DEG']
    outputDF = pd.DataFrame(columns = columnName,data = resultMatrix,index = None)
    outputDF.to_csv(ouputFileName)
    print(ouputFileName)