import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from single_goal_environment import RobotWorld

from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv
import os


env = RobotWorld(
    render_mode=None
)
# vectorize environment
n_cpu = 6
env = DummyVecEnv([lambda: env])

load_steps = 7000000
save_steps = 10000000

model_dir = "models/1706883391"
model_zip = f"PPO_MODEL_{load_steps}"
model = PPO.load(f"{model_dir}/{model_zip}")

model.set_env(env=env)

TIMESTEPS = 3000000
model.learn(
    total_timesteps=TIMESTEPS,
    callback=None,
    log_interval=1,
    tb_log_name="PPO",
    reset_num_timesteps=False
)

model.save(f"{model_dir}/PPO_MODEL_{save_steps}")


# NOTES 
# 1. train for much much longer, from 7 to 10
# 2. check the reward function well
# 3. search online if the observation given are enough for the agent, and a reward function that is good
# for this type of rl