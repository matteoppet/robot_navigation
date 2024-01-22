from single_goal_environment import RobotWorld

from stable_baselines3 import PPO
import os
import time

env = RobotWorld(
    render_mode="human"
)

# Creation dirs
models_dir = f"models/{int(time.time())}"
logs_dir = f"logs/{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    print("> Models dir created..")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print("> Logs dir created..")


env.reset()

model = PPO(
    "MultiInputPolicy",
    env,
    learning_rate=0.0003,
    gamma=0.99,
    n_epochs=10,
    verbose=1,
    tensorboard_log=logs_dir,
    device="cuda" # GPU not used, instead CPU is used
)

# checkpoint = 200000
# id_model = 1705946078
# models_dir = f"models/{id_model}"
# model = PPO.load(f"{models_dir}/{checkpoint}")

TIMESTEPS = 20000
iters = 0
while True:
    iters += 1
    
    # Only for models already created
    # model.set_env(env=env)

    model.learn(
        total_timesteps=TIMESTEPS,
        reset_num_timesteps=False,
        tb_log_name="PPO",
    )

    model.save(f"{models_dir}/{TIMESTEPS*iters}")



""" IMPORT
Open Command prompt and use the conda TF environment to run the training.
GPU training works only on conda environment.

Command to activate the environment:  conda activate tf

Now let's implement the other things.
"""

# ctrl + shift + p = open todo.md