import numpy as np
import pymssql
import os,time

class DataInteraction(object):
		def __init__(
			self,
			server = "219,223,222,210",
			user = "userFang",
			password = "admin",
			):
			# IP/账号/密码
			self.server = server #温度范围x风速范围？
			self.user = user
			self.password = password


 		def getData(self,timeStep,col,startId,num = 2):
 			self.conn = pymssql.connect(self.server,self.user,self.password,database='master')
			self.cursor = self.conn.cursor()
 			self.table = cursor.execute("use maGroup")
 			self.cursor.execute("select top '%d' * from dbo.BaseData_Y2018 order by datew desc"%(num))
    		a = self.cursor.fetchall()
    		#id = timestep+(起始id); 第col列的值存在
    		while (!(a[0][0] == timeStep* num + startId && a[0][col] != None)):
    			self.cursor.execute("select top '%d' * from dbo.BaseData_Y2018 order by datew desc"%(num))
    			time.sleep(0.1)
    			a = self.cursor.fetchall()
    		conn.close()
    		return a

    	def pushData(self,timeStep,col,startId,action):
  			self.conn = pymssql.connect(self.server,self.user,self.password,database='master')
			self.cursor = self.conn.cursor()
 			self.table = cursor.execute("use maGroup")
 			self.cursor.execute("update dbo.BaseData_Y2018 set action = '%d' where  id = '%d' "%(action,timeStep*10 + startId)) 
 			conn.close()  		

 		def getStartId(self):
 			self.conn = pymssql.connect(self.server,self.user,self.password,database='master')
			self.cursor = self.conn.cursor()
 			self.table = cursor.execute("use maGroup")
 			self.cursor.execute("select top 1 * from dbo.BaseData_Y2018 order by datew desc")
    		step = self.cursor.fetchone()
    		#id = timestep+(起始id); 第col列的值存在
    		# while (not(step[0]%10 == 0)):
    		# 	self.cursor.execute("select top 1 * from dbo.BaseData_Y2018 order by datew desc")
    		# 	time.sleep(0.1)
    		# 	step = self.cursor.fetchone()
    		conn.close()
    		return step[0]
 		# def preData(self,timestep,col,startId):
 		# 	self.conn = pymssql.connect(self.server,self.user,self.password,database='master')
			# self.cursor = self.conn.cursor()
 		# 	self.table = cursor.execute("use maGroup")
 		# 	self.cursor.execute("select top 100 * from dbo.BaseData_Y2018 order by datew desc")
   #  		a = self.cursor.fetchall()
   #  		#id = timestep+(起始id); 第col列的值存在
   #  		while (!(a[0][0] == timeStep*10 + startId && a[0][col] != None)):
   #  			self.cursor.execute("select top 100 * from dbo.BaseData_Y2018 order by datew desc")
   #  			a = self.cursor.fetchall()
   #  		conn.close()
   #  		return a[0][col]