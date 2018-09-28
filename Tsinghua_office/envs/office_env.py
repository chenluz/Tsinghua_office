import gym
from gym import error, spaces, utils
from gym.utils import seeding
from .action import openHab
from .action import plugWise
from .observation import InfluxDB
from .simulator import skinTemperature
from .simulator import feedback
import numpy as np

# ref: https://github.com/openai/gym/tree/master/gym/envs
Ta_max = 30
Ta_min = 18
Rh_max = 51
Rh_min = 50
class OfficeEnv(gym.Env):

	def __init__(self):
		self.nS = 1 # state space
		self.nA = 5 # action space 
		self.is_terminal = False
		self.step_count = 0
		self.cur_Skin = 0
		self.cur_Ta = 0
		self.cur_Rh = 0 
		self.action = 0
		self.reward = 0
		self.vote = feedback()
			

	def _step(self, action):
		""" take action and return next state and reward
		Parameters
		----------
		action: int, value is 0, 1, 2, 3, 4
			(0: temperature decrease 2 degreee; 1: decrease 1 degree; 2: no change, 
				3: increase 1 degree, 4: increase 2 degree)

		Return 
		----------
		ob:  array of state
		reward: float , PMV value

		"""
		# get air temperature and air humidity after action
		incr_Ta = action - round(self.nA/2)
		self.action = action
		pre_Ta = self.cur_Ta
		pre_Rh = self.cur_Rh
		self.cur_Ta  = self.cur_Ta + incr_Ta
		self.cur_Rh  = np.random.choice(np.arange(Rh_min, Rh_max, 1))


		if self.cur_Ta > Ta_max:
			self.is_terminal = True
		elif self.cur_Ta < Ta_min:
			self.is_terminal = True

		# get PPD after action from PMV model
		self.reward = -1*self.vote.comfPMV(self.cur_Ta, self.cur_Ta, self.cur_Rh, 1.0)[1] ##PPD

		# get mean skin temperature from PierceSET model
		self.cur_Skin = skinTemperature().comfPierceSET(self.cur_Ta, self.cur_Ta, self.cur_Rh, 1.0)
		state = self._process_state(self.cur_Skin)
	
		return state, self.reward, self.is_terminal, {}

	def _process_state(self, skin_temp):
		""" Divide skin temperature into 8 state
		Parameters
		----------
		skin_temp: float,  
		Return 
		----------
		state: int

		"""
		if skin_temp < 32.5:
			state = 0
		elif skin_temp < 33:
			state = 1
		elif skin_temp < 34:
			state = 2
		elif skin_temp < 34.5:
			state = 3
		elif skin_temp < 34.9:
			state = 4
		elif skin_temp < 35:
			state = 5
		else:
			state = 6
		return state



	def _reset(self):
		self.is_terminal = False
		self.cur_Ta = np.random.choice([Ta_min, Ta_max])
		self.cur_Rh  = np.random.choice(np.arange(Rh_min, Rh_max))
		self.cur_Skin = skinTemperature().comfPierceSET(self.cur_Ta, self.cur_Ta, self.cur_Rh, 1.0)
		state = self._process_state(self.cur_Skin)
		return state


	def _print(self):
		print(self.cur_Ta, self.cur_Rh)


	def _render(self, mode='human', close=False):
		pass


