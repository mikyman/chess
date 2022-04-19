def checkLegalMovesKnight(color, legalMovesV1) -> list:
  piecePosition = getPiecePositions(color + 'n')
  if not piecePosition:
    legalMovesV1.append([])
    return legalMovesV1
  
  # Ein Springer kann max. 8 Felder betreten
  for position in piecePosition:
    sourceSquareRank, sourceSquareLine = position
    for direction in range(1,9):
      # Oben oben rechts
      if direction == 1:
        stepRank = -2
        stepLine = +1
      # Oben rechts rechts
      elif direction == 2:
        stepRank = -1
        stepLine = +2
      # Unten rechts rechts
      elif direction == 3:
        stepRank = +1
        stepLine = +2
      # Unten unten rechts
      elif direction == 4:
        stepRank = +2
        stepLine = +1
      # Unten unten links
      elif direction == 5:
        stepRank = +2
        stepLine = -1
      # Unten links links
      elif direction == 6:
        stepRank = +1
        stepLine = -2
      # Oben links links
      elif direction == 7:
        stepRank = -1
        stepLine = -2
      # Oben oben links
      elif direction == 8:
        stepRank = -2
        stepLine = -1

      # Wenn Index außerhalb des Feldes (es wird bis zu 1 Schritt in jede Richtung geprüft) => prüfe nächste Richtung (direction)
      if not ((0 <= sourceSquareRank+stepRank <= 7) and (0 <= sourceSquareLine+stepLine <= 7)):
        continue

      # Wenn eigene Figur auf dem Feld => prüfe nächste Richtung (direction)
      if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(color):
        continue

      # Wenn Gegner auf dem Feld => füge Zug hinzu => prüfe nächste Richtung (direction)
      if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(OTHER_COLOR[color]):
        legalMovesV1.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
        continue

      # Wenn zu prüfendes Feld frei => füge Zug hinzu => prüfe nächste Richtung (direction)
      if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine] == "--":
        legalMovesV1.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
      
  return legalMovesV1