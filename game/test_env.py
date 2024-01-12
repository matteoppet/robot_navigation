from single_goal_environment import RobotWorld, window_mode, window_size, clock

env = RobotWorld(window_mode=window_mode, window_size=window_size, clock_global_var=clock, render_mode="human")

# checkenv also
from stable_baselines3.common.env_checker import check_env
check_env(env)

obs, info = env.reset(seed=0)

for _ in range(10000000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset(seed=0)

env.close()