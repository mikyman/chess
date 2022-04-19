def checkLegalMovesKing(color, legalMovesV1) -> list:
  sourceSquareRank, sourceSquareLine = getPiecePositions(color + 'k')
  # Ein König kann max. 8 Felder betreten
  for direction in range(1,9):
    # oben
    if direction == 1:
      stepRank = -1
      stepLine = 0
    # oben rechts
    elif direction == 2:
      stepRank = -1
      stepLine = +1
    # rechts
    elif direction == 3:
      stepRank = 0
      stepLine = +1
    # unten rechts
    elif direction == 4:
      stepRank = +1
      stepLine = +1
    # unten
    elif direction == 5:
      stepRank = +1
      stepLine = 0
    # unten links
    elif direction == 6:
      stepRank = +1
      stepLine = -1
    # links
    elif direction == 7:
      stepRank = 0
      stepLine = -1
    # oben links
    elif direction == 8:
      stepRank = -1
      stepLine = -1

    # Wenn Index außerhalb des Feldes (es werden bis zu 2 Schritte in jede Richtung geprüft) => prüfe nächste Richtung (direction)
    if not ((0 <= sourceSquareRank+stepRank <= 7) and (0 <= sourceSquareLine+stepLine <= 7)):
      continue

    # Wenn eigene Figur im Weg => prüfe nächste Richtung (direction)
    if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(color):
      continue

    # Wenn Gegner im Weg => füge Zug hinzu => prüfe nächste Richtung (direction)
    if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(OTHER_COLOR[color]):
      legalMovesKing.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
      continue

    # Wenn zu prüfendes Feld frei => füge Zug hinzu => prüfe nächste Richtung (direction)
    if board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine] == "--":
      legalMovesKing.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
  return legalMovesKing