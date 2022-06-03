from pandas import DataFrame as df

class Board():
  
  def __init__(self, boardSwitch = False):
    self.board = self.createBoard()
    self.numbers = (" 8"," 7"," 6"," 5"," 4"," 3"," 2"," 1")
    self.letters = (" a"," b"," c"," d"," e"," f"," g"," h")
    self.boardSwitch = boardSwitch


  def createBoard(self):
    board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"],
    ]
    return board


  def switchBoard(self) -> None:
    self.numbers = tuple(reversed(self.numbers))
    self.letters = tuple(reversed(self.letters))
    for y in range(4):
      for x in range(8):
        self.board[y][x], self.board[7-y][7-x] = self.board[7-y][7-x], self.board[y][x]

    
  def printBoard(self) -> None:
    print(df(self.board, index=self.numbers, columns=self.letters))
    if self.boardSwitch:
      self.switchBoard()

