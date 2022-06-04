from board import Board
from player import Player
from sys import exit


def startGame(board, player: list):
  LONGCOLOR = {"w": "White", "b": "Black"}
  index = 0
  while True:
    # Gibt von jedem aktiven Spieler die Spielerfarbe weiter
    ret = board.setMove(player[index].color)
    if ret == -1:
      exit(f"\n Checkmate! {LONGCOLOR.get(player[index].color)} wins.\n")
    # Setzt den index immer auf 1 oder 0
    index = (index + 1) % 2
    #-Last Edit
    break
  

if __name__ == "__main__":
  # init
  board = Board()
  player = [Player() for _ in range(2)]
  startGame(board, player)