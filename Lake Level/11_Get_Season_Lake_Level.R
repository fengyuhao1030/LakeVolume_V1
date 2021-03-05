rm(list = ls())
ICESat1Data <- read.csv('E:\\Lake Volume\\Lake Level\\GLAH14_Ref_Compare\\GLAH14_Level.csv')
ICESat2Data <- read.csv('E:\\Lake Volume\\Lake Level\\ATL13_Ref_Compare\\ATL13_Level.csv')
lakeIDs <- sort(unique(c(ICESat1Data$GLWD_ID,ICESat2Data$GLWD_ID)))

for(i in seq(1,length(lakeIDs))){
  lakeID <- lakeIDs[i]
  tempResultMatrix <- as.data.frame(matrix(data = 0,nrow = 1,ncol = 68))
  tempResultMatrix[1,1] <- lakeID
  count <- 2
  for(j in seq(2003,2019)){
    tempYear <- j
    if(tempYear == 2019){
      endSeason <- 3
    }else{
      endSeason <- 4
    }
    for(k in seq(1,endSeason)){
      tempSeason <- k
      if(tempYear < 2010){
        tempData <- ICESat1Data
      }else{
        tempData <- ICESat2Data
      }
      if(tempSeason == 1){
        selectIndex <- which((tempData$GLWD_ID == lakeID)&(tempData$Year == tempYear)&(tempData$Month %in% c(3,4,5)))
      }
      if(tempSeason == 2){
        selectIndex <- which((tempData$GLWD_ID == lakeID)&(tempData$Year == tempYear)&(tempData$Month %in% c(6,7,8)))
      }
      if(tempSeason == 3){
        selectIndex <- which((tempData$GLWD_ID == lakeID)&(tempData$Year == tempYear)&(tempData$Month %in% c(9,10,11)))
      }
      if(tempSeason == 4){
        selectIndex_1 <- which((tempData$GLWD_ID == lakeID)&(tempData$Year == tempYear)&(tempData$Month == 12))
        selectIndex_2 <- which((tempData$GLWD_ID == lakeID)&(tempData$Year == tempYear + 1)&(tempData$Month %in% c(1,2)))
        selectIndex <- c(selectIndex_1,selectIndex_2)
      }
      if(length(selectIndex) == 0){
        tempResultMatrix[1,count] <- -9999
      }else{
        tempResultMatrix[1,count] <- mean(tempData$LakeLevel[selectIndex])
      }
      count <- count + 1
    }
  }
  if(i == 1){
    resultMatrix <- tempResultMatrix
  }else{
    resultMatrix <- rbind(resultMatrix,tempResultMatrix)
  }
  print(i)
}
write.csv(resultMatrix,file = 'E:\\Lake Volume\\Lake Level\\Lake_Level.csv',row.names = FALSE)