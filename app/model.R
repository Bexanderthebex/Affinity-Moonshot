library(car)
train<-(read.csv("~/Desktop/moonshot-affinity/backend/train.csv", header=TRUE))
#/*choiceB<-numeric()
#i=1
#while(i<=nrow(train)){
#if(train[i,1]==1){choiceB[i]<-0; i=i+1} else{choiceB[i]<-1;i=i+1}}
#train<-data.frame(train,choiceB)
#trainB<-data.frame(train[,24],train[,13:23])
#colnames(trainB)<-colnames(train[,1:12])
#data<-rbind(train[,1:12],trainB)
#NOTE: After this the variables are already for A and B observations so the interpretation is for just 1 user

hist( train$A_listed_count)
#normal data
lm<-lm(Choice~A_follower_count+A_following_count+A_mentions_received+ A_retweets_received + A_mentions_sent + A_retweets_sent +A_posts+B_follower_count+B_following_count+B_listed_count+B_mentions_received+B_retweets_received+B_mentions_sent+B_retweets_sent, data=train)
#splitdata; combined choice for A and B
lm.A<-lm(Choice~A_follower_count+A_following_count+A_listed_count+ A_mentions_received + A_mentions_sent + A_retweets_sent+A_posts, data=train)
vif(lm.A) #test for multicollinearity; remove variable with greater than 10 VIF
#received tweets are removed due to high multicollinearity
model<-glm(Choice~A_follower_count+A_following_count+A_mentions_received + A_mentions_sent + A_retweets_sent +A_posts, data=train, family="binomial")
anova<-aov(model)
summary(model)
summary(anova)
print(model$coefficients) #weights
