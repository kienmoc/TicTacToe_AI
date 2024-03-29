import pygame
import random
import time
from QLearning import QLearning

class Human3vs3:
    pass

class TicTacToe3vs3:

    def __init__ (self, training=False, pvp=False):
        self.board = [' '] * 9
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
            self.board = [" "] * 9
            return
        
        self.board = [" "] * 9
        if self.pvp:
            self.player1_turn = random.choice ([True, False])

            self.surface = pygame.Surface (self.ttt.get_size ())
            self.surface = self.surface.convert ()

            self.surface.fill ((250, 250, 250))

            pygame.draw.line (self.surface, (0, 0, 0), (240, 0), (240, 720), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (480, 0), (480, 720), 3)
            
            pygame.draw.line (self.surface, (0, 0, 0), (0, 240), (720, 240), 3)
            pygame.draw.line (self.surface, (0, 0, 0), (0, 480), (720, 480), 3)

            return
        
        self.human_turn = random.choice ([True, False])
        
        self.surface = pygame.Surface (self.ttt.get_size ())
        self.surface = self.surface.convert ()

        self.surface.fill ((250, 250, 250))

        pygame.draw.line (self.surface, (0, 0, 0), (240, 0), (240, 720), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (480, 0), (480, 720), 3)
        
        pygame.draw.line (self.surface, (0, 0, 0), (0, 240), (720, 240), 3)
        pygame.draw.line (self.surface, (0, 0, 0), (0, 480), (720, 480), 3)


    def show_board(self):
        self.ttt.blit(self.surface, (0, 0))
        pygame.display.flip()

    def mouse_click (self):
        (mouseX, mouseY) = pygame.mouse.get_pos ()

        if mouseX < 240:
            col = 0
        elif mouseX < 480:
            col = 1
        else:
            col = 2

        if mouseY < 240:
            row = 0
        elif mouseY < 480:
            row = 1
        else:
            row = 2

        return row * 3 + col + 1
    
    def is_win (self, ch):
        for i in range (3):
            if ch == self.board[i * 3] == self.board[i * 3 + 1] and self.board[i * 3 + 1] == self.board[i * 3 + 2]:
                return 1.0, True
        
        for i in range (3):
            if ch == self.board[i] == self.board[i + 3] and self.board[i + 3] == self.board[i + 6]:
                return 1.0, True
            
        if ch == self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            return 1.0, True
        
        if ch == self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            return 1.0, True
        
        if not any (c == ' ' for c in self.board):
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
        row = int ((pos - 1) / 3)
        col = (pos - 1) % 3

        centerX = ((col) * 240) + 45
        centerY = ((row) * 240) + 45

        if (is_X):
            reward, done = self.game_step (pos, is_X)
            font = pygame.font.Font(None, 40)
            x_image = pygame.image.load("resources/x.png").convert_alpha()
            scaled_x_image = pygame.transform.smoothscale(x_image, (150, 150))
            self.surface.blit(scaled_x_image, (centerX, centerY))
            self.board[pos - 1] = 'X'

            if reward == 1: 
                text = font.render('Player X won!', 1, (10, 10, 10))
                self.surface.blit(text, (20, 680))

            if reward == -5:
                font = pygame.font.Font(None, 40)
                text = font.render('Invalid move!', 1, (10, 10, 10))
                self.surface.blit(text, (40, 700))

                return reward, done

        else:
            reward, done = self.game_step (pos, is_X)
            font = pygame.font.Font(None, 40)

            y_image = pygame.image.load("resources/o.png").convert_alpha()
            scaled_y_image = pygame.transform.smoothscale(y_image, (150, 150))
            self.surface.blit(scaled_y_image, (centerX, centerY))
            self.board[pos - 1] = 'O'

            if reward == 1:
                text = font.render('Player O won!', 1, (10, 10, 10))
                self.surface.blit(text, (20, 680))
            if reward == -5:
                font = pygame.font.Font(None, 40)
                text = font.render('Invalid move!', 1, (10, 10, 10))
                self.surface.blit(text, (40, 700))

                return reward, done
            
        if reward == 0.5:
            font = pygame.font.Font(None, 40)
            text = font.render('Draw Game!', 1, (10, 10, 10))
            self.surface.blit(text, (20, 680))
            return reward, done

        return reward, done
    
    def update_state (self, is_X):
        pos = self.mouse_click ()
        reward, done = self.draw_move (pos, is_X)

        return reward, done
    
    def start_training (self, player1, player2):
        if isinstance (player1, QLearning) and isinstance (player2, QLearning):
            self.training = True
            self.player1 = player1
            self.player2 = player2

    def train (self, epochs):
        if self.training:
            for i in range (epochs):
                print ('Training: ', i)
                self.player1.game_begin ()
                self.player2.game_begin ()
                self.reset ()
                done = False
                is_X = random.choice ([True, False])
                while not done:
                    if is_X:
                        move = self.player1.get_action (self.board, self.possible_moves ())
                    else:
                        move = self.player2.get_action (self.board, self.possible_moves ())
                    
                    reward, done = self.game_step (move, is_X)

                    if reward == 1:
                        if is_X:
                            self.player1.update_Q (reward, self.board, self.possible_moves ())
                            self.player2.update_Q (-1 * reward, self.board, self.possible_moves ())
                        else:
                            self.player1.update_Q (-1 * reward, self.board, self.possible_moves ())
                            self.player2.update_Q (reward, self.board, self.possible_moves ())
                    elif reward == 0.5:
                            self.player1.update_Q (reward, self.board, self.possible_moves ())
                            self.player2.update_Q (reward, self.board, self.possible_moves ())
                    elif reward == -5:
                        if is_X:
                            self.player1.update_Q (reward, self.board, self.possible_moves ())
                        else:
                            self.player2.update_Q (reward, self.board, self.possible_moves ())

                    elif reward == 0:
                        if is_X:
                            self.player2.update_Q (reward, self.board, self.possible_moves ())
                        else:
                            self.player1.update_Q (reward, self.board, self.possible_moves ())
                    is_X = not is_X

    def saveStates(self):
        self.player1.saveQtable("player1_states_3vs3")
        self.player2.saveQtable("player2_states_3vs3")

    def start_game (self, playerX, playerO):
        if (isinstance (playerX, Human3vs3)):
            self.human, self.computer = True, False
            if (isinstance(playerO, QLearning)):
                self.ai = playerO
                self.ai.loadQtable("player2_states_3vs3")
                self.ai.epsilon = 0
                self.isAI = True  
                

        elif (isinstance(playerO, Human3vs3)):
            self.humman, self.computer = False, True
            if (isinstance(playerX, QLearning)):
                self.ai = playerX
                self.ai.loadQtable("player1_states_3vs3")
                self.ai.epsilon = 0 
                self.isAI = True       

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
            elif self.human_turn:
                print ('Human turn')
                event = pygame.event.wait ()
                while event.type != pygame.MOUSEBUTTONDOWN:
                    event = pygame.event.wait ()
                    self.show_board ()

                    if event.type == pygame.QUIT:
                        running = 0
                        print ("End")
                        break

                reward, done = self.update_state (self.human)
                self.show_board ()
                if done:
                    time.sleep (1)
                    self.reset ()
            else:
                if self.isAI:
                    move = self.ai.get_action (self.board, self.possible_moves ())
                    reward, done = self.draw_move (move, self.computer)
                    print ("AI Turn")
                    self.show_board ()

                if done:
                    time.sleep (1)
                    self.reset ()
            
            self.human_turn = not self.human_turn
