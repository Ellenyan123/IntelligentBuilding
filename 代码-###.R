####################################################################################################


new_iris<-iris


###正影响标准化
nmaliz <- function(x){
  standard1<-(x-min(x))/(max(x)-min(x))
  return(standard1)
}

#数据准备
memory<-cbind(new_iris[,1:4],new_iris[,1:4],new_iris[,1:4])
memory<-as.matrix(sapply(memory,nmaliz))


a1<-0:3
a2<-16:30
action<-c()
for(j in 1:length(a1)){
  a<-paste("(",a1[j],",",a2,")",sep="")
  action<-c(action,a)
}




#设置输入层
net_in<-12
#设置隐含层
net_hidden<-5  
#设置输出层
net_out<-60

#初始化w1 b1和w2 b2
w1<-matrix(runif(net_hidden*net_in,-1,1),net_hidden,net_in)  
b1<-rep(0.01,net_hidden)  

w2<-matrix(runif(net_out*net_hidden,-1,1),net_out,net_hidden)  
b2<-rep(0.01,net_out)  

sigmoid<-function(x){  
  y<-1/(1+exp(-x))  
  return(y)  
}  

#学习率
alpha<-0.1
mc<-0.8  
#循环次数
maxiter<-2000
#log
error_log<-NA
#out_log<-matrix(rep(0,length(memory)*maxiter),length(memory),maxiter)  

for(i in 1:maxiter){
  
  #数据抽取
  x<-round(runif(1,1,149))
  X_train<-t(as.matrix(memory[x,]))
  

  #forward propagation
  input<-w1 %*% t(X_train)+b1
  hidden_output<-sigmoid(input) 
  out_input<-w2%*%hidden_output+b2 
  #output1<-sigmoid(out_input)
  ###输出层不用执行sigmoid函数
  output1<-out_input	
  Q_max<-max(output1)          
  
  #获取新st
  new_train<-t(as.matrix(memory[x+1,]))
  #计算新Q
  input2<-w1 %*% t(new_train)+b1
  hidden_output2<-sigmoid(input2) 
  out_input2<-w2%*%hidden_output2+b2 
  #output2<-sigmoid(out_input2)  ###输出层不用执行sigmoid函数
  output2<-out_input2
  
  #从Q新矩阵里取元素标记与at-1=(1*2)相同的向量，记作Qat-1
  Q_new<-output2[which.max(output1)]
  action_n<-which.max(output1)
  
  #设定rt,g
  rt<-0.6
  g<-0.6
  
  #L
  L2<-rt+g*Q_max
  L1<-Q_new
  err<-(L1-L2)
  E<-sum(err^2)/2
  error_log[i]<-E
  
  #back propagation
  
  #dZ2<--err*sigmoid(output1)*(1-sigmoid(output1))  ###dZ2是err
  #dZ1<--t(w2)%*%dZ2*sigmoid(hidden_output)*(1-sigmoid(hidden_output))  ###dZ1<--t(w2)%*%dZ2*hidden_output*(1-hidden_output)
  dZ2<--err
  dZ1<--t(w2)%*%dZ2*hidden_output*(1-hidden_output)
  
  dw2<-dZ2%*%t(hidden_output)   
  dw1<-dZ1%*%X_train 
  
  db2<-sum(dZ2) ###有误
  db1<-sum(dZ1)
  
  if(i==1){  
    
    w2<-w2+alpha*dw2  
    w1<-w1+alpha*dw1 
    
    b2<-b2+alpha*db2  
    b1<-b1+alpha*db1
    
  } else{  
    
    w2<-w2+(1-mc)*alpha*dw2+mc*dw2old
    w1<-w1+(1-mc)*alpha*dw1+mc*dw1old 
    
    b2<-b2+(1-mc)*alpha*db2+mc*db2old
    b1<-b1+(1-mc)*alpha*db1+mc*db1old 

  }  
  
  dw1old<-dw1 
  dw2old<-dw2 
  db2old<-db2
  db1old<-db1
    
  
  #判断使用新action还是随机选用旧action
  c=0.8
  c_min=0.1
  c_1=0.2
  c=max(c-c_1,c_min)
  prob<-rbinom(1, 1, c)
  if(as.logical(prob)){
    new_action<-sample(action,1)
  }else{
    new_action<-action[action_n]
  }
  
  print(new_action)
  
}








####################################################################################################





