import os
import glob
import h5py
import numpy as np

print('Collect file information and set environment......')
inDir = 'E:\\Lake Volume\\Lake Level\\ATL13'
outDir = 'E:\\Lake Volume\\Lake Level\\ATL13_Txt'
os.chdir(inDir)
inFileList = glob.glob('*.h5')
dateList = []
for inFileName in inFileList:
    dateList.append(inFileName[0:10])
dateList = sorted(list(set(dateList)))

print(str(len(dateList)) + ' days in the queue......')
groupMark = ['gt1l','gt1r','gt2l','gt2r','gt3l','gt3r']
for tempDate in dateList:
    newInFileList = []
    for inFileName in inFileList:
        if inFileName[0:10] == tempDate:
            newInFileList.append(inFileName)
    outputFileName = outDir + '\\' + tempDate + '.txt'
    count = 1
    for inFileName in newInFileList:
        fileHandle = h5py.File(inFileName)
        orientInfo = fileHandle['orbit_info']['sc_orient'][:]
        count_1 = 1
        for tempMark in groupMark:
            if tempMark not in list(fileHandle.keys()):
                continue
            else:
                deltaTime = fileHandle[tempMark]['delta_time'][:]
                Latitude = fileHandle[tempMark]['sseg_mean_lat'][:]
                Longitude = fileHandle[tempMark]['sseg_mean_lon'][:]
                ElevationWGS84 = fileHandle[tempMark]['ht_water_surf'][:]
                ElevationEGM = fileHandle[tempMark]['ht_ortho'][:]
                GeoidValue = fileHandle[tempMark]['segment_geoid'][:]
                SWHValue = fileHandle[tempMark]['significant_wave_ht'][:]
                # cloudCon: 0 for clear; 1 for cloudy
                cloudCon = fileHandle[tempMark]['cloud_flag_asr_atl09'][:]
                # beamMark: 0 for weak beam; 1 for strong beam
                if (tempMark in ['gt1l', 'gt2l', 'gt3l']) and (orientInfo[0] == 0):
                    beamMark = np.zeros(deltaTime.shape[0], dtype=int) + 1
                elif (tempMark in ['gt1r', 'gt2r', 'gt3r']) and (orientInfo[0] == 1):
                    beamMark = np.zeros(deltaTime.shape[0], dtype=int) + 1
                else:
                    beamMark = np.zeros(deltaTime.shape[0], dtype=int)
                # weak beams represent the best option for daytime acquisitions
                isNight = (deltaTime % 86400)/3600 + Longitude/15
                for i in range(0,len(isNight)):
                    if (isNight[i] < 6) and (isNight[i] > -6):
                        isNight[i] = 1
                    else:
                        isNight[i] = 0
                tempResultMatrix = np.column_stack((deltaTime, Latitude, Longitude, ElevationWGS84, ElevationEGM, GeoidValue, SWHValue, cloudCon, beamMark, isNight))
                if count_1 == 1:
                    fileResultMatrix = tempResultMatrix
                else:
                    fileResultMatrix = np.row_stack((fileResultMatrix, tempResultMatrix))
                count_1 = count_1 + 1
        fileHandle.close()
        if count == 1:
            dateResultMatrix = fileResultMatrix
        else:
            dateResultMatrix = np.row_stack((dateResultMatrix,fileResultMatrix))
        print('Temp date: {0}, Total file number: {1}, Temp number: {2}'.format(tempDate, str(len(newInFileList)), str(count)))
        count = count + 1
    deleteIndex = []
    for i in range(0,dateResultMatrix.shape[0]):
        if dateResultMatrix[i, 1] > -100000 and dateResultMatrix[i, 1] < 100000:
            latitudeFlag = True
        else:
            latitudeFlag = False
        if dateResultMatrix[i, 2] > -100000 and dateResultMatrix[i, 2] < 100000:
            longitudeFlag = True
        else:
            longitudeFlag = False
        if dateResultMatrix[i, 6] < 100:
            SWHFlag = True
        else:
            SWHFlag = False
        if dateResultMatrix[i, 7] == 0:
            cloudFlag = True
        else:
            cloudFlag = False
        if dateResultMatrix[i, 8] == 1 and dateResultMatrix[i, 9] == 1:
            beamFlag = True
        elif dateResultMatrix[i, 8] == 0 and dateResultMatrix[i, 9] == 0:
            beamFlag = True
        else:
            beamFlag = False
        Flag = latitudeFlag and longitudeFlag and SWHFlag and cloudFlag
        if not Flag:
            deleteIndex.append(i)
    dateResultMatrix = np.delete(dateResultMatrix, np.array(deleteIndex), axis=0)
    # Output
    txtLabels = 'DeltaTime, Latitude, Longitude, ElevationWGS84, ElevationEGM, GeoidValue, SWHValue, CloudCon, BeamMark, IsNight\n'
    txtHandle = open(outputFileName, 'w')
    txtHandle.writelines(txtLabels)
    np.savetxt(txtHandle, dateResultMatrix, fmt='%f', delimiter=',', newline='\n')
    txtHandle.close()
    print(outputFileName)