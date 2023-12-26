from environment import Robot

env = Robot()

# Test with random action
# for ep in range(500):
#     obs, info = env.reset()
#     truncated = False

#     while not truncated:
#         random_action = env.action_space.sample()
#         obs, reward, terminated, truncated, info = env.step(random_action)
#         env.render()


from stable_baselines3 import PPO
import os
import time

models_dir = f"models/{int(time.time())}"
logs_dir = f"logs/{int(time.time())}"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logs_dir):
	os.makedirs(logs_dir)
	
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logs_dir)

TIMESTEPS = 10000
iters = 0
while True:
	iters += 1
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{TIMESTEPS*iters}")
	
# how to use render