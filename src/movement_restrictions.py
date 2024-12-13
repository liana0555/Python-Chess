from vboard import *
from movement_matrix import*

def decideMovePattern(piece: Piece, startPosY: int, startPosX: int) -> list:
    bitmap = [['0'] * 8 for _ in range(8)]
    if isinstance(piece, Pawn):
        bitmap = drawPawn(bitmap, startPosY, startPosX, piece.direction)
    elif piece.name.lower() == 'k':
        bitmap = drawKing(bitmap, startPosY, startPosX)
    elif piece.name.lower() == 'q':
        bitmap = drawQween(bitmap, startPosY, startPosX)
    elif piece.name.lower() == 'r':
        bitmap = drawAxis(bitmap, startPosY, startPosX)
    elif piece.name.lower() == 'b':
        bitmap = drawDiags(bitmap, startPosY, startPosX)
    elif piece.name.lower() == 'n':
        bitmap = drawKnight(bitmap, startPosY, startPosX)
    else:
        raise ValueError(f"Unknown piece type: {piece.name}")
    return bitmap
            
def allOpponentMoves(board: list, color: str) -> list:
    # Initialize a clear virtual board to track attack moves
    Vboard: list = initClearb()

    opponent_color = '1' if color == '0' else '0'
    
    # Iterate through the board
    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]
                
                # Guard against functions accidentally modifying the board
                board_copy = [row[:] for row in board]  # Work on a copy

                # Generate attack moves for different piece types
                if piece.color == opponent_color and piece.name.lower() in ['q', 'r', 'b', 'n']:
                    attack_moves = restrictImpossibleMoves(initClearb(), piece, y, x)
                elif piece.color == opponent_color and piece.name.lower() == 'p':
                    testPrint(drawPawnAtack(initClearb(), y, x, piece.direction))
                    attack_moves = drawPawnAtack(initClearb(), y, x, piece.direction)
                elif piece.color == opponent_color and piece.name.lower() == 'k':
                    attack_moves = drawKing(initClearb(), y, x)
                else:
                    continue  # Skip if piece type is not recognized

                # Merge attack moves with the virtual board
                Vboard = [
                    ['1' if a == '1' or b == '1' else '0' for a, b in zip(row1, row2)]
                    for row1, row2 in zip(Vboard, attack_moves)
                ]
    
    return Vboard


def simulateMove(board: list, startY: int, startX: int, endY: int, endX: int) -> list:
    simulated_board = [row[:] for row in board]  # Deep copy of the board
    simulated_board[endY][endX] = simulated_board[startY][startX]  # Move piece
    simulated_board[startY][startX] = '0'  # Empty the start position
    return simulated_board

def isKingInCheck(board: list, color: str) -> bool:
    """
    Determines if the King of the specified color is in check using allOpponentMoves.
    """
    # Find the position of the King for the given color
    for y in range(8):
        for x in range(8):
            if isPiece(board, y, x):
                piece = board[y][x]
                if piece.name.lower() == 'k' and piece.color == color:
                    # Generate all opponent moves
                    opponent_moves = allOpponentMoves(board, color)
                    # Check if the King's position is under attack
                    return opponent_moves[y][x] == '1'
    return False
   
        
    
def restrictImpossibleMoves(board: list, piece: Piece, startPosY: int, startPosX: int) -> list:
    possible_moves = decideMovePattern(piece, startPosY, startPosX)
    
    for y in range(8):
        for x in range(8):
            if possible_moves[y][x] == '1':
                if not inBoard(y, x):
                    possible_moves[y][x] = '0'
                    continue
                
                if isAlly(board, startPosY, startPosX, y, x):
                    possible_moves[y][x] = '0'
                    continue
                
                if piece.name.lower() in ['q', 'r', 'b','p']:  # Queen, Rook, or Bishop
                    dy = y - startPosY
                    dx = x - startPosX
                    if abs(dy) > 1 or abs(dx) > 1:  # Ensure this is a sliding move
                        stepY = (dy // abs(dy)) if dy != 0 else 0
                        stepX = (dx // abs(dx)) if dx != 0 else 0

                        # Trace the path step by step
                        currentY, currentX = startPosY + stepY, startPosX + stepX
                        while (currentY != y or currentX != x):
                            if isinstance(board[currentY][currentX],Piece) :
                                if board[currentY][currentX].name.lower() != 'k': 
                                    possible_moves[y][x] = '0'
                                    break

                            currentY += stepY
                            currentX += stepX
                
                if piece.name.lower() == 'p':
                    if not isOpponent(board, startPosY, startPosX, y, x):
                        # Pawns can only move diagonally if capturing
                        if abs(x - startPosX) == 1 and abs(y - startPosY) == 1:
                            possible_moves[y][x] = '0'
                    else:
                        # Pawns can't move forward into an occupied square
                        if x == startPosX and abs(y - startPosY) == 1:
                            possible_moves[y][x] = '0'
                                                # Pawns can't move forward into an occupied square
                        if x == startPosX and abs(y - startPosY) == 2:
                            possible_moves[y][x] = '0'
                            
                if piece.name.lower() == 'k':
                    if allOpponentMoves(board,piece.color)[y][x]=='1':
                        possible_moves[y][x]= '0'
 
                
                

    return possible_moves
