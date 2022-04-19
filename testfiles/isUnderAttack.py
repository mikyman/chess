def isUnderAttack(color, sourceSquareRank, sourceSquareLine) -> bool:
  # Prinzip der Funktion:
  # Vom Standpunkt der Feld-Koordinaten werden die möglichen Zugpositionen vom 
  # Bauern/Springer/Läufer/Turm/Damen und König geholt
  # Wenn in solch einem Feld die jeweilige gegnerische Figur stehen könnte => Figur angegriffen => return True; sonst return False
  
  return [sourceSquareRank,sourceSquareLine] in checkLegalMovesV1(OTHER_COLOR[color], True):