from vboard import *
from movement_matrix import *

# Decides the movement pattern for a given piece on the board
def decideMovePattern(piece: Piece, startY: int, startX: int) -> list:

# Initialize an empty 8x8 board for the move pattern
    bitmap = [['0'] * 8 for _ in range(8)]

 # Map piece types to their respective movement functions
    moveDrawers = {
        'k': drawKing,
        'q': drawQween,
        'r': drawAxis,
        'b': drawDiags,
        'n': drawKnight,
    }

    if isinstance(piece, Pawn):
# Draw the pawn's moves based on its direction
        bitmap = drawPawn(bitmap, startY, startX, piece.direction)
    elif piece.name.lower() in moveDrawers:
# Call the corresponding function for other pieces
        bitmap = moveDrawers[piece.name.lower()](bitmap, startY, startX)
    else:
# Raise an error for unknown piece types
        raise ValueError(f"Unknown piece type: {piece.name}")

    return bitmap

#Watch all the opponent's movement (To see where we can put the king where we can't)
def allOpponentMoves(board: list, color: str) -> list:
    vboard = initClearb() # Initialize a blank virtual board
    opponentColor = '1' if color == '0' else '0' # Determine opponent's color

    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]

                if piece.color != opponentColor:
                    continue # Skip if the piece is not an opponent's piece

# Handle different piece types and their attack patterns
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

# Simulates a move on the board and returns the resulting board
def simulateMove(board: list, startY: int, startX: int, endY: int, endX: int) -> list:
    simulatedBoard = [row[:] for row in board]
    simulatedBoard[endY][endX] = simulatedBoard[startY][startX]
    simulatedBoard[startY][startX] = '0'
    return simulatedBoard

# Checks if the king of a given color is in check
def isKingInCheck(board: list, color: str) -> bool:
    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]
                if piece.name.lower() == 'k' and piece.color == color:
                    opponentMoves = allOpponentMoves(board, color)
                    return opponentMoves[y][x] == '1' # King is under attack
    return False

# Determines if a player's king is in checkmate
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
                                    return False  # Escape possible
    return True

# Restricts moves for a piece based on game rules and the board state
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
                        possibleMoves[y][x] = '0' # Path blocked
                        continue

                if piece.name.lower() == 'p':
                    if not validatePawnMove(board, piece, startY, startX, y, x):
                        possibleMoves[y][x] = '0'
                        continue
                    if checkEnPassant(board, piece, startY, startX, y, x):
                        possibleMoves[y][x] = '2'  # Mark en passant square as "2"

            #Checking the king when he is checkmated
                if piece.name.lower() == 'k':
                    simulatedBoard = simulateMove(board, startY, startX, y, x)
                    if isKingInCheck(simulatedBoard, piece.color):
                        possibleMoves[y][x] = '0'
                    continue
            #Checking other pieces when they can't move away because there will be a check
                if recursionDepth == 0 and piece.name.lower() != 'k':
                    simulatedBoard = simulateMove(board, startY, startX, y, x)
                    if isKingInCheck(simulatedBoard, piece.color):
                        possibleMoves[y][x] = '0'

  # Handle castling moves for the king
    if piece.name.lower() == 'k':
        if canCastle(board, piece, startY, startX, 'left'):
            possibleMoves[startY][startX - 2] = '2'  # Mark left castle square as "2"
        if canCastle(board, piece, startY, startX, 'right'):
            possibleMoves[startY][startX + 2] = '2'  # Mark right castle square as "2"

    return possibleMoves

# Checks if the path between two squares is clear
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

# Validates a pawn's move
def validatePawnMove(board: list, piece: Piece, startY: int, startX: int, endY: int, endX: int) -> bool:

    if abs(endX - startX) == 1 and endY - startY == piece.direction:
        return isOpponent(board, startY, startX, endY, endX) or checkEnPassant(board,   piece, startY, startX, endY, endX)



    if endX == startX:
        if endY - startY == piece.direction and not isPiece(board, endY, endX):
            return True
        if abs(endY - startY) == 2 and startY in (1, 6) and not isPiece(board, endY, endX):
            intermediateY = startY + piece.direction
            if not isPiece(board, intermediateY, startX):
                return True

    return False


# Checks if castling is possible
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

# Executes a castling move
def executeCastle(board: list, kingY: int, kingX: int, direction: str) -> list:
    rookX = 0 if direction == 'left' else 7
    rookNewX = kingX - 1 if direction == 'left' else kingX + 1
    kingNewX = kingX - 2 if direction == 'left' else kingX + 2

    board[kingY][kingNewX] = board[kingY][kingX]
    board[kingY][kingX] = '_'

    board[kingY][rookNewX] = board[kingY][rookX]
    board[kingY][rookX] = '_'

    return board

# Checks if an en passant capture is possible
def checkEnPassant(board: list, piece: Piece, startY: int, startX: int, endY: int, endX: int):
    if abs(endX - startX) == 1 and endY - startY == piece.direction:
        opponentPawn = board[startY][endX]
        if isinstance(opponentPawn, Piece) and opponentPawn.name.lower() == 'p' and \
            opponentPawn.color != piece.color and opponentPawn.justMovedTwo:
            return True
    return False

# Executes an en passant capture
def executeEnPassant(board: list, pawnY: int, pawnX: int, targetY: int, targetX: int) -> list:
    board[targetY][targetX] = board[pawnY][pawnX]
    board[pawnY][pawnX] = '_'
    board[pawnY][targetX] = '_'

    return board

# Merges two boards, combining their attack patterns
def mergeBoards(board1: list, board2: list) -> list:
    return [
        ['1' if a == '1' or b == '1' else '0' for a, b in zip(row1, row2)]
        for row1, row2 in zip(board1, board2)
    ]
