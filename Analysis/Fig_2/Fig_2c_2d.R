rm(list = ls())
library(ggplot2)
setwd('E:\\Lake Volume\\0_Article_History\\MS_v4\\Figs\\Fig_2\\Fig_2c_2d')

##==== Function ====##
theme_custom <- function(){
  myTheme <- theme(panel.background = element_rect(fill = 'white',color = 'black',size = 0.7),
                   panel.grid = element_blank(),
                   legend.position = 'none',
                   plot.margin = margin(5,5,5,5),
                   plot.background = element_blank(),
                   axis.ticks = element_line(size = 0.2),
                   axis.ticks.length = unit(-0.15,'lines'),
                   axis.title.y = element_text(size = 10.5,margin = margin(0,5,0,0),face = 'bold',family = 'Times'),
                   axis.title.x = element_text(size = 10.5,margin = margin(4,0,0,0),face = 'bold',family = 'Times'),
                   axis.text.y = element_text(size = 9,margin = margin(0,6,0,0),family = 'Times',color = '#000000'),
                   axis.text.x = element_text(size = 9,margin = margin(7,0,0,0),family = 'Times',color = '#000000'))
  return(myTheme)
}
##==== Function ====##

dataMatrix <- read.csv('DVolume_Basin_Popu_075.csv')
dataMatrix$VolumeChange <- dataMatrix$Volume_2020 - dataMatrix$Volume_2000
dataMatrix$VolumePercapitaChange <- dataMatrix$Volume_2020/dataMatrix$Popu_2020 - dataMatrix$Volume_2000/dataMatrix$Popu_2000
write.csv(dataMatrix,file = 'DVolume_Basin_Popu_075_Draw.csv',row.names = FALSE)

# Lake volume change
breakSeq <- c(-5e10,-1e10,-5e9,-1e9,-5e8,-1e8,-5e7,-1e7,-5e6,-1e6,0,1e6,5e6,1e7,5e7,1e8,5e8,1e9,5e9,1e10,5e10)
for(i in seq(1,length(breakSeq))){
  if(i == 1){
    basinNumber <- length(which(dataMatrix$VolumeChange <= breakSeq[i]))
    tempResultMatrix <- data.frame(XLocation = i,Number = basinNumber)
    resultMatrix_1 <- tempResultMatrix
  }else{
    basinNumber <- length(which((dataMatrix$VolumeChange <= breakSeq[i])&(dataMatrix$VolumeChange >= breakSeq[i-1])))
    tempResultMatrix <- data.frame(XLocation = i,Number = basinNumber)
    resultMatrix_1 <- rbind(resultMatrix_1,tempResultMatrix)
  }
}
basinNumber <- length(which(dataMatrix$VolumeChange >= breakSeq[i]))
tempResultMatrix <- data.frame(XLocation = i+1,Number = basinNumber)
resultMatrix_1 <- rbind(resultMatrix_1,tempResultMatrix)
resultMatrix_1$XLocation <- resultMatrix_1$XLocation - 0.5
resultMatrix_1$Class[seq(1,11)] <- 'Neg'
resultMatrix_1$Class[seq(12,22)] <- 'Pos'

# Lake volume per capita change
breakSeq <- c(-5000,-1000,-500,-100,-50,-10,-5,-1,0,1,5,10,50,100,500,1000,5000)
for(i in seq(1,length(breakSeq))){
  if(i == 1){
    basinNumber <- length(which(dataMatrix$VolumePercapitaChange <= breakSeq[i]))
    tempResultMatrix <- data.frame(XLocation = i,Number = basinNumber)
    resultMatrix_2 <- tempResultMatrix
  }else{
    basinNumber <- length(which((dataMatrix$VolumePercapitaChange <= breakSeq[i])&(dataMatrix$VolumePercapitaChange >= breakSeq[i-1])))
    tempResultMatrix <- data.frame(XLocation = i,Number = basinNumber)
    resultMatrix_2 <- rbind(resultMatrix_2,tempResultMatrix)
  }
}
basinNumber <- length(which(dataMatrix$VolumePercapitaChange >= breakSeq[i]))
tempResultMatrix <- data.frame(XLocation = i+1,Number = basinNumber)
resultMatrix_2 <- rbind(resultMatrix_2,tempResultMatrix)
resultMatrix_2$XLocation <- resultMatrix_2$XLocation - 0.5
resultMatrix_2$Class[seq(1,9)] <- 'Neg'
resultMatrix_2$Class[seq(10,18)] <- 'Pos'

# Draw
Fig_2c <- ggplot()+
  geom_col(data = resultMatrix_1,mapping = aes(x = XLocation,y = Number,fill = Class),width = 0.8,color = '#000000',size = 0.2)+
  scale_x_continuous(limits = c(0,22),breaks = c(2,4,6,8,10,12,14,16,18,20),
                     labels = c('-10','-9','-8','-7','-6','6','7','8','9','10'),expand = expansion(mult = 0.02))+
  scale_y_continuous(limits = c(0,50),breaks = seq(0,50,10),labels = c('0','10','20','30','40','50'),expand = expansion(mult = 0.03))+
  scale_fill_manual(values = c('#d4232d','#2f7cb2'))+
  xlab('Change in lake volume')+
  ylab('Number of basins')+
  theme_custom()
pdf('Fig_2c.pdf',width = 3.54,height = 2)
print(Fig_2c)
dev.off()

Fig_2d <- ggplot()+
  geom_col(data = resultMatrix_2,mapping = aes(x = XLocation,y = Number,fill = Class),width = 0.8,color = '#000000',size = 0.2)+
  scale_x_continuous(limits = c(0,18),breaks = c(2,4,6,8,10,12,14,16),
                     labels = c('-1000','-100','-10','-1','1','10','100','1000'),expand = expansion(mult = 0.02))+
  scale_y_continuous(limits = c(0,50),breaks = seq(0,50,10),labels = c('0','10','20','30','40','50'),expand = expansion(mult = 0.03))+
  scale_fill_manual(values = c('#d4232d','#2f7cb2'))+
  xlab('Change in lake volume per capita')+
  ylab('Number of basins')+
  theme_custom()
pdf('Fig_2d.pdf',width = 3.54,height = 2)
print(Fig_2d)
dev.off()