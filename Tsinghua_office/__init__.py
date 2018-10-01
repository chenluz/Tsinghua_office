from gym.envs.registration import register

register(
    id='band_control-v0',
    entry_point='Tsinghua_office.envs:OfficeTestEnv'
)

register(
    id='band_control-v1',
    entry_point='Tsinghua_office.envs:OfficeEnv'
)

