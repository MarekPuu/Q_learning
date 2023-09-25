import numpy as np
import random
import pickle

folder_name = "Q-Tables"

class QLearningAgent:
    def __init__(self, agent_name,board_length, discount=0.9, learning_rate=0.5, epsilon=0.1):
        self.agent_name = agent_name
        self.discount = discount
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.q_table = {}
        self.board_length = board_length
        self.initialize()

    def initialize(self):
        print("Initializing QLearningAgent")
        self.load_q_table()

    # Returns the state of the board as a string
    def get_state(self, board):
        return ''.join(board)
    
    def q_table_by_state(self,state):
        return self.q_table[state]
    
    def choose_action(self, state,use_random=False):
        if(state not in self.q_table):
            self.q_table[state] = [0] * self.board_length   
        for i in range(self.board_length ):
            if(state[i] != ' '):
                self.q_table[state][i] = -100

        if use_random and np.random.uniform(0, 1) < self.epsilon:
            available_actions = [i for i, x in enumerate(state) if x == ' ']
            return random.choice(available_actions)
        else:
            q_value = np.argmax(self.q_table[state])
            return q_value
        
    def learn(self, old_state, new_state, action, reward):
        old_q_value = self.q_table.get((old_state), None)

        if(new_state not in self.q_table):
            self.q_table[new_state] = [0] * self.board_length  

        if old_q_value is None:
            self.q_table[old_state] = [0] * self.board_length
            self.q_table[old_state][action] = reward
        else:
            temporal_difference = reward + (self.discount * np.max((self.q_table[new_state])) ) - old_q_value[action]
            new_q_value = old_q_value[action] + (self.learning_rate * temporal_difference)
            self.q_table[old_state][action] = new_q_value


    def save_q_table(self):
        try:
            global folder_name
            filename = f'{folder_name}/{self.agent_name}.pkl'
            print("Saving q_table to ",filename)
            with open(filename, "wb") as file:
                pickle.dump(self.q_table, file)
        except Exception as e:
            print(e)            

    def load_q_table(self):
        print("Loading q_table for: ", self.agent_name)
        try:
            global folder_name
            filename = f'{folder_name}/{self.agent_name}.pkl'
            with open(filename, "rb") as file:
                self.q_table = pickle.load(file)        
        except Exception as e:
            print(e)
            