import sys  

print(sys.path)
print(sys.version)

def create_board():
    return [" " for _ in range(9)]


def is_game_over(board):
    # Überprüfen Sie, ob das Spiel beendet ist (gewonnen, unentschieden oder noch nicht beendet).

    for i in range(3):
        # Überprüfen der horizontalen Zeilen
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] and board[i * 3] != " ":
            return True

        # Überprüfen der vertikalen Spalten
        if board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return True

    # Überprüfen der Diagonalen
    if board[0] == board[4] == board[8] and board[0] != " ":
        return True

    if board[2] == board[4] == board[6] and board[2] != " ":
        return True

    # Überprüfen auf ein Unentschieden (falls das Spielfeld voll ist)
    if " " not in board:
        return True

    # Das Spiel ist noch nicht beendet
    return False

def get_winner(board):
    # Ermitteln Sie den Gewinner des Spiels (X, O) oder Unentschieden.

    for i in range(3):
        # Überprüfen der horizontalen Zeilen
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] and board[i * 3] != " ":
            return board[i * 3]

        # Überprüfen der vertikalen Spalten
        if board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return board[i]

    # Überprüfen der Diagonalen
    if board[0] == board[4] == board[8] and board[0] != " ":
        return board[0]

    if board[2] == board[4] == board[6] and board[2] != " ":
        return board[2]

    # Kein Gewinner, das Spiel ist unentschieden
    return "Unentschieden"
