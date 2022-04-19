def getPiecePositions(piece) -> list:
  piecePosition = []
  # Iteration über das Brett. Position der der Figur(en) wird gesucht
  for sourceSquareRank in range(8):
    for sourceSquareLine in range(8):
      # Wenn Figur(en) gefunden
      if board.iloc[sourceSquareRank,sourceSquareLine] == piece:
        # speichere die Position(en) und gebe sie zurück.
        # Ausser es wird der König gesucht,
        # dann wird diese Position direkt zurückgegeben.
        if piece.endswith('k'):
          return [sourceSquareRank,sourceSquareLine]
        piecePosition.append([sourceSquareRank,sourceSquareLine])
  # und gebe sie zurück
  return piecePosition