from environment import Robot
from stable_baselines3 import PPO 
import gym
import sys

models_dir = "models/1703713312"

env = Robot()

model_path = f"{models_dir}/420000.zip"
model = PPO.load(model_path, env=env)

episodes = 500

for ep in range(episodes):
    obs, info = env.reset()
    truncated = False
    while not truncated:
        obs = obs
        action, _states = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()
        