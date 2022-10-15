from abc import ABC, abstractmethod


class Piece(ABC):
  # upper_piece is for white and lower_piece is for black
  # etc. P or p for pawn
  def __init__(self, selfPos: tuple, piece: str):
    self.x, self.y = selfPos
    self.piece = piece        # for piece icons
    self.color = ('b','w')[piece.isupper()]
  
  @abstractmethod
  def getHitMoves(self, board):
    pass

  @abstractmethod
  def getPossibleMoves(self, board):
    pass
  
  # Only for debug
  def get_state(self):
    return (self.x, self.y, self.piece)
    
  def __str__(self):
    return (self.piece)


class Pawn(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)
    self.f = (-1, 1)[self.color=='w']     # f for factor
    self.isStartPosition = True
    self.moves = []

  def getHitMoves(self, board):
    hitMoves = []
    for newPos in ((self.x-(1*self.f), self.y-(1*self.f)), (self.x+(1*self.f), self.y-(1*self.f))):
      if newPos in board:
        if self.color != board.get(newPos).color:
          hitMoves.append(newPos)
    return hitMoves
    
  def getPossibleMoves(self, board):
    self.moves.clear()
    if ((0 < self.y <= 6) and (0 <= self.x <= 7)):
      if (self.x, self.y-(1*self.f)) not in board: # ask here, and not isKingCheck (global)
        self.moves.append((self.x, self.y-(1*self.f)))
        if self.isStartPosition and (self.x, self.y-(2*self.f)) not in board:
          self.moves.append((self.x, self.y-(2*self.f)))
      self.moves.extend(self.getHitMoves(board))
    return self.moves

  def canChange(self):
    if ((self.y == 1) and (self.color == 'w') or 
        (self.y == 6) and (self.color == 'b')):
      return bool(self.moves)
    return False


class Rook(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)

  def getHitMoves(self, board):
    hitMoves = []
    for pos in self.getPossibleMoves(board):
      if ((pos in board) and (self.color != board.get(pos).color)):
        hitMoves.append(pos)
    return hitMoves

  def getPossibleMoves(self, board):
    moves = []
    for f in (-1, 1):
      for i in range(1, 8):
        # move on x-line
        new_x = self.x-(i*f)
        if (0 <= new_x <= 7):
          if (new_x, self.y) not in board:
            moves.append((new_x, self.y))
          else:
            if self.color != board.get((new_x, self.y)).color:
              moves.append((new_x, self.y))
            break
        else:
          break
      for i in range(1, 8):
        # move on y-line
        new_y = self.y-(i*f)
        if (0 <= new_y <= 7):
          if (self.x, new_y) not in board:
            moves.append((self.x, new_y))
          else:
            if self.color != board.get((self.x, new_y)).color:
              moves.append((self.x, new_y))
            break
        else:
          break
    return moves


class Knight(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)

  def getHitMoves(self, board):
    hitMoves = []
    for pos in self.getPossibleMoves(board):
      if ((pos in board) and (self.color != board.get(pos).color)):
        hitMoves.append(pos)
    return hitMoves

  def getPossibleMoves(self, board):
    moves = []
    for pos in ((-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)):
      new_x = self.x + pos[0]
      new_y = self.y + pos[1]
      if ((0 <= new_x <= 7) and (0 <= new_y <= 7)):
        if (new_x, new_y) not in board:
            moves.append((new_x, new_y))
        else:
          if (self.color != board.get((new_x, new_y)).color):
            moves.append((new_x, new_y))
    return moves


class Bishop(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)

  def getHitMoves(self, board):
    hitMoves = []
    for pos in self.getPossibleMoves(board):
      if ((pos in board) and (self.color != board.get(pos).color)):
        hitMoves.append(pos)
    return hitMoves

  def getPossibleMoves(self, board):
    moves = []
    for pos in ((-1,+1),(+1,-1),(+1,+1),(-1,-1)):
      for i in range(1, 8):
        new_x = self.x-(pos[0]*i)
        new_y = self.y-(pos[1]*i)
        if ((0 <= new_x <= 7) and (0 <= new_y <= 7)):
          if (new_x, new_y) not in board:
              moves.append((new_x, new_y))
          else:
            if (self.color != board.get((new_x, new_y)).color):
              moves.append((new_x, new_y))
            break
        else:
          break
    return moves


class Queen(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)

  def getHitMoves(self, board):
    hitMoves = []
    for pos in self.getPossibleMoves(board):
      if ((pos in board) and (self.color != board.get(pos).color)):
        hitMoves.append(pos)
    return hitMoves

  def getPossibleMoves(self, board):
    rook_moves = Rook((self.x, self.y), ('r', 'R')[self.piece.isupper()]).getPossibleMoves(board)
    bishop_moves = Bishop((self.x, self.y), ('b', 'B')[self.piece.isupper()]).getPossibleMoves(board)
    return rook_moves + bishop_moves


class King(Piece):
  def __init__(self, xy_coord, piece):
    super().__init__((xy_coord), piece)

  def getHitMoves(self, board):
    pass

  def getPossibleMoves(self, board):
    pass


class Board():
  def __init__(self):
    self.figure_and_names = list(zip((Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook), 'rnbqkbnr'))
    self.board = self.reset()
    
  def reset(self):
    new_board = dict()
    new_board.update({(i, 0):figure[0]((i, 0), figure[1]) for i, figure in enumerate(self.figure_and_names)})
    new_board.update({(i, 1):Pawn((i, 1), 'p') for i in range(8)})
    new_board.update({(i, 6):Pawn((i, 6), 'P') for i in range(8)})
    new_board.update({(i, 7):figure[0]((i, 7), figure[1].upper())
                      for i, figure in enumerate(self.figure_and_names)})
    return new_board
  
  def setFigure(self, old_xy, new_xy):
    pass
  
  def printBoard(self):
    print('  0 1 2 3 4 5 6 7')
    for y in range(8):
      print(y, end='')
      for x in range(8):
        print(f" {self.board.get((x, y), '-')}", end='')
      print()

  
b = Board()
b.printBoard()
# for k in b.board:
  # print(b.board[k].piece)
  # print(b.board[k].getPossibleMoves(b.board))
# # print(b.board[(1,1)].canChange())
  # print(b.board[k].getHitMoves(b.board))
