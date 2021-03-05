rm(list = ls())
setwd('E:\\Lake Volume\\Lake Level\\RefLevel')

ATL13Level <- read.csv('E:\\Lake Volume\\Lake Level\\ATL13_Ref_Compare\\ATL13_Level.csv')
fileNames <- list.files(pattern = '.csv')
flag <- 0
lakeIDs <- numeric()
for(i in seq(1,length(fileNames))){
  # Reference data
  fileName <- fileNames[i]
  selectIndex <- gregexpr('_',fileName)[[1]][1]
  tempID <- as.numeric(substring(fileName,1,(selectIndex - 1)))
  lakeIDs[i] <- tempID
  refLakeLevelData <- read.csv(fileName)
  # Row data
  selectIndex <- which(ATL13Level$GLWD_ID == tempID)
  rowLakeLevelData <- ATL13Level[selectIndex,]
  for(j in seq(1,nrow(rowLakeLevelData))){
    tempYear <- rowLakeLevelData$Year[j]
    tempMonth <- rowLakeLevelData$Month[j]
    tempDay <- rowLakeLevelData$Day[j]
    selectIndex <- which((refLakeLevelData$Year == tempYear)&(refLakeLevelData$Month == tempMonth)&(refLakeLevelData$Day == tempDay))
    if(length(selectIndex) == 0){
      next
    }
    tempResultMatrix <- data.frame(GLWD_ID = tempID,Lat = rowLakeLevelData$Lat[1],Lon = rowLakeLevelData$Lon[1],
                                   Year = tempYear,Month = tempMonth,Day = tempDay,Level = refLakeLevelData$Level[selectIndex])
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
write.csv(resultMatrix,file = 'E:\\Lake Volume\\Lake Level\\ATL13_Ref_Compare\\Ref_Level.csv',row.names = FALSE)