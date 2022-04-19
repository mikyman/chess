# def checkLegalMovesV1(color,isBoardSwitched,onlyDangerFields=False,capturableEnPassant=[]) -> list:
def checkLegalMovesV1(color,onlyDangerFields=False,capturableEnPassant=[]) -> list:
  legalMovesV1 = checkLegalMovesPawn(color,onlyDangerFields,capturableEnPassant)
  for p in ['r', 'b', 'q']:
    legalMovesV1 = checkLegalMovesRookBishopQueen(color+p, legalMovesV1)
  legalMovesV1 = checkLegalMovesKnight(color, legalMovesV1)
  legalKingMoves = checkLegalMovesKing(color, legalMovesV1)
  return legalMovesV1