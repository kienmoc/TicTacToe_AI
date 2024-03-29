import random
import pickle

class QLearning:

    def __init__(self,epsilon=0.2, lr=0.3, gamma=0.9):
        self.epsilon = epsilon
        self.lr = lr
        self.gamma = gamma
        self.Q = {}
        self.last_board = None
        self.q_last = 0.0
        self.state_action_last = None

    def game_begin (self):
        self.last_board = None
        self.q_last = 0
        self.state_action_last = None

    def get_action (self, state, possible_moves):
        self.last_board = tuple (state)

        if random.random () < self.epsilon:
            move = random.choice (possible_moves)
            self.state_action_last = (self.last_board, move)
            self.q_last = self.get_Q (self.last_board, move)

            return move
        else:
            Q_lists = []
            for action in possible_moves:
                Q_lists.append (self.get_Q (self.last_board, action))

            max_Q = max (Q_lists)
            if Q_lists.count (max_Q) > 1:
                best_option = [i for i in range (len (possible_moves)) if Q_lists[i] == max_Q]
                i = random.choice (best_option)
            
            else:
                i = Q_lists.index (max_Q)

            self.state_action_last = (self.last_board, possible_moves[i])
            self.q_last = self.get_Q (self.last_board, possible_moves[i])

            return possible_moves[i]

    def get_Q (self, state, action):
        if (self.Q.get ((state, action))) is None:
            self.Q[(state, action)] = 1
        return self.Q.get ((state, action))
    
    def update_Q (self, reward, state, possible_moves):
        Q_lists = []
        for move in possible_moves:
            Q_lists.append (self.get_Q (tuple (state), move))
        if Q_lists:
            max_Q_next = max (Q_lists)
        else:
            max_Q_next = 0
        
        self.Q[self.state_action_last] = self.q_last + self.lr * ((reward + self.gamma * max_Q_next) - self.q_last)
    
    def saveQtable(self,file_name):  #save table
        with open(file_name, 'wb') as handle:
            pickle.dump(self.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQtable(self,file_name): # load table
        with open(file_name, 'rb') as handle:
            self.Q = pickle.load(handle)