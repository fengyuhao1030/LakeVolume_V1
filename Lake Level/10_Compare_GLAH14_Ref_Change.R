rm(list = ls())
setwd('E:\\Lake Volume\\Lake Level\\GLAH14_Ref_Compare')

compareMatrix <- read.csv('GLAH_Ref_Compare.csv')
lakeIDs <- unique(compareMatrix$GLWD_ID)
flag <- 0
for(i in seq(1,length(lakeIDs))){
  tempID <- lakeIDs[i]
  selectIndex <- which(compareMatrix$GLWD_ID == tempID)
  tempMatrix <- compareMatrix[selectIndex,]
  if(nrow(tempMatrix) < 2){
    next
  }else{
    newTempMatrix <- tempMatrix
    for(j in seq(2,nrow(tempMatrix))){
      newTempMatrix$RefLevel[j] <- tempMatrix$RefLevel[j] - tempMatrix$RefLevel[j-1]
      newTempMatrix$RowLevel[j] <- tempMatrix$RowLevel[j] - tempMatrix$RowLevel[j-1]
    }
    newTempMatrix <- newTempMatrix[-1,]
    if(flag == 0){
      resultMatrix <- newTempMatrix
      flag <- 1
    }else{
      resultMatrix <- rbind(resultMatrix,newTempMatrix)
    }
  }
}
write.csv(resultMatrix,file = 'GLAH_Ref_Compare_Change.csv',row.names = FALSE)