This environment is created for the experiment in Tsinghua university 
Please install all the package in requirment.txt first. 
Then run pip install -e . to install the environment

Using Q and double deep Q learning to train a agent to improve thermal comfort, 
Generally, the agent takes actions based on state to maximum cumulative reward
Here, the agent changes temperature setpoint based on skin temperature to maximum long-term thermal comfort
In this case,state, action, reward are:
state: there is 7 state, please check office_env.py _process_state function
Action: 0: decrease setpoint 2 degree, 1: decrease setpoint 1 dgreee, 0: no change
		2: increase setpoint 1 degree, 3: increase setpoint 2 degree.
Rewared: thermal comfort level 


For testing version: 
skin temperature is mean skin temperature calculated by PierceSET model
thermal comfort level is PPD cacluated by PMV.


For real version;
Skin temperature is wrist skin temperature measured by smartband
Thermal comfort level is the real feedback from occupant

To run the testing version: python main.py 

