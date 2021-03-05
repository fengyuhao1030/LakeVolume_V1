import os
import glob
import pandas as pd
from osgeo import gdal,gdal_array
from osgeo import osr
from collections import Counter

def Reprojection (dataset, pixel_spacing, s_proj, t_proj):
    s_srs = osr.SpatialReference()
    s_srs.ImportFromProj4(s_proj)
    t_srs = osr.SpatialReference()
    t_srs.ImportFromProj4(t_proj)
    tx = osr.CoordinateTransformation(s_srs,t_srs)
    g = gdal.Open(dataset)
    geo_t = g.GetGeoTransform()
    x_size = g.RasterXSize
    y_size = g.RasterYSize
    (ulx, uly, ulz) = tx.TransformPoint(geo_t[0], geo_t[3])
    (lrx, lry, lrz) = tx.TransformPoint(geo_t[0] + geo_t[1]*x_size, geo_t[3] + geo_t[5]*y_size)
    mem_drv = gdal.GetDriverByName('MEM')
    dest = mem_drv.Create('', int((lrx - ulx)/pixel_spacing), int((uly - lry)/pixel_spacing), 1, gdal.GDT_Int16)
    new_geo = (ulx, pixel_spacing, geo_t[2], uly, geo_t[4], -pixel_spacing)
    dest.SetGeoTransform(new_geo)
    dest.SetProjection (t_srs.ExportToWkt())
    gdal.ReprojectImage(g, dest, s_srs.ExportToWkt(), t_srs.ExportToWkt(), gdal.GRA_NearestNeighbour)
    return dest

lakeRegions = ['0_10N','0_10S','0_30N','0_30S','0_50N','0_50S',
'20E_10N','20E_10S','20E_30N','20E_30S','20E_50N','20E_50S','20E_70N',
'20W_10N','20W_10S','20W_30N','20W_50N',
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
    regionMark = lakeRegions[i]
    inputPath = 'E:\\Lake Volume\\Lake Area\\Fix_WaterHistory_Month\\' + regionMark
    outputPath = 'E:\\Lake Volume\\Lake Area\\Proj_WaterHistory_Month\\' + regionMark
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    # Lon
    regionMark = regionMark.split('_')
    lonString = regionMark[0]
    selectIndex_1 = lonString.find('W')
    selectIndex_2 = lonString.find('E')
    if not (selectIndex_1 == -1):
        llLon = -int(lonString[:-1])
    if not (selectIndex_2 == -1):
        llLon = int(lonString[:-1])
    if (selectIndex_1 == -1) and (selectIndex_2 == -1):
        llLon = int(lonString)
    # Lat
    latString = regionMark[1]
    selectIndex_1 = latString.find('S')
    selectIndex_2 = latString.find('N')
    if not (selectIndex_1 == -1):
        llLat = -int(latString[:-1])
    if not (selectIndex_2 == -1):
        llLat = int(latString[:-1])
    # SRS
    sourceSRS = '+proj=latlong +ellps=WGS84'
    targetSRS = '+proj=cea +lon_0=' + str(llLon + 10) + ' +lat_ts=' + str(llLat + 10) + ' +ellps=WGS84'
    os.chdir(inputPath)
    inFileList = glob.glob('*.tif')
    lakeIDs = []
    for fileName in inFileList:
        selectIndex = fileName.find('_')
        lakeIDs.append(int(fileName[0:selectIndex]))
    lakeIDs = list(set(lakeIDs))
    lakeIDs = sorted(lakeIDs)

    for j in range(0,len(lakeIDs)):
        lakeID = lakeIDs[j]
        csvMatrix = []
        for tempYear in range(2003,2020):
            startSeason = 1
            if tempYear == 2019:
                endSeason = 3
            else:
                endSeason = 4
            for tempSeason in range(startSeason,(endSeason + 1)):
                if tempSeason == 1:
                    inRaster_1 = str(lakeID) + '_' + str(tempYear) + '_3.tif'
                    inRaster_2 = str(lakeID) + '_' + str(tempYear) + '_4.tif'
                    inRaster_3 = str(lakeID) + '_' + str(tempYear) + '_5.tif'
                if tempSeason == 2:
                    inRaster_1 = str(lakeID) + '_' + str(tempYear) + '_6.tif'
                    inRaster_2 = str(lakeID) + '_' + str(tempYear) + '_7.tif'
                    inRaster_3 = str(lakeID) + '_' + str(tempYear) + '_8.tif'
                if tempSeason == 3:
                    inRaster_1 = str(lakeID) + '_' + str(tempYear) + '_9.tif'
                    inRaster_2 = str(lakeID) + '_' + str(tempYear) + '_10.tif'
                    inRaster_3 = str(lakeID) + '_' + str(tempYear) + '_11.tif'
                if tempSeason == 4:
                    inRaster_1 = str(lakeID) + '_' + str(tempYear) + '_12.tif'
                    inRaster_2 = str(lakeID) + '_' + str(tempYear+1) + '_1.tif'
                    inRaster_3 = str(lakeID) + '_' + str(tempYear+1) + '_2.tif'
                try:
                    rasterDS = gdal.Open(inRaster_1)
                    inRasterArray_1 = gdal_array.LoadFile(inRaster_1)
                    inRasterArray_2 = gdal_array.LoadFile(inRaster_2)
                    inRasterArray_3 = gdal_array.LoadFile(inRaster_3)
                except:
                    print('Error')
                else:
                    # Output
                    outputRasterArray = inRasterArray_1
                    outputRasterArray[outputRasterArray == -1] = -1
                    outputRasterArray[outputRasterArray == 255] = -1
                    outputRasterArray[inRasterArray_2 == 2] = 2
                    outputRasterArray[inRasterArray_3 == 2] = 2
                    outputFileName_1 = outputPath + '\\' + str(lakeID) + '_' + str(tempYear) + '_S' + str(tempSeason) + '.tif'
                    gdal_array.SaveArray(outputRasterArray.astype('int16'), outputFileName_1, 'GTiff', rasterDS)
                    # Projection
                    outputFileName_2 = outputPath + '\\' + str(lakeID) + '_' + str(tempYear) + '_S' + str(tempSeason) + '_Proj.tif'
                    outRaster = Reprojection(outputFileName_1, 90, sourceSRS, targetSRS)
                    driver = gdal.GetDriverByName ('GTiff')
                    driver.CreateCopy(outputFileName_2,outRaster,0)
                    del(driver)
                    rasterSummary = Counter(gdal_array.LoadFile(outputFileName_2).flatten())
                    csvMatrix.append([tempYear,tempSeason,rasterSummary[2]*90*90])
        outputCSVFileName = outputPath + '\\' + str(lakeID) + '_Area.csv'
        columnName = ['Year','Season','Area']
        outputDF = pd.DataFrame(columns = columnName,data = csvMatrix,index = None)
        outputDF.to_csv(outputCSVFileName)
        showInfo = str(j+1) + '_' + str(len(lakeIDs))
        print(showInfo)

