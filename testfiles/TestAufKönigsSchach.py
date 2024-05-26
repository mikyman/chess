import itertools
import copy

# __VERSION = 0.9

# Alle Koordiinaten sind nach Y,X Schemata angeordnet.
# NamensKürzel der Figuren auf dem Brett:
# R = Turm, B = Läufer, N = Springer, Q = Königin, K = König, P = Bauern.
FIGUREN_RICHTUNG = {
                    "R":[(0,1),(1,0),(0,-1),(-1,0)],
                    "B":[(-1,1),(1,1),(1,-1),(-1,-1)],
                    "N":[(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)],
                    "Q":[(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)],
                    "K":[(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
                  }
BAUERN_RICHTUNG = { # (vor, rechts, links)
                    "w":[(-1,0),(-1,1),(-1,-1)],
                    "b":[(1,0),(1,1),(1,-1)],
                  }
MAXIMALE_BEWEGUNG = {
                      "R":7,
                      "B":7,
                      "N":1,
                      "Q":7,
                      "K":1
                    }

class Brett():
  
  @classmethod
  def init(cls, standard=True):
    '''
      Diese Funktion muss als erstes aufgerufen werden,
      um alle membervariablen zu initiallisieren.
      Wenn das 'standard'-keyword 'True' ist,
      wird die normale Figuren-Aufstellung auf dem Brett erstellt.
      Bei 'False' wird dagegen ein leeres Brett erstellt.
    '''
    cls.__KOORDS = set([(y,x) for y in range(8) for x in range(8)])
    if standard:
      cls.pos_koenig = [(7,4),(0,4)] # [(weiss Y,weiss X), (schwarz Y, schwarz X)]
      cls.__felder = [
                    ['br','bn','bb','bq','bk','bb','bn','br'],
                    ('bp '*8).split(),
                    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                    ('WP '*8).split(),
                    ['WR','WN','WB','WQ','WK','WB','WN','WR'],
                    # ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                    ]
    else:
      cls.pos_koenig = [(),()]
      cls.__felder = [["  "]*8 for _ in range(8)]
  
  @classmethod
  def ist_gueldig(cls, koord: tuple) -> bool:
    # return (0 <= koord[0] <= 7 and 0 <= koord[1] <= 7)
    return koord in cls.__KOORDS
  
  @classmethod
  def update(cls):
    pass
  
  @staticmethod
  def erstelle_brett(brett):
    TRENN_LINIE = "----" * 8
    new_brett = []
    for i in range(16):
      if i%2==0:
        new_brett.append(TRENN_LINIE)
      else:
        new_brett.append("".join([
                              (f"|{feld}|","|  |")["  " == feld]
                              for feld in brett[i//2]
                              ])
                            )
    new_brett.append(TRENN_LINIE)
    return new_brett

  @staticmethod
  def print_brett(brett):
    for zeile in Brett.erstelle_brett(brett):
      print(zeile)
  
  @classmethod
  def hole_figur_farbe(cls, farbe: str) -> str:
    return ('b','W')[farbe[0] in ('W','w')]

  @classmethod
  def iter_figuren_positionen(cls, farbe: str) -> tuple:
    farbe = Brett.hole_figur_farbe(farbe)
    for y, x in itertools.product(range(8), repeat=2):
      if (cls.__felder[y][x][0] == farbe):
        yield [farbe, cls.__felder[y][x][1], y, x]
  
  @classmethod
  def bauern_zug(cls, farbe: str, y_pos: int, x_pos: int, vom_gegner: bool) -> set:
    gueltige_positionen = list()
    richtungen = BAUERN_RICHTUNG.get(farbe.lower(), cls.hole_figur_farbe(farbe))
    for i, richtung in enumerate(richtungen):
      delda_y = y_pos+richtung[0]
      delda_x = x_pos+richtung[1]
      if not cls.ist_gueldig( (delda_y, delda_x) ):
        continue
      ist_frei = cls.__felder[delda_y][delda_x][0] == ' '
      ist_team = cls.__felder[delda_y][delda_x][0] == farbe
      if (i != 0):
        if (vom_gegner) :
          gueltige_positionen.append( (delda_y, delda_x) )
        else: # schlagen im eigenen Zug
          if not (ist_frei or ist_team):
            gueltige_positionen.append( (delda_y, delda_x) )
      # vorgehen
      elif not (vom_gegner):
        delda_y2 = 2*delda_y
        if (ist_frei):
          gueltige_positionen.append( (delda_y, delda_x) )
          if (y_pos in (1, 6)):
            if (cls.__felder[delda_y2][delda_x][0] == ' '):
              gueltige_positionen.append( (delda_y2, delda_x) )
    return set(gueltige_positionen)
  
  @classmethod
  def hole_güldige_züge(cls, farbe: str, vom_gegner: bool) -> set[tuple]:
    zuege = []
    for farbe, figur, y_pos, x_pos in cls.iter_figuren_positionen(farbe):
      figur = figur.upper()
      if figur == 'P':
        zuege.extend(cls.bauern_zug(farbe, y_pos, x_pos, vom_gegner))
        continue
      for posYX in FIGUREN_RICHTUNG.get(figur, []):
        for bewegung in range(1, MAXIMALE_BEWEGUNG[figur]+1):
          delda_y = y_pos+(posYX[0]*bewegung)
          delda_x = x_pos+(posYX[1]*bewegung)
          if not cls.ist_gueldig( (delda_y, delda_x) ):
            break
          else:
            # Steht auf der aktuellen Position das eigene Team: abruch
            # if not vom_gegner:
            if (not vom_gegner):
              if (cls.__felder[delda_y][delda_x][0] == farbe): break
            # ... Wenn nicht, Zug merken und weiter gehen            
            zuege.append((delda_y,delda_x))
            # Wurde beim weitergehen eine gegnerische Figur geschlagen:
            # abruch
            if (cls.__felder[delda_y][delda_x][0].isalpha()): break
    return set(zuege)
    # return zuege
  
  @classmethod
  def hole_brett_kopie(cls):
    return copy.deepcopy(cls.__felder)
  
  @classmethod
  def zeige_güldige_Züge(cls, pos_yx):
    y,x = pos_yx
    # Wenn kein leeres Feld gewählt, dann...
    if ("  " == cls.__felder[y][x]):
      return cls.__felder
    brett_kopie = cls.hole_brett_kopie()
    figur = brett_kopie[y][x][1].upper()
    # Todo: Bauern-Züge einbinden!
    for pos in FIGUREN_RICHTUNG.get(figur,[(1,0)]):
      for bewegung in range(1, MAXIMALE_BEWEGUNG[figur]+1):
        y2, x2 = pos
        if not cls.ist_gueldig( (y2*bewegung+y, x2*bewegung+x) ):
          break
        delda_y = y+(y2*bewegung)
        delda_x = x+(x2*bewegung)
        if not ("  " == brett_kopie[delda_y][delda_x]):
          break
        brett_kopie[delda_y][delda_x] = "**"
    return brett_kopie

  @classmethod
  def hole_koenigPos(cls, farbe: chr) -> tuple:
    if farbe[0] in ('W','b','s'):
      return cls.pos_koenig[farbe != 'W']
    return ()
  
  @staticmethod
  def _ist_schach(pos_koenig: tuple, gegner_zuege: set) -> bool:
    return pos_koenig in gegner_zuege
  
  @classmethod
  def _ist_matt(cls, pos_koenig: tuple, gegner_zuege: set, farbe: chr) -> bool:
    y,x = pos_koenig
    for richtung in FIGUREN_RICHTUNG.get('K'):
      delda_y, delda_x = y+richtung[0], x+richtung[1]
      if cls.ist_gueldig((delda_y, delda_x)):
        pos_in_gegner_zuege = (delda_y, delda_x) in gegner_zuege
        kein_verbuendeter = cls.__felder[delda_y][delda_x][0] != farbe
        print((delda_y, delda_x), (not pos_in_gegner_zuege) and (kein_verbuendeter))
        if ((not pos_in_gegner_zuege) and (kein_verbuendeter)):
          return False
    return True
  
  @classmethod
  def ist_schach_oder_matt(cls, farbe: chr)-> int:
    pos_koenig = cls.hole_koenigPos(farbe)
    if pos_koenig:  # Brett ist nicht 'standard'
      gegner_farbe = ('W','b')[farbe == 'W']
      status = 0
      zuege = cls.hole_güldige_züge(gegner_farbe, True)
      if Brett._ist_schach(pos_koenig, zuege):
        if cls._ist_matt(pos_koenig, zuege, farbe):
          status = 2
        else:
          status = 1
      return status
  
  @classmethod
  def setze_figur(cls, figur: str, yx_pos: tuple):
    if cls.ist_gueldig(yx_pos):
      y, x = yx_pos
      cls.__felder[y][x] = figur
      if figur in ('WK','bk'):
        index = int(figur.islower())
        cls.pos_koenig[index] = yx_pos
    else:
      print(f'Falsche Positionsangabe: {figur, yx_pos}')

  @classmethod
  def bewege_figur(cls, figur: str, von: tuple, nach: tuple):
    if cls.ist_gueldig(von):
      # TODO: prüfen ob figur sich so bewegen kann.
      cls.setze_figur(figur, nach)
      y,x = von
      cls.__felder[y][x] = '  '
  
  @classmethod
  def a(cls, farbe: chr, gegner_zug: bool):
    brett_kopie = cls.hole_brett_kopie()
    for yx in Brett.hole_güldige_züge(farbe, gegner_zug):
      y,x = yx
      brett_kopie[y][x] = '**'
    Brett.print_brett(brett_kopie)

  @classmethod
  def b(cls, farbe):
    print(sorted(cls.__KOORDS))
    for k_yx in cls.iter_figuren_positionen(farbe):
      print(k_yx)
  
  @classmethod
  def c(cls):
    brett = cls.__felder
    Brett.print_brett(brett)



Brett.init(False)
#Brett.setze_figur("WK", (6,4))
# Brett.setze_figur("bp", (5,5))
# for i in range(8):
# for k_yx in Brett.hole_güldige_züge('W'):
  # xy = (k_yx[1], k_yx[0])
  # Brett.print_brett(Brett.zeige_güldige_Züge((6,i)))
# Brett.print_brett()
# print(Brett.hole_königPos('b'))
# Brett.b('W')
#for fig in ("bp","bn"):
#  Brett.setze_figur(fig, (5,5))
  # print(f'Ist Schach: {Brett.ist_schach("W")}')
#  Brett.a('b', True)
# for _ in Brett.hole_güldige_züge('W', True):
#   print(_,end=',') 
for fig, pos in ( ("WN",(1,3)), ('bk',(2,4)), ('WQ',(2,5)), ('WP',(3,2)), ('bp',(3,3)), ('WP',(2,2))):
  Brett.setze_figur(fig,pos)
print('Original Brett:')
Brett.c()
print(f'Ist Schach: {Brett.ist_schach_oder_matt("b")}')
print(Brett.hole_güldige_züge('b', False))
Brett.a('W', True)
Brett.a('b', False)
  