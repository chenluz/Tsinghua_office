from gym.envs.registration import register

register(
    id='band_control-v0',
    entry_point='Tsinghua_office.envs:OfficeEnv'
)

