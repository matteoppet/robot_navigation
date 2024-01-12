from gym.envs.registration import register

register(
    id="gym_environments/RobotWorld-v0",
    entry_point="gym.environments.envs:RobotWorldEnv",
)