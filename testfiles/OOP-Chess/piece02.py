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
  
  def canHitKing(self, testPos, board):
    for x, y in ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)):
      new_x = self.x-x
      new_y = self.y-y
      if ((0 <= new_x <= 7) and (0 <= new_y <= 7)):
        if ((new_x, new_y) == testPos):
          return True
    return False

  def getHitMoves(self, board):
    pass

  def getPossibleMoves(self, board):
    moves = []
    for x, y in ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)):
      new_x = self.x-x
      new_y = self.y-y
      pos = (new_x, new_y)
      if ((0 <= new_x <= 7) and (0 <= new_y <= 7)):
        if ((pos not in board) or (self.color != board.get(pos).color)):
          if not Board().isDangerousField(pos, self.piece, board):
            moves.append(pos)
    return moves
    


class Board():
  def __init__(self, testMode=False):
    if testMode:
      self.board = dict()
      self.figure = {'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King, 'p': Pawn}
    else:
      self.figure_and_names = list(zip((Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook), 'rnbqkbnr'))
      self.board = self.reset()
    self.kingPositions = self.getKingPos()
    
  def reset(self):
    new_board = dict()
    new_board.update({(i, 0):figure[0]((i, 0), figure[1]) for i, figure in enumerate(self.figure_and_names)})
    new_board.update({(i, 1):Pawn((i, 1), 'p') for i in range(8)})
    new_board.update({(i, 6):Pawn((i, 6), 'P') for i in range(8)})
    new_board.update({(i, 7):figure[0]((i, 7), figure[1].upper())
                      for i, figure in enumerate(self.figure_and_names)})
    return new_board
  
  def getKingPos(self):
    if (self.board.get((4,7)) and self.board.get((4,0))):
      return {'K': (4,7), 'k': (4,0)}
    return {self.board.get(pos).piece: pos for pos in self.board if self.board.get(pos) in ('Kk')}        
  
  def setNewFigure(self, pos_xy:tuple, piece:str):
    if ((0 <= pos_xy[0] <= 7) and (0 <= pos_xy[1] <= 7)):
      # for input-error
      if piece.lower()[0] in ('rnbqkp'):
        figure = self.figure.get(piece.lower()[0])
        self.board.update({pos_xy:figure(pos_xy, piece[0])})
        if piece[0] in 'Kk':
          self.kingPositions.update({piece[0]: pos_xy})
  
  def moveFigure(self, old_xy, new_xy):
    pass
  
  @staticmethod
  def isDangerousField(pos_xy: tuple, piece, board) -> bool:
    # get Knight's positions and checked, can attack my position
    if ((0 <= pos_xy[0] <= 7) and (0 <= pos_xy[1] <= 7)):
      knight_moves = Knight(pos_xy, ('n', 'N')[piece.isupper()]).getHitMoves(board)
      for pos in knight_moves:
        # this piece is figure.piece
        if board.get(pos).piece in ('nN'):
          return True
      # get all positions at the Queen and checked, can any piece in this radius, attack my position
      queen_moves = Queen(pos_xy, ('q', 'Q')[piece.isupper()]).getHitMoves(board)
      for pos in queen_moves:
        # input(pos)
        if board.get(pos).piece in ('Kk'):
          if board.get(pos).canHitKing(pos_xy, board):
            return True
          continue
        elif pos_xy in board.get(pos).getPossibleMoves(board):
          return True
      return False
    else:
      raise Exception('X-Coordinate or Y-Coordinate are outside the boardsize.')

  def printBoard(self):
    print('  0 1 2 3 4 5 6 7')
    for y in range(8):
      print(y, end='')
      for x in range(8):
        print(f" {self.board.get((x, y), '-')}", end='')
      print()

# TODO:
# + add FEN
# + add isCheckmate()
# + add makeMoves()
# + add rochade()
# + Tranform to pygame
# EDIT:
# isDangerousField renamed to getDangerousFields
# getDangerousFields became a list of posible moves
# get a list of all dangerous fields and test the list as a set


if __name__ == '__main__':
  b = Board(True)
  b.setNewFigure((4,4), 'K')
  for fig in ('k'):
    b.setNewFigure((4,2), fig)
    b.printBoard()
    # for k in b.board:
      # print(b.board[k].piece)
      # print(b.board[k].getPossibleMoves(b.board))
    # # print(b.board[(1,1)].canChange())
      # print(b.board[k].getHitMoves(b.board))
    print(b.board.get((4,4)).getPossibleMoves(b.board))
