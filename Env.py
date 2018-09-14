# All states: reward = abs(T-26) /1000
#T is temperature of states

# import & define const 

# 空调的档位低、中、高、自动
# 读取s、s_的时候，确保在s_更新的即时：
	# 方案一：数据库更新完数据即时发送指令，收到指令读取数据
	# 方案二：固定时间间隔获取数据库数据更新情况，在获取数据更新完的即时，读取数据
import numpy as np
import time
import sys

class Env(object):
		def __init__(self):
			# super(Env,self).__init__()
			self.action_space = [] #温度范围x风速范围？
			self.n_actions = len(self.action_space)
			self.n_features = 6#?
			#self.title('Env')
			#self.geometry('{}x{}'.format()) #设置窗口大小
 		#def reset(self)
 			#self.update()
 			#time.sleep(0.1)
 			#origin = np.array([])
 			#return (np.array())

 		def step(self, timeStep):
 			#以t为索引读取数据，或者以序号索引读取数
 			#当前t的state，通过读取已经导入的采集数据
 			s_ = #获取state的数据?
 			s = #读取上一timestep的state数据?
 			a = #读取上一timestep的action数据?
 			#base_action = np.array([0,0]) #移动canvas的参数

 			#执行动作action作为参数

 			#读取上一timestep的温度计算reward?
 			reward = abs(_-26)/1000

 			#结束条件
 			if timeStep < 10000:
 				done = False
 			else:
 				done = True 
 			return s_, reward, done, s, a

 		# def render(self):
 		# 	self.update()

