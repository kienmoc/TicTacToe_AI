from TicTacToe3vs3 import TicTacToe3vs3, Human3vs3
from QLearning import QLearning
from TicTacToe5vs5 import TicTacToe5vs5, Human5vs5

game = TicTacToe5vs5 (pvp=True)
player1 = Human5vs5 ()
player2 = Human5vs5 ()

game.start_game (player1, player2)
game.reset ()
game.run ()