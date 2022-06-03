from board import Board
from player import Player

# Globals:
# Constances:
DIRECTIONS_ = {
                "RBQK":((-1,0),(+1,0),(0,+1),(0,-1),(-1,+1),(+1,-1),(+1,+1),(-1,-1)),
                "N": ((-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1))
              }

OTHERCOLOR 	= {
                "w":"b",
                "b":"w"
              }


if __name__ == "__main__":
  # init
  b = Board(True)
  player = [Player() for _ in range(2)]
  print(b.printBoard())
  print(b.printBoard())
  print(b.printBoard())
  print(b.printBoard())