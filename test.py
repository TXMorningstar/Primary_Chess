import chess

MAINBOARD = chess.Board()
strategy = MAINBOARD.movable((2,1), price=True)
print(strategy)