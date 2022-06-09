
class Player():
  id = 0
  def __init__(self):
    Player.id += 1
    self.type = self.setPlayerType(Player.id)
    self.color = self.setPlayerColor(Player.id)
    
  def __del__(self):
    Player.id -= 1
    
  def setPlayerType(self, id) -> str:
    while True:
      print()
      print(f" Player {id}, please choice:")
      print("  h for Human")
      print("  e for Engine")
      playerType = input("> ").lower()
      if playerType == "h": return "human"
      elif playerType == "e": return "engine"
  
  def setPlayerColor(self, id) -> str:
    # id % 2 != 0 -> 'w' else 'b'
    return ("b","w")[id % 2]
