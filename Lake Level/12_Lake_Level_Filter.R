rm(list = ls())
setwd('E:\\Lake Volume\\Lake Level')

lakeLevel <- read.csv('Lake_Level.csv')
count_1 <- 1
count_2 <- 1
validateSum <- 0
delIndex <- numeric()
for(i in seq(1,nrow(lakeLevel))){
  tempSeries <- lakeLevel[i,]
  validateIndex <- which((tempSeries != lakeLevel[i,1])&(tempSeries != -9999))
  validateData <- tempSeries[validateIndex]
  validateSum <- validateSum + length(validateData)
  if(length(validateIndex) == 0){
    delIndex[count_1] <- i
    count_1 <- count_1 + 1
    next()
  }
  for(j in seq(1,length(validateIndex))){
    Q1 <- as.numeric(quantile(validateData,0.25))
    Q3 <- as.numeric(quantile(validateData,0.75))
    upLimit <- Q3 + 3*(Q3 - Q1)
    lowLimit <- Q1 - 3*(Q3 - Q1)
    if((validateData[j] < lowLimit)|(validateData[j] > upLimit)){
      lakeLevel[i,validateIndex[j]] <- -9999
      print(count_2)
      count_2 <- count_2 + 1
    }
  }
}
lakeLevel <- lakeLevel[-delIndex,]
write.csv(lakeLevel,file = 'LakeLevel_Filter.csv',row.names = FALSE)