import gym
from gym import error, spaces, utils
from gym.utils import seeding
from .observation import InfluxDB
import numpy as np
import csv
import datetime

# ref: https://github.com/openai/gym/tree/master/gym/envs
Ta_max = 30
Ta_min = 24
Rh_max = 51
Rh_min = 50
Tskin_max = 35.5
Tskin_min = 32


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
		self.db = InfluxDB(host='localhost', port=8086, username='chenlu',
            password='research', database='nus')
			

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

		# get obervation from Database
		ob_dict = self.db.get_observation("15m","60s")

		# get latest comfort feedback
		self.reward = ob_dict["thermal_comfort"]

		# get past 60s mean wrist skin temperature 
		self.cur_Skin = ob_dict["skin_temp_mean"]
		#state = self._process_state_table(self.cur_Skin)
		state = self._process_state_DDQN(self.cur_Skin)
	
		return state, self.reward, self.is_terminal, {}


	def _process_state_table(self, skin_temp):
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


	def _process_state_DDQN(self, skin_temp):
		""" convert skin temperature to value with 0 and 1
		Parameters
		----------
		skin_temp: float,  
		Return 
		----------
		state: float from 0 to 1

		""" 
		state = (skin_temp - Tskin_min)*1.0/(Tskin_max - Tskin_min) 
	
		return state



	def _reset(self):
		self.is_terminal = False
		self.cur_Ta = np.random.choice([Ta_min, Ta_max])
		self.cur_Rh  = np.random.choice(np.arange(Rh_min, Rh_max))
		self.cur_Skin = self.db.get_observation("15m","60s")["skin_temp_mean"]
		#state = self._process_state_table(self.cur_Skin)
		state = self._process_state_DDQN(self.cur_Skin)
		return state



	def _render(self, mode='human', close=False):
		pass

	def my_render(self, folder, model='human', close=False):
	    with open(folder + "_render.csv", 'a', newline='') as csvfile:
	        fieldnames = ['time', 'action', 'air_temp', 'air_humid', 'skin_temp', 'reward', "is_terminal"]
	        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	        writer.writerow({fieldnames[0]: datetime.datetime.utcnow(), 
	        	fieldnames[1]:self.action, 
				fieldnames[2]:self.cur_Ta, 
				fieldnames[3]:self.cur_Rh, 
				fieldnames[4]:self.cur_Skin,
				fieldnames[5]:self.reward,
				fieldnames[6]:self.is_terminal})




