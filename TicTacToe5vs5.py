import pygame
import random
import time
from QLearning import QLearning

class Human5vs5:
    pass

class TicTacToe5vs5:

    def __init__ (self, training=False, pvp=False):
        self.board = [' '] * 25
        self.done = False
        self.pvp = pvp

        self.training = training
        self.player1 = None
        self.player2 = None
        self.aiplayer = None
        self.isAI = None

        self.player1_turn = None
        self.human_turn = None

        if not self.training:
            pygame.init ()
            self.ttt = pygame.display.set_mode ((720, 720))
            pygame.display.set_caption ("Tic Tac Toe")

    def possible_moves(self):
        return [moves + 1 for moves, v in enumerate(self.board) if v == ' ']

    def reset (self):
        if self.training:
            self.board = [" "] * 25
            return
        
        self.board = [" "] * 25
        if self.pvp:
            self.player1_turn = random.choice ([True, False])

            self.surface = pygame.Surface (self.ttt.get_size ())
            self.surface = self.surface.convert ()

            self.surface.fill ((250, 250, 250))

            pygame.draw.line (self.surface, (0, 0, 0), (144, 0), (144, 720), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (288, 0), (288, 720), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (432, 0), (432, 720), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (576, 0), (576, 720), 3)
            
            pygame.draw.line (self.surface, (0, 0, 0), (0, 144), (720, 144), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (0, 288), (720, 288), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (0, 432), (720, 432), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (0, 576), (720, 576), 3)

            return
        
        self.human_turn = random.choice ([True, False])
        
        self.surface = pygame.Surface (self.ttt.get_size ())
        self.surface = self.surface.convert ()

        self.surface.fill ((250, 250, 250))

        pygame.draw.line (self.surface, (0, 0, 0), (144, 0), (144, 720), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (288, 0), (288, 720), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (432, 0), (432, 720), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (576, 0), (576, 720), 3)
        
        pygame.draw.line (self.surface, (0, 0, 0), (0, 144), (720, 144), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (0, 288), (720, 288), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (0, 432), (720, 432), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (0, 576), (720, 576), 3)


    def show_board(self):
        self.ttt.blit(self.surface, (0, 0))
        pygame.display.flip()

    def mouse_click (self):
        (mouseX, mouseY) = pygame.mouse.get_pos ()

        if mouseX < 144:
            col = 0
        elif mouseX < 288:
            col = 1
        elif mouseX < 432:
            col = 2
        elif mouseX < 576:
            col = 3
        else:
            col = 4

        if mouseY < 144:
            row = 0
        elif mouseY < 288:
            row = 1
        elif mouseY < 432:
            row = 2
        elif mouseY < 576:
            row = 3
        else:
            row = 4

        return row * 5 + col + 1

    def is_win(self, ch):
        for i in range(5):
            if (self.board[i * 5] == ch and
                self.board[i * 5 + 1] == ch and
                self.board[i * 5 + 2] == ch and
                self.board[i * 5 + 3] == ch):
                return 1.0, True

        for j in range(5):
            if (self.board[j] == ch and
                self.board[j + 5] == ch and
                self.board[j + 10] == ch and
                self.board[j + 15] == ch):
                return 1.0, True

        for i in range(2):
            for j in range(2):
                if (self.board[i * 5 + j] == ch and
                    self.board[i * 5 + j + 6] == ch and
                    self.board[i * 5 + j + 12] == ch and
                    self.board[i * 5 + j + 18] == ch):
                    return 1.0, True

        for i in range(2):
            for j in range(2):
                if (self.board[i * 5 + 3 + j] == ch and
                    self.board[i * 5 + 3 + j + 4] == ch and
                    self.board[i * 5 + 3 + j + 8] == ch and
                    self.board[i * 5 + 3 + j + 12] == ch):
                    return 1.0, True
                    
        if not any(c == ' ' for c in self.board):
            return 0.5, True

        return 0.0, False



    def game_step (self, pos, is_X):
        if is_X:
            ch = 'X'
        else:
            ch = 'O'

        if self.board[pos - 1] != ' ':
            return -5, True

        self.board[pos - 1] = ch

        reward, done = self.is_win (ch)

        return reward, done
    

    
    def draw_move (self, pos, is_X):
        row = int ((pos - 1) / 5)
        col = (pos - 1) % 5

        centerX = ((col) * 144) + 35
        centerY = ((row) * 144) + 35

        if (is_X):
            reward, done = self.game_step (pos, is_X)
            font = pygame.font.Font(None, 30)
            x_image = pygame.image.load("resources/x.png").convert_alpha()
            scaled_x_image = pygame.transform.smoothscale(x_image, (75, 75))
            self.surface.blit(scaled_x_image, (centerX, centerY))
            self.board[pos - 1] = 'X'

            if reward == 1: 
                text = font.render('Player X won!', 1, (10, 10, 10))
                self.surface.blit(text, (10, 680))

            if reward == -5:
                font = pygame.font.Font(None, 30)
                text = font.render('Invalid move!', 1, (10, 10, 10))
                self.surface.blit(text, (10, 700))

                return reward, done

        else:
            reward, done = self.game_step (pos, is_X)
            font = pygame.font.Font(None, 30)

            y_image = pygame.image.load("resources/o.png").convert_alpha()
            scaled_y_image = pygame.transform.smoothscale(y_image, (75, 75))
            self.surface.blit(scaled_y_image, (centerX, centerY))
            self.board[pos - 1] = 'O'

            if reward == 1:
                text = font.render('Player O won!', 1, (10, 10, 10))
                self.surface.blit(text, (10, 680))
            if reward == -5:
                font = pygame.font.Font(None, 30)
                text = font.render('Invalid move!', 1, (10, 10, 10))
                self.surface.blit(text, (10, 700))

                return reward, done
            
        if reward == 0.5:
            font = pygame.font.Font(None, 20)
            text = font.render('Draw Game!', 1, (10, 10, 10))
            self.surface.blit(text, (10, 680))
            return reward, done

        return reward, done
    
    def update_state (self, is_X):
        pos = self.mouse_click ()
        reward, done = self.draw_move (pos, is_X)

        return reward, done
    
    # def start_training (self, player1, player2):
    #     if isinstance (player1, QLearning) and isinstance (player2, QLearning):
    #         self.training = True
    #         self.player1 = player1
    #         self.player2 = player2

    # def train (self, epochs):
    #     if self.training:
    #         for i in range (epochs):
    #             print ('Training: ', i)
    #             self.player1.game_begin ()
    #             self.player2.game_begin ()
    #             self.reset ()
    #             done = False
    #             is_X = random.choice ([True, False])
    #             while not done:
    #                 if is_X:
    #                     move = self.player1.get_action (self.board, self.possible_moves ())
    #                 else:
    #                     move = self.player2.get_action (self.board, self.possible_moves ())
                    
    #                 reward, done = self.game_step (move, is_X)

    #                 if reward == 1:
    #                     if is_X:
    #                         self.player1.update_Q (reward, self.board, self.possible_moves ())
    #                         self.player2.update_Q (-1 * reward, self.board, self.possible_moves ())
    #                     else:
    #                         self.player1.update_Q (-1 * reward, self.board, self.possible_moves ())
    #                         self.player2.update_Q (reward, self.board, self.possible_moves ())
    #                 elif reward == 0.5:
    #                         self.player1.update_Q (reward, self.board, self.possible_moves ())
    #                         self.player2.update_Q (reward, self.board, self.possible_moves ())
    #                 elif reward == -5:
    #                     if is_X:
    #                         self.player1.update_Q (reward, self.board, self.possible_moves ())
    #                     else:
    #                         self.player2.update_Q (reward, self.board, self.possible_moves ())

    #                 elif reward == 0:
    #                     if is_X:
    #                         self.player2.update_Q (reward, self.board, self.possible_moves ())
    #                     else:
    #                         self.player1.update_Q (reward, self.board, self.possible_moves ())
    #                 is_X = not is_X

    # def saveStates(self):
    #     self.player1.saveQtable("player1_states_5vs5")
    #     self.player2.saveQtable("player2_states_5vs5")

    def start_game (self, playerX, playerO):
        # if (isinstance (playerX, Human5vs5)):
        #     self.human, self.computer = True, False
        #     if (isinstance(playerO, QLearning)):
        #         self.ai = playerO
        #         self.ai.loadQtable("player2_states_5vs5")
        #         self.ai.epsilon = 0
        #         self.isAI = True  
                

        # elif (isinstance(playerO, Human5vs5)):
        #     self.humman, self.computer = False, True
        #     if (isinstance(playerX, QLearning)):
        #         self.ai = playerX
        #         self.ai.loadQtable("player1_states_5vs5")
        #         self.ai.epsilon = 0 
        #         self.isAI = True      
        pass

    def run (self):
        running = 1
        done = False

        pygame.event.clear ()

        while running == 1:
            if self.pvp:
                if self.player1_turn:
                    print ('Player 1 turn')
                    event = pygame.event.wait ()
                    while event.type != pygame.MOUSEBUTTONDOWN:
                        event = pygame.event.wait ()
                        self.show_board ()

                        if event.type == pygame.QUIT:
                            running = 0
                            print ("End")
                            break

                    reward, done = self.update_state (self.player1_turn)
                    self.show_board ()
                    if done:
                        time.sleep (1)
                        self.reset ()

                else:
                    print ('Player 2 turn')
                    event = pygame.event.wait ()
                    while event.type != pygame.MOUSEBUTTONDOWN:
                        event = pygame.event.wait ()
                        self.show_board ()

                        if event.type == pygame.QUIT:
                            running = 0
                            print ("End")
                            break

                    reward, done = self.update_state (self.player1_turn)
                    self.show_board ()
                    if done:
                        time.sleep (1)
                        self.reset ()


                self.player1_turn = not self.player1_turn
            # elif self.human_turn:
            #     print ('Human turn')
            #     event = pygame.event.wait ()
            #     while event.type != pygame.MOUSEBUTTONDOWN:
            #         event = pygame.event.wait ()
            #         self.show_board ()

            #         if event.type == pygame.QUIT:
            #             running = 0
            #             print ("End")
            #             break

            #     reward, done = self.update_state (self.human)
            #     self.show_board ()
            #     if done:
            #         time.sleep (1)
            #         self.reset ()
            # else:
            #     if self.isAI:
            #         move = self.ai.get_action (self.board, self.possible_moves ())
            #         reward, done = self.draw_move (move, self.computer)
            #         print ("AI Turn")
            #         self.show_board ()

            #     if done:
            #         time.sleep (1)
            #         self.reset ()
            
            # self.human_turn = not self.human_turn
