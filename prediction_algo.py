import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import xlrd
import openpyxl
from sklearn.datasets import load_boston
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from Data_interaction import DataInteraction 


class Prediction():
	def __init__(self)：
		DI = DataInteraction()

	def _train_prediction(self,timeStep,col,startId,num = 16002):
	#导入数据？
		table = DI.getData(timeStep,col,startId,num)

	# #数据manipulation
	# 	nrows = table.nrows #行数？
	# 	#c1=arange(0,nrows,1) #0到行数的list
		table.reverse()
		table = np.array(table)[:,col]

	# 	cols_list =table.col_values(x)      
	# 	cols_array=np.array(cols)# 把list转换为矩阵进行矩阵操作
	# 	datamatrix[:,x]=cols_array# 把数据进行存储 

		# temData = datamatrix[:,0] #？？？
		# humData = datamatrix[:,1] #？？？

		x_predcit = table[-4:]

		x = np.zeros((num-4,4)) #数据行数-4

		for i in range(num-4):
		    x[i][0:4] = table[i:i+4]
		x_target_tem = table[4:]

		x_train, x_test, y_train, y_test = train_test_split(x, x_target_tem, test_size=0, random_state=33)

	#训练数据和测试数据进行标准化处理
		ss_x = StandardScaler()
		x_train = ss_x.fit_transform(x_train)
		x_predict =ss_x.fit_transform(x_predict)
		# x_test = ss_x.transform(x_test)

		ss_y = StandardScaler()
		y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
		# y_test = ss_y.transform(y_test.reshape(-1, 1))

		# 4.1 支持向量机模型进行学习和预测
		# 线性核函数配置支持向量机
		linear_svr = SVR(kernel="linear")
		# 训练
		linear_svr.fit(x_train, y_train)
	
		# 预测 保存预测结果
		linear_svr_y_predict = linear_svr.predict(x_predict)
		linear_svr_y_predict = ss_y.inverse_transform(linear_svr_y_predict)

		return linear_svr_y_predict
		# 多项式核函数配置支持向量机
		# poly_svr = SVR(kernel="poly")
		# # 训练
		# poly_svr.fit(x_train, y_train)
		# # 预测 保存预测结果
		# poly_svr_y_predict = linear_svr.predict(x_test)
