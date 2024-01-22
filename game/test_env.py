from single_goal_environment import RobotWorld

env = RobotWorld(render_mode=None)

# checkenv also
print("Using check_env to verify the custom environemnt..")
from stable_baselines3.common.env_checker import check_env
check_env(env)
print("Check_env terminated, no errors..")
print()
print("Beginning of random action on the environment..")
obs, info = env.reset(seed=0)

for _ in range(10000000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset(seed=0)

env.close()