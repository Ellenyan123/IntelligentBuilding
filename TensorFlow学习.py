TensorFlow的运算是数据流的图
	- 对象
		- operation对象，计算节点
		- Tensor对象，表示不同操作间的数据节点
			Tensor：不同维度、行列的数据，作为神经网络的输入
	- process 
		- 开始任务，即创建一个默认的图
		- 实例代码：
			import tensorflow as tf
			import numpy as np

			c=tf.constant(value=1)
			#print(assert c.graph is tf.get_default_graph())
			print(c.graph)
			print(tf.get_default_graph())

			g=tf.Graph()
			print("g:",g)
			with g.as_default():
			    d=tf.constant(value=2)
			    print(d.graph)
			    #print(g)

			g2=tf.Graph()
			print("g2:",g2)
			g2.as_default()
			e=tf.constant(value=15)
			print(e.graph)		

	- 上下文管理器（contextor）
		- 资源的创建和释放场景

			Raw one：

			class Database(object):
 
			    def __init__(self):
			        self.connected = False
			 
			    def connect(self):
			        self.connected = True
			 
			    def close(self):
			        self.connected = False
			 
			    def query(self):
			        if self.connected:
			            return 'query data'
			        else:
			            raise ValueError('DB not connected ')
			 
			def handle_query():
			    db = Database()
			    db.connect()
			    print 'handle --- ', db.query()
			    db.close()
			 
			def main():
			    handle_query()
			 
			if __name__ == '__main__':
			    main()

			使用修饰器进行改写：

			class Database(object):
				    ...
				 
				def dbconn(fn):
				    def wrapper(*args, **kwargs):
				        db = Database()
				        db.connect()
				        ret = fn(db, *args, **kwargs)
				        db.close()
				        return ret
				    return wrapper
				 
				@dbconn
				def handle_query(db=None):
				    print 'handle --- ', db.query()
				 
				def main():
				    ...

