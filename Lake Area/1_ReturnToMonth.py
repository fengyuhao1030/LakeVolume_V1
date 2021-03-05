import os
import rasterio

lakeRegions = ['LB_0_10N','LB_0_10S','LB_0_30N','LB_0_30S','LB_0_50N','LB_0_50S',
'LB_20E_10N','LB_20E_10S','LB_20E_30N','LB_20E_30S','LB_20E_50N','LB_20E_50S','LB_20E_70N',
'LB_20W_10N','LB_20W_10S','LB_20W_30N','LB_20W_50N','LB_20W_70N',
'LB_40E_10N','LB_40E_10S','LB_40E_30N','LB_40E_30S','LB_40E_50N','LB_40E_70N',
'LB_40W_10S','LB_40W_30S','LB_40W_50N','LB_40W_70N',
'LB_60E_10N','LB_60E_10S','LB_60E_30N','LB_60E_50N','LB_60E_50S','LB_60E_70N',
'LB_60W_10S','LB_60W_30N','LB_60W_30S','LB_60W_50N','LB_60W_50S','LB_60W_70N',
'LB_80E_10N','LB_80E_10S','LB_80E_30N','LB_80E_50N','LB_80E_70N',
'LB_80W_10N','LB_80W_10S','LB_80W_30N','LB_80W_30S','LB_80W_50N','LB_80W_50S','LB_80W_70N','LB_80W_70S',
'LB_100E_10N','LB_100E_10S','LB_100E_30N','LB_100E_30S','LB_100E_50N','LB_100E_50S','LB_100E_70N',
'LB_100W_10N','LB_100W_10S','LB_100W_30N','LB_100W_50N','LB_100W_70N',
'LB_120E_10N','LB_120E_10S','LB_120E_30N','LB_120E_30S','LB_120E_50N','LB_120E_50S','LB_120E_70N',
'LB_120W_10N','LB_120W_30N','LB_120W_50N','LB_120W_70N',
'LB_140E_10S','LB_140E_30N','LB_140E_30S','LB_140E_50N','LB_140E_50S','LB_140E_70N',
'LB_140W_30N','LB_140W_50N','LB_140W_70N',
'LB_160E_30S','LB_160E_50N','LB_160E_50S',
'LB_160W_10S','LB_160W_50N','LB_160W_70N',
'LB_180W_30S','LB_180W_50N','LB_180W_70N']

inputPath = 'E:\\Lake Volume\\Lake Area\\WaterHistory_Year\\'
outputPath = 'E:\\Lake Volume\\Lake Area\\WaterHistory_Month\\'
for i in range(90,91):
    tempLakeRegion = lakeRegions[i]
    tempFolderName = outputPath + tempLakeRegion[3:]
    os.mkdir(tempFolderName)
    for tempYear in range(2003,2020):
        yearRasterFileName = inputPath + tempLakeRegion + '_' + str(tempYear) + '.tif'
        with rasterio.open(yearRasterFileName) as yearRasterDS:
            yearRasterData = yearRasterDS.read(1)
            outputRasterMeta = yearRasterDS.meta.copy()
            outputRasterMeta.update({'dtype':'uint8','compress': 'lzw'})
            for tempMonth in range(1,13):
                monthRasterData = (yearRasterData % 3).astype('uint8')
                yearRasterData = yearRasterData // 3
                outputFileName = tempFolderName + '\\' + tempLakeRegion + '_' + str(tempYear) + '_' + str(tempMonth) + '.tif'
                with rasterio.open(outputFileName,'w',**outputRasterMeta) as dest:
                    dest.write(monthRasterData,indexes = 1)
                    