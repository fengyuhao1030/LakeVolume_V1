rm(list = ls())
library(foreign)
setwd('E:\\Lake Volume\\Lake Level\\GLAH14_SJ_SJ')

fileNames <- list.files(pattern = '.csv')
flag <- 0
for(i in seq(1,length(fileNames))){
  fileName <- fileNames[i]
  tempYear <- as.numeric(substring(fileName,1,4))
  tempMonth <- as.numeric(substring(fileName,6,7))
  tempDay <- as.numeric(substring(fileName,9,10))
  tempData <- read.csv(fileName)
  lakeIDs <- unique(tempData$GLWD_ID)
  for(j in seq(1,length(lakeIDs))){
    lakeID <- lakeIDs[j]
    selectIndex <- which(tempData$GLWD_ID == lakeID)
    elevTP <- as.numeric(tempData$ElevTP[selectIndex])
    geoidCorr <- as.numeric(tempData$ElevEGM[selectIndex])
    satCorr <- as.numeric(tempData$SatCorr[selectIndex])
    eillpCorr <- as.numeric(tempData$EillpCorr[selectIndex])
    tempLat <- as.numeric(tempData$LAT_DEG[selectIndex[1]])
    tempLon <- as.numeric(tempData$LONG_DEG[selectIndex[1]])
    if((length(elevTP) < 3)|(sd(elevTP) > 5)){
      next
    }
    if(length(elevTP) > 10){
      medianElev <- quantile(elevTP,0.5)
      NMAD <- 1.4826*quantile(abs(elevTP - medianElev),0.5)
      upLimit <- medianElev + NMAD
      downLimit <- medianElev - NMAD
      selectIndex <- which((elevTP > downLimit)&(elevTP < upLimit))
      meanElev <- mean(elevTP[selectIndex] + satCorr[selectIndex] - geoidCorr[selectIndex] - eillpCorr[selectIndex])
    }else{
      meanElev <- mean(elevTP + satCorr - geoidCorr - eillpCorr)
    }
    tempResultMatrix <- data.frame(Year = tempYear,Month = tempMonth,Day = tempDay,
                                   GLWD_ID = lakeID,Lat = tempLat,Lon = tempLon,LakeLevel = meanElev)
    if(flag == 0){
      resultMatrix <- tempResultMatrix
      flag <- 1
    }else{
      resultMatrix <- rbind(resultMatrix,tempResultMatrix)
    }
  }
  showInfo <- paste0(as.character(i),'_',as.character(length(fileNames)))
  print(showInfo)
}
write.csv(resultMatrix,file = 'E:\\Lake Volume\\Lake Level\\GLAH14_Ref_Compare\\GLAH14_Level.csv',row.names = FALSE)