from Env import env
from RL_brain import DeepQNetwork
from prediction_algo import Prediciton
from Data_interaction import DataInteraction

def run_env():
    step = 0
    startId = DI.getStartId()
    col_tem = 3
    col_hum = 4
    col_tem_out = 3
    col_hum_out = 4
    col_tem_pre = 3
    col_tem_pre = 4
    col_action = 9
#for episode in range(1):
    #预测下一时序的室外参数？
    prediction_tem = Pre._train_prediction(step,col_tem_pre,startId,num = 10000)
    prediction_hum = Pre._train_prediction(step,col_hum_pre,startId,num = 10000) 
    # initial observation
    s_tem = DI.getData(step,col_tem,startId)[0][col_tem]
    s_hum = DI.getData(step,col_hum,startId)[0][col_hum]
    s_tem_out = DI.getData(step,col_tem_out,startId)[0][col_tem_out]
    s_hum_out = DI.getData(step,col_hum_out,startId)[0][col_hum_out]

    observation = [s_tem,s_hum,s_tem_out,s_hum_out,prediction_tem,prediction_hum] #从数据表中获取s的数据(此处的s是用的预测室外参数)
    action = RL.choose_action(observation)
    DI.pushData(step,col_action,startId,action)

    step += 1 #每个step代表控制时间间隔50S

    while True:
        # fresh env
        #env.render()

        # RL choose action based on observation
        

        # RL take action and get next observation and reward
        observation_, reward, done, observation, action = env.step(step)
        # 将t和t-1的数据存入memory
        RL.store_transition(observation, action, reward, observation_)

        action_ = RL.choose_action(observation_)
         
        #动作输出并存入s,a数据库

        if (step > 201) and ((step+1) % 5 == 0): #获得200个transition之后开始学习，每5步学习一次
            RL.learn()

        # swap observation
        #observation = observation_

        # break while loop when end of this episode
        if done:
            break
        step += 1

    # end of game
    print('episode over')
    #env.destroy()


if __name__ == "__main__":
    # maze game
    env = env()
    DI = DataInteraction()
    Pre = Prediction()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      # learning_rate=0.01,
                      # reward_decay=0.9,
                      # e_greedy=0.9,
                      # replace_target_iter=200,
                      # memory_size=2000,
                      # output_graph=True
                      )
    env.run_env()
    # env.mainloop()
    RL.plot_cost()
