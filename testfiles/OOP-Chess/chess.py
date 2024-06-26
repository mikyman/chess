from board import Board
from player import Player
from sys import exit


def startGame(board, player: list):
  index = 0
  while True:
    print()
    board.printBoard()
    # Gibt von jedem aktiven Spieler die Spielerfarbe weiter
    ret = board.setMove(player[index].color)
    if ret == -1:
      exit(f"\n Checkmate! {LONG_COLOR.get(player[index].color)} wins.\n")
    # Setzt den index immer auf 1 oder 0
    index = (index + 1) % 2
    
    #-Last Edit
    if not index:
      break
  

if __name__ == "__main__":
  print('\n --- DEMO ---')
  # init
  LONG_COLOR = {"w": "White", "b": "Black"}
  
  while True:
    board = Board()
    player = [Player() for _ in range(2)]
    startGame(board, player)
    
    # if play again
    if player:
      player.clear()
    break
