import sys
import os

# Assuming current_file.py is located in training_agent directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from single_goal_environment import RobotWorld

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

import os
import time


#### Creation dirs
models_dir = f"models/{int(time.time())}"
logs_dir = f"logs/{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    print("> Models dir created..")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print("> Logs dir created..")


#### Setup env
env = RobotWorld(render_mode="human")
# vectorize environment
n_cpu = 6
env = DummyVecEnv([lambda: env])


#### Setup model
model = PPO(
    "MultiInputPolicy",
    env,
    learning_rate=0.0003,
    gamma=0.99,
    n_epochs=10,
    verbose=1,
    tensorboard_log=logs_dir,
    device="cuda"
)

#### Train model
TIMESTEPS = 200000
model.learn(
    total_timesteps=TIMESTEPS,
    callback=None,
    log_interval=1,
    tb_log_name="PPO",
    reset_num_timesteps=False
)

model.save(f"{models_dir}/PPO_MODEL_{TIMESTEPS}")