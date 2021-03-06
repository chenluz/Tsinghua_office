## reference:https://github.com/dennybritz/reinforcement-learning/tree/master/TD

import gym
import itertools
import matplotlib
import numpy as np
import pandas as pd
import sys
from collections import defaultdict, OrderedDict
from lib import plotting
import time
import csv

if "../" not in sys.path:
  sys.path.append("../") 

matplotlib.style.use('ggplot')

MAX_STEP = 200

##ref: https://github.com/dennybritz/reinforcement-learning
def make_epsilon_greedy_policy(Q, nA):
    """
    Creates an epsilon-greedy policy based on a given Q-function and epsilon.
    
    Args:
        Q: A dictionary that maps from state -> action-values.
            Each value is a numpy array of length nA (see below)
        nA: Number of actions in the environment.
    
    Returns:
        A function that takes the observation and epsilon as an argument and returns
        the probabilities for each action in the form of a numpy array of length nA.
    
    """
    def policy_fn(observation,epsilon):
        """
        Args:
          observation: the state of the environment
          epsilon: The probability to select a random action . float between 0 and 1.
                   decreased with the increase of runned episodes  
        """
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[observation])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fn


def q_learning(env, num_episodes, discount_factor, alpha, epsilon, epsilon_min,
 epsilon_decay, folder):
    """
    Q-Learning algorithm: Off-policy TD control. Finds the optimal greedy policy
    while following an epsilon-greedy policy
    
    Args:
        env: office environment.
        num_episodes: Number of episodes to run for.
        discount_factor: Lambda time discount factor.
        alpha: TD learning rate.
        epsilon: Chance the sample a random action. Float betwen 0 and 1.
    
    Returns:
        A tuple (Q, episode_lengths).
        Q is the optimal action-value function, a dictionary mapping state -> action values.
        stats is an EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
    """
    
    # The final action-value function.
    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.nA))

    # Keeps track of useful statistics
    stats = plotting.EpisodeStats(
        episode_lengths=np.zeros(num_episodes),
        episode_rewards=np.zeros(num_episodes))    
    
    # The policy we're following

    policy = make_epsilon_greedy_policy(Q, env.nA)
    
    for i_episode in range(num_episodes):
  
        if epsilon > epsilon_min and i_episode > 500:
            # complete random exploration 500 episodes, 
            # then decrase exploration till epsilon less than epsilon_min
            epsilon *= epsilon_decay
        sys.stdout.flush()

        # Reset the environment and pick the first action episode
        state = env.reset()

        # One step in the environment
        for t in range(0, MAX_STEP):
        
            # Take a step
            action_probs = policy(state, epsilon)

            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            next_state, reward, done, _ = env.step(action) 


            # Update statistics
            stats.episode_rewards[i_episode] += reward
            stats.episode_lengths[i_episode] = t
        

            write_csv(folder, state, action, next_state, reward, stats.episode_rewards[i_episode])
            
            # TD Update
            best_next_action = np.argmax(Q[next_state])    
            td_target = reward + discount_factor * Q[next_state][best_next_action]
            td_delta = td_target - Q[state][action]
            Q[state][action] += alpha * td_delta

            if done: 
                break
                
            state = next_state
        print("episode: {}/{}, score: {}, e: {:.2}"
            .format(i_episode, num_episodes,  stats.episode_rewards[i_episode], epsilon))
        write_Q(folder, Q)

    
    return Q, stats


def write_csv(folder, state, action, next_state, reward, episodes_rewards):
    with open(folder + ".csv", 'a', newline='') as csvfile:
        fieldnames = ['state', 'action', 'next state', 'reward']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({fieldnames[0]: state, fieldnames[1]: action, fieldnames[2]:next_state,
                fieldnames[3]:reward})


def write_Q(folder, Q_dict):
    with open(folder + "_Q.csv", 'a', newline='') as csvfile:
        OrderdQ_dict = OrderedDict(sorted(Q_dict.items(), key=lambda t: t[0]))
        fieldnames = []
        row = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for k, v in OrderdQ_dict.items():
            row[k] = np.argmax(v)
            fieldnames.append(row[k])
        writer = csv.DictWriter(csvfile, fieldnames=range(0,7))
        writer.writerow(row)                                                                                                            