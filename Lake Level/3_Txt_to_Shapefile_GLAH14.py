import os
import glob
import csv
import numpy as np
from osgeo import osr
from osgeo import ogr

print('Collect file information and set environment......')
inDir = 'E:\\Lake Volume\\Lake Level\\GLAH14_Txt\\'
outDir = 'E:\\Lake Volume\\Lake Level\\GLAH14_Shp\\'
os.chdir(inDir)
inFileList = glob.glob('*.txt')
sr = osr.SpatialReference()
sr.ImportFromProj4('''+init=epsg:4326''')

print(str(len(inFileList)) + ' files in the queue......')
for i in range(0, len(inFileList)):
    # inFileName and outputFileName
    inFileName = inFileList[i]
    # Line number
    inFileHandle = open(inDir + inFileName, 'r')
    reader = csv.reader(inFileHandle, delimiter=',')
    lineNum = np.array(list(reader)).shape[0]
    if lineNum == 1:
        continue
    del inFileHandle
    # New file handle, read
    inFileHandle = open(inDir + inFileName, 'r')
    reader = csv.reader(inFileHandle, delimiter=',')
    outputFileName = outDir + inFileName[0:4] + '_' + inFileName[5:7] + '_' + inFileName[8:-4] + '.shp'
    # Create new layer
    driver = ogr.GetDriverByName('ESRI shapefile')
    ds = driver.CreateDataSource(outputFileName)
    lyr = ds.CreateLayer('Layer', sr, ogr.wkbPoint)
    newFieldTemplate = ogr.FieldDefn('LaserIndex', ogr.OFTReal)
    newFieldTemplate.SetWidth(16)
    newFieldTemplate.SetPrecision(3)
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('X')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('Y')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('ElevTP')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('ElevEGM')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('SatCorr')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('EillpCorr')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('NumPeak')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('AtmosCon')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('SatCon')
    lyr.CreateField(newFieldTemplate)
    for row in reader:
        if row[0].isalpha():
            continue
        else:
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.AddPoint(float(row[2]), float(row[1]))
            tempFeature = ogr.Feature(lyr.GetLayerDefn())
            tempFeature.SetGeometry(tempGeom)
            tempFeature.SetField('LaserIndex', row[0])
            tempFeature.SetField('X', row[2])
            tempFeature.SetField('Y', row[1])
            tempFeature.SetField('ElevTP', row[3])
            tempFeature.SetField('ElevEGM', row[4])
            tempFeature.SetField('SatCorr', row[5])
            tempFeature.SetField('EillpCorr', row[6])
            tempFeature.SetField('NumPeak', row[7])
            tempFeature.SetField('AtmosCon', row[8])
            tempFeature.SetField('SatCon', row[9])
            lyr.CreateFeature(tempFeature)
    del ds
    print(str(i+1) + ' files have done')