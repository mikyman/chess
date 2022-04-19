# def checkLegalMovesPawn(color,isBoardSwitched,onlyDangerFields=False,capturableEnPassant=[])->list:
def checkLegalMovesPawn(color,onlyDangerFields=False,capturableEnPassant=[])->list:
  legalMovesV1 = []
  piece = color + 'p'
  i = 1 if color == 'w' else -1
  piecePosition = getPiecePositions(piece)
  # Liste 'piecePosition' ist leer
  if not piecePosition:
    return legalMovesV1
    
  for position in piecePosition:
    sourceSquareRank, sourceSquareLine = position
    # Wenn onlyDangerFields wahr ist, wird nur nach schlagfähigen Zügen gesucht
    if not onlyDangerFields:
      # Bauernzug vor
      # Wenn Bauer in 2. Reihe und beide Felder davor sind frei => füge Zug hinzu
      if ((sourceSquareRank == 6 and color == 'w') or (sourceSquareRank == 1 and color == 'b')):
        if ((board.iloc[sourceSquareRank-1*i,sourceSquareLine] == "--") and
          (board.iloc[sourceSquareRank-2*i,sourceSquareLine] == "--")):
            legalMovesV1.append([sourceSquareRank-2*i,sourceSquareLine])
      # Wenn Feld davor frei und Bauer steht nicht in der obersten Reihe => füge Zug hinzu
      if 1 <= sourceSquareRank <= 6:
        if board.iloc[sourceSquareRank-1*i,sourceSquareLine] == "--":
          legalMovesV1.append([sourceSquareRank-1*i,sourceSquareLine])
    
    # Schlagzug
    # Wenn Bauer nicht am linken Rand steht 
    # => prüfe Schlagzug nach links (bei ungedrehtem Brett)
    # => prüfe Schlagzug nach rechts (bei gedrehtem Brett)
    if ((1 <= sourceSquareRank <= 6) and (sourceSquareLine > 0)):
      # Wenn links oder rechts oben Figur des Gegners steht => füge Zug hinzu
      if board.iloc[sourceSquareRank-1*i,sourceSquareLine-1].startswith(OTHER_COLOR[color]):
        legalMovesV1.append([sourceSquareRank-1*i,sourceSquareLine-1])
    # Wenn weisser Bauer nicht am rechten Rand steht (oder schwarzer Bauer bei gedrehtem Brett)
    # => prüfe Schlagzug nach rechts
    if ((1 <= sourceSquareRank <= 6) and (sourceSquareLine < 7)):
      # Wenn rechts oben Figur des Gegners steht => füge Zug hinzu
      if board.iloc[sourceSquareRank-1*i,sourceSquareLine+1].startswith(OTHER_COLOR[color]):
        legalMovesV1.append([sourceSquareRank-1*i,sourceSquareLine+1])
    
    # EnPassant
    # Wenn neben mir ein gegnerischer Bauer steht, der gerade einen Doppelschritt gegangen ist
    # => füge Zug hinzu
    # Wenn links neben eigenen Bauer
    if ((sourceSquareRank == 3) and (piece == 'wp') or
        (sourceSquareRank == 4) and (piece == 'bp')):
      if sourceSquareLine > 0:
        if capturableEnPassant == [sourceSquareRank,sourceSquareLine-1]:
          legalMovesV1.append([sourceSquareRank-1*i,sourceSquareLine-1])
      # Wenn rechts neben eigenen Bauer
      if sourceSquareLine < 7:
        if capturableEnPassant == [sourceSquareRank,sourceSquareLine+1]:
          legalMovesV1.append([sourceSquareRank-1*i,sourceSquareLine+1])

  return legalMovesV1