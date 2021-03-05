import os
import glob
import csv
import numpy as np
from osgeo import osr
from osgeo import ogr

print('Collect file information and set environment......')
inDir = 'E:\\Lake Volume\\Lake Level\\ATL13_Txt\\'
outDir = 'E:\\Lake Volume\\Lake Level\\ATL13_Shp\\'
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
    outputFileName = outDir + inFileName[0:4] + '_' + inFileName[5:7] + '_' + inFileName[8:10] + '.shp'
    # Create new layer
    driver = ogr.GetDriverByName('ESRI shapefile')
    ds = driver.CreateDataSource(outputFileName)
    lyr = ds.CreateLayer('Layer', sr, ogr.wkbPoint)
    newFieldTemplate = ogr.FieldDefn('DeltaTime', ogr.OFTReal)
    newFieldTemplate.SetWidth(16)
    newFieldTemplate.SetPrecision(5)
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('X')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('Y')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('ElevWGS84')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('ElevEGM')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('GeoidValue')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('SWHValue')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('CloudCon')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('BeamMark')
    lyr.CreateField(newFieldTemplate)
    newFieldTemplate.SetName('IsNight')
    lyr.CreateField(newFieldTemplate)
    for row in reader:
        if row[0].isalpha():
            continue
        else:
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.AddPoint(float(row[2]), float(row[1]))
            tempFeature = ogr.Feature(lyr.GetLayerDefn())
            tempFeature.SetGeometry(tempGeom)
            tempFeature.SetField('DeltaTime', row[0])
            tempFeature.SetField('X', row[2])
            tempFeature.SetField('Y', row[1])
            tempFeature.SetField('ElevWGS84', row[3])
            tempFeature.SetField('ElevEGM', row[4])
            tempFeature.SetField('GeoidValue',row[5])
            tempFeature.SetField('SWHValue',row[6])
            tempFeature.SetField('CloudCon', row[7])
            tempFeature.SetField('BeamMark', row[8])
            tempFeature.SetField('IsNight', row[9])
            lyr.CreateFeature(tempFeature)
    del ds
    print(str(i+1) + ' files have done')