from environment import Robot
from stable_baselines3.common.env_checker import check_env

env = Robot()
# check_env(env)

for ep in range(500):
    obs, info = env.reset()
    truncated = False

    while not truncated:
        random_action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(random_action)
        env.render()