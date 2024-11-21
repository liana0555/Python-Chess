from vboard import *
from movement_matrix import*

def generateMM(bitmap:list,startPosY:int,startPosX:int)->list: 
    match bitmap[startPosY][startPosX].name:
        case "N":
            bitmap[startPosY][startPosX].possibleMoves = drawKnight(bitmap[startPosY][startPosX].possibleMoves,startPosY,startPosX);
            
    
        
    
        
    

def simplePieceMove(Vboard:list,startPosY:int,startPosX:int,endPosY:int,endPosX:int)->list:
    Vboard[endPosY][endPosX] = Vboard[startPosY][startPosX];
    Vboard[startPosY][startPosX] = "_";
    Vboard[endPosY][endPosX].cordY =endPosY;
    Vboard[endPosY][endPosX].cordX =endPosX;
    return Vboard;

# def pieceMove(Vboard:list,startPosY:int,startPosX:int,endPosY:int,endPosX:int)->list:
#     if inBoard(startPosY,startPosX) and  inBoard(endPosY,endPosX):
        

def test():
    board=initBoardR();
    testBoardPrint(board);
    print(board[0][0].cordX);
    print(board[0][0].cordY);
    generateMM(board,0,1);
    testPrint(board[0][1].possibleMoves);

test();
