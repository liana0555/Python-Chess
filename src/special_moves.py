from vboard import *
from movement_matrix import *

def canCastle(board: list, king: Piece, kingY: int, kingX: int, direction: str) -> bool:
    if king.name.lower() != 'k' or king.has_moved:
        return False

    rookX = 0 if direction == 'left' else 7
    rook = board[kingY][rookX]

    if not isinstance(rook, Piece) or rook.name.lower() != 'r' or rook.has_moved:
        return False

    step = -1 if direction == 'left' else 1
    currentX = kingX + step

    while currentX != rookX:
        if isPiece(board, kingY, currentX) or isKingInCheck(simulateMove(board, kingY, kingX, kingY, currentX), king.color):
            return False
        currentX += step

    return True

def executeCastle(board: list, kingY: int, kingX: int, direction: str) -> list:
    rookX = 0 if direction == 'left' else 7
    rookNewX = kingX - 1 if direction == 'left' else kingX + 1
    kingNewX = kingX - 2 if direction == 'left' else kingX + 2

    board[kingY][kingNewX] = board[kingY][kingX]
    board[kingY][kingX] = '0'

    board[kingY][rookNewX] = board[kingY][rookX]
    board[kingY][rookX] = '0'

    return board

def canEnPassant(board: list, pawn: Piece, startY: int, startX: int, endY: int, endX: int) -> bool:
    if pawn.name.lower() != 'p':
        return False

    opponentPawn = board[startY][endX]

    if not isinstance(opponentPawn, Piece) or opponentPawn.name.lower() != 'p' or opponentPawn.color == pawn.color:
        return False

    if abs(startY - endY) == 1 and abs(startX - endX) == 1 and opponentPawn.justMovedTwo:
        return True

    return False

def executeEnPassant(board: list, pawnY: int, pawnX: int, targetY: int, targetX: int) -> list:
    board[targetY][targetX] = board[pawnY][pawnX]
    board[pawnY][pawnX] = '0'

    board[pawnY][targetX] = '0'

    return board
