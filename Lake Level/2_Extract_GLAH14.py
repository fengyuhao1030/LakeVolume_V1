import os
import glob
import h5py
import numpy as np

print('Collect file information and set environment......')
inDir = 'E:\\Lake Volume\\Lake Level\\GLAH14'
outDir = 'E:\\Lake Volume\\Lake Level\\GLAH14_Txt'
os.chdir(inDir)
inFileList = glob.glob('*.H5')

print(str(len(inFileList)) + ' files in the queue......')
for i in range(0,len(inFileList)):
    inFileName = inFileList[i]
    fileHandle = h5py.File(inFileName)
    outputFileName = outDir + '\\' + inFileName[:-3] + '.txt'
    obsIndex = fileHandle['Data_40HZ']['Time']['i_rec_ndx'][:]
    shotIndex = fileHandle['Data_40HZ']['Time']['i_shot_count'][:]
    laserIndex = obsIndex % 1000000 * 100 + shotIndex
    Latitude = fileHandle['Data_40HZ']['Geolocation']['d_lat'][:]
    Longitude = fileHandle['Data_40HZ']['Geolocation']['d_lon'][:]
    for j in range(0, len(laserIndex)):
        if Longitude[j] > 180:
            Longitude[j] = Longitude[j] - 360
        else:
            Longitude[j] = Longitude[j]
    ElevationTP = fileHandle['Data_40HZ']['Elevation_Surfaces']['d_elev'][:]
    satElevationCorr = fileHandle['Data_40HZ']['Elevation_Corrections']['d_satElevCorr'][:]
    ellipElevationCorr = fileHandle['Data_40HZ']['Geophysical']['d_deltaEllip'][:]
    ElevationEGM = fileHandle['Data_40HZ']['Geophysical']['d_gdHt'][:]
    for j in range(0,len(satElevationCorr)):
        if satElevationCorr[j] < -10:
            satElevationCorr[j] = 0
        if satElevationCorr[j] > 10:
            satElevationCorr[j] = 0
    for j in range(0,len(ellipElevationCorr)):
        if ellipElevationCorr[j] < -10:
            ellipElevationCorr[j] = 0
        if ellipElevationCorr[j] > 10:
            ellipElevationCorr[j] = 0
    peakNum = fileHandle['Data_40HZ']['Waveform']['i_numPk'][:]
    atomosCon = fileHandle['Data_40HZ']['Atmosphere']['FRir_qa_flg'][:]
    saturationCon = fileHandle['Data_40HZ']['Quality']['sat_corr_flg'][:]
    resultMatrix = np.column_stack((laserIndex, Latitude, Longitude, ElevationTP,ElevationEGM,
                                    satElevationCorr,ellipElevationCorr,peakNum, atomosCon, saturationCon))
    deleteIndex = []
    for j in range(0, len(laserIndex)):
        if Latitude[j] > -100000 and Latitude[j] < 100000:
            LatitudeFlag = True
        else:
            LatitudeFlag = False
        if Longitude[j] > -100000 and Longitude[j] < 100000:
            LongitudeFlag = True
        else:
            LongitudeFlag = False
        if peakNum[j] == 1:
            peakNumFlag = True
        else:
            peakNumFlag = False
        if atomosCon[j] == 15:
            atomosFlag = True
        else:
            atomosFlag = False
        if saturationCon[j] == 0:
            saturationFlag = True
        else:
            saturationFlag = False
        Flag = LatitudeFlag and LongitudeFlag and peakNumFlag and atomosFlag and saturationFlag
        if not Flag:
            deleteIndex.append(j)
    resultMatrix = np.delete(resultMatrix, np.array(deleteIndex), axis=0)
    txtLabels = 'LaserIndex,Latitude,Longitude,ElevationTP,ElevationEGM,SatCorr,EillpCorr,PeakNum,AtmosCon,SaturationCon\n'
    txtHandle = open(outputFileName, 'w')
    txtHandle.writelines(txtLabels)
    np.savetxt(txtHandle, resultMatrix, fmt='%f', delimiter=',', newline='\n')
    fileHandle.close()
    txtHandle.close()
    print(str(i + 1) + ' files have done')