rm(list = ls())
library(foreign)
setwd('E:\\Lake Volume\\Lake Level\\ATL13_SJ')

fileNames <- list.files(pattern = '.dbf')
flag <- 0
for(i in seq(1,length(fileNames))){
  fileName <- fileNames[i]
  tempYear <- as.numeric(substring(fileName,1,4))
  tempMonth <- as.numeric(substring(fileName,6,7))
  tempDay <- as.numeric(substring(fileName,9,10))
  tempData <- read.dbf(fileName)
  lakeIDs <- unique(tempData$GLWD_ID)
  for(j in seq(1,length(lakeIDs))){
    lakeID <- lakeIDs[j]
    selectIndex <- which(tempData$GLWD_ID == lakeID)
    orthoLevel <- as.numeric(tempData$ElevEGM[selectIndex])
    swHeight <- as.numeric(tempData$SWHValue[selectIndex])
    tempLat <- as.numeric(tempData$LAT_DEG[selectIndex[1]])
    tempLon <- as.numeric(tempData$LONG_DEG[selectIndex[1]])
    if((length(orthoLevel) < 3)|(sd(orthoLevel) > 5)){
      next
    }
    if(length(orthoLevel) > 10){
      medianLevel <- quantile(orthoLevel,0.5)
      NMAD <- 1.4826*quantile(abs(orthoLevel - medianLevel),0.5)
      upLimit <- medianLevel + NMAD
      downLimit <- medianLevel - NMAD
      selectIndex <- which((orthoLevel > downLimit)&(orthoLevel < upLimit))
      meanLevel <- mean(orthoLevel[selectIndex] - swHeight[selectIndex])
    }else{
      meanLevel <- mean(orthoLevel - swHeight)
    }
    tempResultMatrix <- data.frame(Year = tempYear,Month = tempMonth,Day = tempDay,
                                   GLWD_ID = lakeID,Lat = tempLat,Lon = tempLon,LakeLevel = meanLevel)
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
write.csv(resultMatrix,file = 'E:\\Lake Volume\\Lake Level\\ATL13_Ref_Compare\\ATL13_Level.csv',row.names = FALSE)