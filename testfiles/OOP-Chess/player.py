class Player():

  id = 0
  def __init__(self):
    Player.id += 1
    self.type = self.setPlayerType(Player.id)
    self.color = self.setPlayerColor(Player.id)
    
  def __del__(self):
    Player.id -= 1
    
  def setPlayerType(self, id):
    while True:
      playerType = input(f"\nPlayer {id}, please choice:\n h for human\n e for engine\n> ").lower()
      if playerType == "h": return "human"
      elif playerType == "e": return "engine"
  
  def setPlayerColor(self, id):
    # id % 2 != 0 -> 'w' else 'b'
    return ('b','w')[id % 2]
