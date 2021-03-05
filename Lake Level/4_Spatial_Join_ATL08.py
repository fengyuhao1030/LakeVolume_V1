import os
import glob
import geopandas as gpd

print('Collect file information and set environment......')
os.chdir('E:\\Lake Volume\\Lake Level\\GLAH14_Shp')
inFileList = glob.glob('*.shp')
outputPath = 'E:\\Lake Volume\\Lake Level\\GLAH14_SJ'

print('Process......')
lakeShape = gpd.read_file('E:\\Lake Volume\\Lake Level\\Lakes\\GLWD_Lakes_Reservoirs.shp')
for i in range(0, len(inFileList)):
    inFileName = inFileList[i]
    outputFileName = outputPath + '\\' + inFileName[0:-4] + '_SJ.shp'
    GLASShape = gpd.read_file(inFileName)
    try:
        tempResult = gpd.sjoin(GLASShape, lakeShape, how='inner', op='within')
        tempResult.to_file(outputFileName)
    except:
        continue
    print(str(i + 1) + ' files have done')