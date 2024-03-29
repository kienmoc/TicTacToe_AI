from TicTacToe3vs3 import TicTacToe3vs3
from TicTacToe5vs5 import TicTacToe5vs5
from QLearning import QLearning

game = TicTacToe5vs5 (training=True)
player1 = QLearning ()
player2 = QLearning ()
game.start_training (player1, player2)
game.train (50000)
game.saveStates ()