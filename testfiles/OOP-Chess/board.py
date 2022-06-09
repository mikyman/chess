from pandas import DataFrame

# Globals:
# Constances:
DIRECTIONS = {
              "RBQK":((-1,0),(+1,0),(0,+1),(0,-1),(-1,+1),(+1,+1),(+1,-1),(-1,-1)),
              "N": ((-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1))
             }

OTHER_COLOR = {
                "w":"b",
                "b":"w"
              }


class Board():

  def __init__(self, boardSwitch = False):
    self.board = self.createBoard()
    self.numbers = (" 8"," 7"," 6"," 5"," 4"," 3"," 2"," 1")
    self.letters = (" a"," b"," c"," d"," e"," f"," g"," h")
    self.boardSwitch = boardSwitch
    self.kingPositions = self.__getKingsPos()

  def createBoard(self):
    board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["wp","wp","wp","wp","wp","bp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"],
    ]
    return board

  def __switchBoard(self) -> None:
    self.numbers = tuple(reversed(self.numbers))
    self.letters = tuple(reversed(self.letters))
    for y in range(4):
      for x in range(8):
        self.board[y][x], self.board[7-y][7-x] = self.board[7-y][7-x], self.board[y][x]

  def __getKingsPos(self) -> dict:
    kingPos = {}
    # Iteration über das Brett.
    # Wenn König gefunden
    # => füge als dictionary {'wk': (y, x), 'bk': (y, x)} hinzu
    for y in range(8):
      for x in range(8):
        if self.board[y][x] in ("wk", "bk"):
          kingPos[self.board[y][x]] = (y, x)
    return kingPos

  def printBoard(self) -> None:
    print(DataFrame(self.board, index=self.numbers, columns=self.letters))
    if self.boardSwitch:
      self.__switchBoard()

  def attackedByOpponent(self, dangerFields, piece) -> bool:
    for df in dangerFields:
      if self.board[df[0]][df[1]] == OTHER_COLOR[piece[0]] + piece[1]:
        return True
    return False

  # ====================================================================================================
  # Filtere legale Zugmöglichkeiten
  # ====================================================================================================

  def checkLegalMovesPawns(self, piece: str, legalMovesV1: list, y: int, x: int,
                            capturableEnPassant: list) -> list:

    # Für Position: ggü-liegende Reihen/Linien von Schwarz und Weiß ergeben 7
    summand = (0,7)[piece.startswith("b")]

    # Für Zug: (Schlag)Richtung der Bauern von schwarz und weiß
    # haben umgekehrte Vorzeichen
    factor = (1,-1)[piece.startswith("b")] 

    # Wenn Bauer in 2./7. Reihe und beide Felder davor frei => füge Zug hinzu
    if y == abs(6 - summand) and board[y-1*factor][x] == "--" and board[y-2*factor][x] == "--":  
      legalMovesV1.append([y-2 * factor, x])

    # Wenn Bauer in 5./4. Reihe und links/rechts ein gegn. Bauer steht,
    # der gerade einen Doppelschritt gegangen ist, => füge Zug hinzu
    elif y == abs(3 - summand) and x != abs(0 - summand) and capturableEnPassant == [(y, x-1*factor)]:
      legalMovesV1.append([y-1*factor, x-1*factor])
    elif y == abs(3 - summand) and x != abs(7 - summand) and capturableEnPassant == [(y, x+1*factor)]:
      legalMovesV1.append([y-1*factor, x+1*factor])

    # Immer und unabhängig von Reihe:
    # Feld davor frei? Schlagzug nach links/rechts möglich? => füge Zug hinzu
    if board[y-1*factor][x] == "--":
      legalMovesV1.append([y-1*factor, x])
    if x != abs(0 - summand) and board[y-1*factor, x-1*factor].startswith(OTHERCOLOR[piece[0]]):
      legalMovesV1.append([y-1*factor, x-1*factor])
    if x != abs(7-summand) and board[y-1*factor, x+1*factor].startswith(OTHERCOLOR[piece[0]]):
      legalMovesV1.append([y-1*factor, x+1*factor])
    return legalMovesV1
  
  def checkLegalMovesV1(self, piece, legalMovesV1, y, x, capturableEnPassant) -> list:
    if piece[1] == "p":
      return self.checkLegalMovesPawns(piece, legalMovesV1, y, x, capturableEnPassant)
    return self.checkLegalMovesPieces(piece, legalMovesV1, y, x)

  def checkLegalMovesV2(color,piece,legalMovesV1,legalMovesV2,sourceRank,sourceLine) -> list:
    backRank = (0,7)[color == "w"] # (Grund)reihe in Abhängigkeit von Farbe (schwarz/weiß)

    # "checkCastleMovesV2" || Prüfung, ob Rochadezug vorliegt und ob diese durchgeführt werden kann (König darf nicht ins Schach)
    for move in legalMovesV1.copy():
      summand07 = (7,0)[move in [[backRank,6],[backRank,7]]] # (Grund)reihe in Abhängigkeit von Rochade (kurz/lang)
      summand08 = (8,0)[move in [[backRank,6],[backRank,7]]] # Linie in Abhängigkeit von Rochade (kurz/lang)
      # Beide Rochadezüge (Zielfeld = Königsfeld/Turmfeld) prüfen | Zwischenschritt + Zielfeld dürfen nicht bedroht sein
      if piece.endswith("k") and board.iloc[backRank,abs(4-summand08)] == color+"k" and move in [[backRank,abs(6-summand08)],[backRank,abs(7-summand07)]]:
        # 1. Königsschritt gehen (Zwischenschritt)
        board.iloc[backRank,abs(4-summand08)] = "--"
        board.iloc[backRank,abs(5-summand08)] = color+"k"     
        if isKingInCheck(color): # Wenn König im Schach => Rochadezug entfernen + Ausgangsstellung wiederherstellen + nächster Zug
          legalMovesV1.remove(move)
          board.iloc[backRank,abs(5-summand08)] = "--"
          board.iloc[backRank,abs(4-summand08)] = color+"k"
          continue      
        else: # Wenn König nach 1. Königsschritt nicht im Schach => 2. Königsschritt gehen (Zielfeld)
          board.iloc[backRank,abs(5-summand08)] = "--"
          board.iloc[backRank,abs(6-summand08)] = color+"k"       
          if isKingInCheck(color): # Wenn König im Schach => Rochadezug entfernen + Ausgangsstellung wiederherstellen + nächster Zug
            legalMovesV1.remove(move)
            board.iloc[backRank,abs(6-summand08)] = "--"
            board.iloc[backRank,abs(4-summand08)] = color+"k"
            continue        
          else: # Wenn König auch nach 2. Königsschritt nicht im Schach =>  Ausgangsstellung wiederherstellen
            board.iloc[backRank,abs(6-summand08)] = "--"
            board.iloc[backRank,abs(4-summand08)] = color+"k"
            # Turm darf als Zielfeld gewählt werden, auch wenn es bedroht ist | ohne continue wäre remove im Anschluss, da Turmfeld im Schach
            if move == [backRank,abs(7-summand07)]: continue

      enterSquare = board.iloc[move[0],move[1]]   # Inhalt von Zielfeld zwischenspeichern, um move später zu resetten 
      board.iloc[sourceRank,sourceLine] = "--"  # Zug ausführen (Quellfeld = "--" ...
      board.iloc[move[0],move[1]] = piece     # ... und Zielfeld = die gewählte Figur)

      # Wenn mein König nach dem getesteten legalMove im Schach steht, wird dieser Zug entfernt
      if isKingInCheck(color):
        legalMovesV1.remove(move)

      board.iloc[move[0],move[1]] = enterSquare # Nach Prüfung Zug zurück (Zielfeld = Figur, die vorher da stand ...
      board.iloc[sourceRank,sourceLine] = piece # ... und Quellfeld = die gewählte Figur)

    for lmv1 in legalMovesV1:
      legalMovesV2.append(lmv1)
    return legalMovesV2

  def checkLegalMovesPieces(self, piece: str, legalMovesV1: list, y: int, x: int) -> list:
    # Springer hat andere Richtungen als der Rest der Figuren
    piece_key = ("RBQK", "N")[piece[1].upper() == "N"]  # EDIT!
    directions = DIRECTIONS.get(piece_key)

    for direction in directions:
      for step in range(1,8):
        # Bei Läufer müssen die geraden
        # und bei Turm die diagonalen Züge ausgeschlossen werden
        if ((piece[1] != ("b") and direction in directions[:4]) or
            (piece[1] != ("r") and direction in directions[4:])
           ):
          newY = y + (step * direction[0])
          newX = x + (step * direction[1])

          # Index außerhalb => nächste Richtung
          if ((0 <= newY <= 7) and (0 <= newX <= 7)):

            # Feld frei => Zug hinzu + nächster Schritt
            if self.board[newY][newX] == "--":
              legalMovesV1.append((newY, newX))

              # König/Springer kann nur einen Schritt gehen,
              # daher nächste Richtung
              if piece[1] not in ("n", "k"):
                continue

            # Gegner im Weg => Zug hinzufügen + nächste Richtung
            elif self.board[newY][newX].startswith(OTHER_COLOR[piece[0]]):
              legalMovesV1.append((newY, newX))

            # In jeden anderen Fall ausser dem 1. => nächste Richtung
            break
          else: break

        # Richtung passt nicht zur Figur => nächste Richtung
        else: break
    return legalMovesV1

  def isUnderAttack(self, color, y, x) -> bool:
    piece       = color + "p" # Bauer
    factor      = (1, -1)[color == "b"]
    dangerFields = []

    # wenn Feld links oben bzw. rechts oben innerhalb Brett
    # => Feld speichern und später prüfen, ob da gegn. Bauer steht
    if (0 <= y-1 * factor <= 7):
      if (0 <= x-1 <= 7):
        dangerFields.append((y-1 * factor, x-1))
      if (0 <= x+1 <= 7):
        dangerFields.append((y-1 * factor, x+1))
      if self.attackedByOpponent(dangerFields, piece): return True

    # Vom Standpunkt des Königs werden Bauern/Springer/Läufer/Turm/Damen/Königszüge gegangen (dangerFields)
    # Wenn in solch einem Feld die jeweilige gegnerische Figur steht => König angegriffen => return True; sonst return False
    dangerFields.clear()
    for shortcut in ["r","b","q","n","k"]:  # Turm / Läufer / Dame / Springer / König
      piece = color + shortcut
      dangerFields = self.checkLegalMovesPieces(piece, dangerFields, y, x)
      if dangerFields:
        if self.attackedByOpponent(dangerFields, piece): return True
        dangerFields.clear()
    return False

  def isKingInCheck(self, color: str) -> bool:
    # prüfe, ob König von (color) im Schach steht (return True/False)
    y, x = self.kingPositions.get(color + "k")
    return self.isUnderAttack(color, y, x)

  def setMove(self, playerColor):
    # legalMoves = getLegalMoves(playerColor)  # -> list
    legalMoves = [(6, 6)]


    # König im Schach...
    if self.isKingInCheck(playerColor):
      # und hat keine güldigen Züge mehr
      if not legalMoves:
        return -1
      else:
        print(" Check")
        pass
    else:
      print("Ich bin Frei!!")
    
