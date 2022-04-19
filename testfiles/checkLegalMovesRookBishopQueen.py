def checkLegalMovesRookBishopQueen(piece,legalMovesV1) -> list:
  piecePosition = getPiecePositions(piece)
  if not piecePosition:
    legalMovesV1.append([])
    return legalMovesV1
  
  for position in piecePosition:
    sourceSquareRank, sourceSquareLine = position
    # Turm und Läufer haben max. 4, Dame max. 8 Richtungen. Alle können maximal 7 Schritte gehen
    for direction in range(1,9):
      # Default-Werte von 10 sorgen später für Abbruch der step-Loop,
      # wenn kein legaler Schritt (von 1-7) gefunden wird
      # Wenn z.B. bei Turm die directions 5-8 oder bei Läufer die directions 1-4 dran sind,
      # soll break folgen
      if (piece.endswith("r") and direction > 4):
        break
      elif (piece.endswith("b") and direction < 5):
        continue
      else:
        for step in range(1,8):        
          # Turm oder Dame
          if (piece.endswith("r") or piece.endswith("q")):
            # Je nach Richtung werden die Indizes definiert
            # 1 = vorne, 2 = hinten, 3 = rechts, 4 = links
            if direction == 1:
              stepRank = step * -1
              stepLine = 0
            elif direction == 2:
              stepRank = step * +1
              stepLine = 0
            elif direction == 3:
              stepRank = 0
              stepLine = step * +1
            elif direction == 4:
              stepRank = 0
              stepLine = step * -1
            
          # Läufer oder Dame
          elif (piece.endswith("b") or piece.endswith("q")):
            # Je nach Richtung werden die Indizes definiert
            # 5 = vorne rechts, 6 = hinten links, 7 = hinten rechts, 8 = vorne links
            if direction == 5:
              stepRank = step * -1
              stepLine = step * +1
            elif direction == 6:
              stepRank = step * +1
              stepLine = step * -1
            elif direction == 7:
              stepRank = step * +1
              stepLine = step * +1
            elif direction == 8:
              stepRank = step * -1
              stepLine = step * -1
            

          # Wenn Index außerhalb des Feldes (es werden bis zu 7 Schritte in jede Richtung geprüft) => prüfe nächste Richtung (direction)
          if not ((0 <= sourceSquareRank+stepRank <= 7) and (0 <= sourceSquareLine+stepLine <= 7)):
            break

          # Wenn eigene Figur im Weg => prüfe nächste Richtung (direction)
          elif board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(piece[0]):
            break

          # Wenn Gegner im Weg => füge Zug hinzu => prüfe nächste Richtung (direction)
          elif board.iloc[sourceSquareRank+stepRank,sourceSquareLine+stepLine].startswith(OTHER_COLOR[piece[0]]):
            legalMovesV1.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
            break

          # Wenn zu prüfendes Feld frei => füge Zug hinzu => prüfe nächstes Feld (step)
          else:
            legalMovesV1.append([sourceSquareRank+stepRank,sourceSquareLine+stepLine])
            
  return legalMovesV1