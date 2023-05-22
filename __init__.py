from gym.envs.registration import register
register(
    id='FourInARow/Sag-Env',
    entry_point='envs.four_env:FourInARowEnv',
    max_episode_steps=300,
)
print(f"registered")
