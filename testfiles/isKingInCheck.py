def isKingInCheck(color) -> bool:
  # Feld mit eigenem König wird gesucht
  sourceSquareRank, sourceSquareLine = getPiecePositions(color + "k")
  # prüft, ob Feld mit eigenem König im Schach steht (True = im Schach sonst nicht im Schach)
  return isUnderAttack(color, sourceSquareRank, sourceSquareLine)