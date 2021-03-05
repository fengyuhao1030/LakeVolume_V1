rm(list = ls())

lakeRegions = c('0_10N','0_10S','0_30N','0_30S','0_50N','0_50S',
                '20E_10N','20E_10S','20E_30N','20E_30S','20E_50N','20E_50S','20E_70N',
                '20W_10N','20W_10S','20W_30N','20W_50N',
                '40E_10N','40E_10S','40E_30N','40E_30S','40E_50N','40E_70N',
                '40W_10S','40W_30S','40W_50N','40W_70N',
                '60E_10N','60E_10S','60E_30N','60E_50N','60E_50S','60E_70N',
                '60W_10S','60W_30N','60W_30S','60W_50N','60W_50S','60W_70N',
                '80E_10N','80E_10S','80E_30N','80E_50N','80E_70N',
                '80W_10N','80W_10S','80W_30N','80W_30S','80W_50N','80W_50S','80W_70N','80W_70S',
                '100E_10N','100E_10S','100E_30N','100E_30S','100E_50N','100E_50S','100E_70N',
                '100W_10N','100W_10S','100W_30N','100W_50N','100W_70N',
                '120E_10N','120E_10S','120E_30N','120E_30S','120E_50N','120E_50S','120E_70N',
                '120W_10N','120W_30N','120W_50N','120W_70N',
                '140E_10S','140E_30N','140E_30S','140E_50N','140E_50S','140E_70N',
                '140W_30N','140W_50N','140W_70N',
                '160E_30S','160E_50N','160E_50S',
                '160W_10S','160W_50N','160W_70N',
                '180W_30S','180W_50N','180W_70N')

firstDirFlag <- 1
for(lakeRegion in lakeRegions){
  inputPath = paste0('E:\\Lake Volume\\Lake Area\\Proj_WaterHistory_Month\\',lakeRegion)
  setwd(inputPath)
  fileNames <- list.files(pattern = '.csv')
  
  firstFileFlag <- 1
  for(i in seq(1,length(fileNames))){
    fileName <- fileNames[i]
    selectIndex <- gregexpr('_',fileName)[[1]]
    lakeID <- as.numeric(substring(fileName,1,(selectIndex - 1)))
    tempData <- read.csv(fileName)
    # Find out and remove invalid area value
    # Season = 1
    selectIndex <- which(tempData$Season == 1)
    seasonData_1 <- tempData[selectIndex,]
    summaryData <- as.data.frame(table(seasonData_1$Area))
    summaryData$Var1 <- as.numeric(as.character(summaryData$Var1))
    delIndex <- numeric()
    for(j in seq(1,nrow(summaryData))){
      tempFreq <- summaryData$Freq[j]
      if(tempFreq > 3){
        delIndex <- c(delIndex,which(seasonData_1$Area == summaryData$Var1[j]))
      }
    }
    if(length(delIndex) > 0){
      seasonData_1 <- seasonData_1[-delIndex,]
    }
    # Season = 2
    selectIndex <- which(tempData$Season == 2)
    seasonData_2 <- tempData[selectIndex,]
    summaryData <- as.data.frame(table(seasonData_2$Area))
    summaryData$Var1 <- as.numeric(as.character(summaryData$Var1))
    delIndex <- numeric()
    for(j in seq(1,nrow(summaryData))){
      tempFreq <- summaryData$Freq[j]
      if(tempFreq > 3){
        delIndex <- c(delIndex,which(seasonData_2$Area == summaryData$Var1[j]))
      }
    }
    if(length(delIndex) > 0){
      seasonData_2 <- seasonData_2[-delIndex,]
    }
    # Season = 3
    selectIndex <- which(tempData$Season == 3)
    seasonData_3 <- tempData[selectIndex,]
    summaryData <- as.data.frame(table(seasonData_3$Area))
    summaryData$Var1 <- as.numeric(as.character(summaryData$Var1))
    delIndex <- numeric()
    for(j in seq(1,nrow(summaryData))){
      tempFreq <- summaryData$Freq[j]
      if(tempFreq > 3){
        delIndex <- c(delIndex,which(seasonData_3$Area == summaryData$Var1[j]))
      }
    }
    if(length(delIndex) > 0){
      seasonData_3 <- seasonData_3[-delIndex,]
    }
    # Season = 4
    selectIndex <- which(tempData$Season == 4)
    seasonData_4 <- tempData[selectIndex,]
    summaryData <- as.data.frame(table(seasonData_4$Area))
    summaryData$Var1 <- as.numeric(as.character(summaryData$Var1))
    delIndex <- numeric()
    for(j in seq(1,nrow(summaryData))){
      tempFreq <- summaryData$Freq[j]
      if(tempFreq > 3){
        delIndex <- c(delIndex,which(seasonData_4$Area == summaryData$Var1[j]))
      }
    }
    if(length(delIndex) > 0){
      seasonData_4 <- seasonData_4[-delIndex,]
    }
    # Combine season data
    tempData <- rbind(seasonData_1,seasonData_2,seasonData_3,seasonData_4)
    tempResultMatrix <- as.data.frame(matrix(data = 0,nrow = 1,ncol = 68))
    tempResultMatrix[1,1] <- lakeID
    count <- 2
    for(j in seq(2003,2019)){
      if(j == 2019){
        endSeason <- 3
      }else{
        endSeason <- 4
      }
      for(k in seq(1,endSeason)){
        selectIndex <- which((tempData$Year == j)&(tempData$Season == k))
        if(length(selectIndex) == 0){
          tempResultMatrix[1,count] <- -9999
        }else{
          tempResultMatrix[1,count] <- tempData$Area[selectIndex]
        }
        count <- count + 1
      }
    }
    if(firstFileFlag == 1){
      resultMatrix <- tempResultMatrix
      firstFileFlag <- 0
    }else{
      resultMatrix <- rbind(resultMatrix,tempResultMatrix)
    }
    showInfo <- paste0(lakeRegion,'_',as.character(i))
    print(showInfo)
  }
  if(firstDirFlag == 1){
    totalResultMatrix <- resultMatrix
    firstDirFlag <- 0
  }else{
    totalResultMatrix <- rbind(totalResultMatrix,resultMatrix)
  }
}

delIndex <- numeric()
for(i in seq(1,nrow(totalResultMatrix))){
  tempRow <- totalResultMatrix[i,]
  selectIndex <- which(tempRow != -9999)
  if(length(selectIndex) < 11){
    delIndex <- c(delIndex,i)
  }
  print(i)
}
totalResultMatrix <- totalResultMatrix[-delIndex,]

write.csv(totalResultMatrix,file = 'E:\\Lake Volume\\Lake Area\\Lake_Area_1.csv',row.names = FALSE)