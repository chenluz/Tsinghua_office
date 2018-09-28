""" This environment is created for the experiment in Tsinghua university 
Please install all the package in requirment.txt first. 
Then run pip install -e . to install the environment

Using Q learning to train a agent to improve thermal comfort, 
Generally, the agent takes actions based on state to maximum reward
Here, the agent changes temperature setpoint based on skin temperature to maximum thermal comfort
In this case,state, action, reward are:
state: there is 7 state, please check office_env.py _process_state function
Action: 0: decrease setpoint 2 degree, 1: decrease setpoint 1 dgreee, 0: no change
		2: increase setpoint 1 degree, 3: increase setpoint 2 degree.
Rewared: thermal satisfaction 


For testing version: 
skin temperature is mean skin temperature calculated by PierceSET model
thermal satisfaciton is PPD cacluated by PMV.

To run the testing version: python main.py 
""

