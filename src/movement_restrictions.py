from vboard import *
from movement_matrix import *
from special_moves import *

def decideMovePattern(piece: Piece, startY: int, startX: int) -> list:
    bitmap = [['0'] * 8 for _ in range(8)]

    moveDrawers = {
        'k': drawKing,
        'q': drawQween,
        'r': drawAxis,
        'b': drawDiags,
        'n': drawKnight,
    }

    if isinstance(piece, Pawn):
        bitmap = drawPawn(bitmap, startY, startX, piece.direction)
    elif piece.name.lower() in moveDrawers:
        bitmap = moveDrawers[piece.name.lower()](bitmap, startY, startX)
    else:
        raise ValueError(f"Unknown piece type: {piece.name}")

    return bitmap

def allOpponentMoves(board: list, color: str) -> list:
    vboard = initClearb()
    opponentColor = '1' if color == '0' else '0'

    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]

                if piece.color != opponentColor:
                    continue

                if piece.name.lower() in ['q', 'r', 'b', 'n']:
                    attackMoves = restrictImpossibleMoves(board, piece, y, x, recursionDepth=1)
                elif piece.name.lower() == 'p':
                    attackMoves = drawPawnAtack(initClearb(), y, x, piece.direction)
                elif piece.name.lower() == 'k':
                    attackMoves = drawKing(initClearb(), y, x)
                else:
                    continue

                vboard = mergeBoards(vboard, attackMoves)

    return vboard

def simulateMove(board: list, startY: int, startX: int, endY: int, endX: int) -> list:
    simulatedBoard = [row[:] for row in board]
    simulatedBoard[endY][endX] = simulatedBoard[startY][startX]
    simulatedBoard[startY][startX] = '0'
    return simulatedBoard

def isKingInCheck(board: list, color: str) -> bool:
    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]
                if piece.name.lower() == 'k' and piece.color == color:
                    opponentMoves = allOpponentMoves(board, color)
                    return opponentMoves[y][x] == '1'
    return False

def isMate(board: list, color: str) -> bool:
    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]
                if piece.color == color:
                    possibleMoves = restrictImpossibleMoves(board, piece, y, x)
                    for moveY in range(8):
                        for moveX in range(8):
                            if possibleMoves[moveY][moveX] == '1':
                                simulatedBoard = simulateMove(board, y, x, moveY, moveX)
                                if not isKingInCheck(simulatedBoard, color):
                                    return False
    return True

def restrictImpossibleMoves(board: list, piece: Piece, startY: int, startX: int, recursionDepth: int = 0) -> list:
    possibleMoves = decideMovePattern(piece, startY, startX)

    for y in range(8):
        for x in range(8):
            if possibleMoves[y][x] == '1':
                if not inBoard(y, x) or isAlly(board, startY, startX, y, x):
                    possibleMoves[y][x] = '0'
                    continue

                if piece.name.lower() in ['q', 'r', 'b', 'p']:
                    if not isPathClear(board, startY, startX, y, x):
                        possibleMoves[y][x] = '0'
                        continue

                if piece.name.lower() == 'p':
                    if not validatePawnMove(board, piece, startY, startX, y, x):
                        possibleMoves[y][x] = '0'
                        continue

                    if canEnPassant(board, piece, startY, startX, y, x):
                        possibleMoves[y][x] = '1'

                if piece.name.lower() == 'k':
                    simulatedBoard = simulateMove(board, startY, startX, y, x)
                    if isKingInCheck(simulatedBoard, piece.color):
                        possibleMoves[y][x] = '0'
                    continue

                if recursionDepth == 0 and piece.name.lower() != 'k':
                    simulatedBoard = simulateMove(board, startY, startX, y, x)
                    if isKingInCheck(simulatedBoard, piece.color):
                        possibleMoves[y][x] = '0'

    if piece.name.lower() == 'k':
        if canCastle(board, piece, startY, startX, 'left'):
            possibleMoves[startY][startX - 2] = '1'
        if canCastle(board, piece, startY, startX, 'right'):
            possibleMoves[startY][startX + 2] = '1'

    return possibleMoves

def isPathClear(board: list, startY: int, startX: int, endY: int, endX: int) -> bool:
    dy = endY - startY
    dx = endX - startX

    stepY = (dy // abs(dy)) if dy != 0 else 0
    stepX = (dx // abs(dx)) if dx != 0 else 0

    currentY, currentX = startY + stepY, startX + stepX
    while currentY != endY or currentX != endX:
        if isinstance(board[currentY][currentX], Piece):
            return False
        currentY += stepY
        currentX += stepX

    return True

def validatePawnMove(board: list, piece: Piece, startY: int, startX: int, endY: int, endX: int) -> bool:
    if abs(endX - startX) == 1 and abs(endY - startY) == 1:
        return isOpponent(board, startY, startX, endY, endX)

    if endX == startX:
        if abs(endY - startY) == 1 and not isPiece(board, endY, endX):
            return True
        if abs(endY - startY) == 2 and startY in (1, 6) and not isPiece(board, endY, endX):
            intermediateY = startY + (1 if piece.direction == 1 else -1)
            if not isPiece(board, intermediateY, startX):
                return True

    return False

def mergeBoards(board1: list, board2: list) -> list:
    return [
        ['1' if a == '1' or b == '1' else '0' for a, b in zip(row1, row2)]
        for row1, row2 in zip(board1, board2)
    ]
