
#library&const
"""
This part of code is the Deep Q Network (DQN) brain.

Using:
Tensorflow: r1.2
"""
# #问题点：
#     -参数：
#           - Q‘网络参数更新iteration
#           - epsilon每次增加的量
#     -与Prototype不同之处：s,r,a,s_在每次获得s_时，获得（s,r,a,s_） 作为参数传入store_transition(self, s, a, r, s_)

import numpy as np
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)

class DeepQNetwork:
	def __init__(
		self,
		n_actions ,
		n_features,
		learning_rate=0.003,
		reward_decay=0.99,
		#e_greedy=0.1,
		epsilon_max=0.99,
		replace_target_iter=50, #Q参数替换的迭代次数
		memory_size=500,
		batch_size=48,
		e_greedy_increment=0.01, #89次加到99
		output_graph=False,
	):
		#动作数量
		self.n_actions = n_actions

		#状态数量
		self.n_features = n_features

		#learning_rate学习速率
		self.lr = learning_rate

		#Q-learning中reward衰减因子
		self.gamma = reward_decay

		#e-greedy的选择概率最大值
		self.epsilon_max = epsilon_max

		#更新Q现实网络参数的步骤数
		self.replace_target_iter = replace_target_iter

		#存储记忆的数量
		self.memory_size = memory_size

		#每次从记忆库中取的样本数量
		self.batch_size = batch_size

		#每次动作输出epsilon增大的量
		self.epsilon_increment = e_greedy_increment

		#epsilon的初始值
		self.epsilon = 0.1

		#学习的步骤初始值
		self.learn_step_counter = 0

		#初始化memory为zero
		self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

		#构建target_net&evaluate_net(BP算法，e的维度：对每个输出神经元求loss平方差进行反馈传播)
		self._build_net()
		t_params = tf.get_collection('target_net_params')
		e_params = tf.get_collection('eval_net_params')
		self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params)]

		self.sess = tf.Session() #创建会话

		if output_graph:
			tf.summary.FileWriter("logs/", self.sess.graph) #将graph等event传入log目录下? 

		self.sess.run(tf.global_variables_initializer()) #对variable进行初始化的代码
		self.cost_his = [] #?

	def _build_net(self):

		#all inputs
		self.s = tf.placeholder(tf.float32,[None, self.n_features],name='s')
		self.s_ = tf.placeholder(tf.float32,[None, self.n_features], name = 's_')
		self.r = tf.placeholder(tf.float32, [None, ], name = 'r')
		self.a = tf.placeholder(tf.float32, [None, ], name = 'a')

		w_initializer, b_initializer = tf.random_normal_initializer(0.,0.3), tf.constant_initializer(0.1)

		#build_evaluate_net
		with tf.variable_scope('eval_net'):
			e1 = tf.layers.dense(self.s, 20, tf.nn.relu, kernel_initializer=w_initializer, bias_initializer=b_initializer,name='e1')
			self.q_eval = tf.layers.dense(e1, self.n_actions, kernel_initializer=w_initializer, bias_initializer=b_initializer,name='q')

		#build_target_net
		with tf.variable_scope('target_net'):
			t1 = tf.layers.dense(self.s_,20,tf.nn.relu, kernel_initializer=w_initializer, bias_initializer=b_initializer,name='t1')
			self.q_next = tf.layers.dense(t1,self.n_actions, kernel_initializer=w_initializer,
                                          bias_initializer=b_initializer, name='t2')

		with tf.variable_scope('q_target'):
			q_target = self.r + self.gamma * tf.reduce_max(self.q_next, axis=1, name='Qmax_s_')
			self.q_target = tf.stop_gradient(q_target) #

		with tf.variable_scope('q_eval'):
			a_indices = tf.stack([tf.range(tf.shape(self.a)[0], dtype=tf.int32), self.a], axis=1)
			self.q_eval_wrt_a = tf.gather_nd(params=self.q_eval, indices=a_inidices)

		with tf.variable_scope('loss'):
			self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval_wrt_a, name = 'TD_error'))

		with tf.variable_scope('train'):
			self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

	def store_transition(self, s, a, r, s_):
		if not hasattr(self, 'memory_counter'):
			self.memory_counter = 0
		transition = np.hstack((s, [a,r], s_))
		index = self.memory_counter % self.memory_size
		#replace the old memory with new memory
		self.memory[index, :] = transition
		self.memory_counter += 1

	def choose_action(self, observation):
		# 获取batch的维度，用以feed到placeholder
		if  np.random.uniform() < self.epsilon:
			action_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
			action = np.argmax(actions_value)
		else:
			action = np.random.randint(0,self.n_actions)
		return action

	def learn(self):
		#检查并替换目标参数
		if self.learn_step_counter % self.replace_target_iter == 0:
			self.sess.run(self.target_replace_op)
			print('\ntargrt_params_replaced\n')

		#sample batch memory from all memory
		if self.memory_counter > self.memory_size:
			sample_index = np.random.choice(self.memory_size, size=self.batch_size)
		else:
			sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
		batch_memory = self.memory[sample_index, :]

		_, cost = self.sess.run(
			[self._train_op, self.loss],
			feed_dict={
				self.s: batch_memory[:, :self.n_features],
				self.a: batch_memory[;, self.n_features],
				self.r: batch_memory[:, self.n_features+1],
				self.s_: batch_memory[:, -self.n_features:],
			})

		self.cost_his.append(cost)

		#increase epsilon
		self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
		self.learn_step_counter += 1

	def plot_cost(self):
		import matplotlib.pyplot as plt 
		plt.plot(np.arange(len(self.cost_his)),self.cost_his)
		plt.ylabel('Cost')
		plt.xlabel('traing steps')
		plt.show()

if __name__ == '__main__':
	DQN = DeepQNetwork(n_actions = ,n_features = 6, output_graph = True)
####if __name__ == '__main__'的意思是：当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。


