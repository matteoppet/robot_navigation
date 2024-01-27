from single_goal_environment import RobotWorld

from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv
import os


env = RobotWorld(
    render_mode="human"
)
# vectorize environment
n_cpu = 6
env = DummyVecEnv([lambda: env])


model_dir = "models/1706282098"
model_zip = "PPO_MODEL_200000"
model = PPO.load(f"{model_dir}/{model_zip}")

model.set_env(env=env)

TIMESTEPS = 200000
model.learn(
    total_timesteps=TIMESTEPS,
    callback=None,
    log_interval=1,
    tb_log_name="PPO",
    reset_num_timesteps=False
)

model.save(f"{model_dir}/PPO_MODEL_{TIMESTEPS}")