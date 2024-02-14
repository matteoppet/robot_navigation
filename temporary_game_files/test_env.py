from environment import RobotWorld

env = RobotWorld(render_mode="human")

obs, info = env.reset(seed=0)

for _ in range(10000000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset()

env.close()