import vboard
from piece import *

#   Drawing board for Puzzle (1,2,3)
def initPuzzle1()->list:
    VBoard=[['_']*8 for y in range(8)]
    VBoard[0][0]=Piece('K',Color.black)
    VBoard[0][2]=Piece('K',Color.white)
    VBoard[0][1]=Piece('B',Color.black)
    VBoard[1][0]=Pawn('P',Color.black,1)
    VBoard[1][1]=Pawn('P',Color.black,1)
    VBoard[7][0]=Piece('R',Color.white)
    VBoard[2][1]=Pawn('P',Color.white,-1)
    return VBoard

def initPuzzle2()->list:
    VBoard=[['_']*8 for y in range(8)]
    VBoard[1][0]=Piece('K',Color.black)
    VBoard[0][2]=Piece('K',Color.white)
    VBoard[2][0]=Pawn('P',Color.black,1)
    VBoard[1][1]=Pawn('P',Color.black,1)
    VBoard[3][1]=Pawn('P',Color.white,-1)
    VBoard[6][7]=Pawn('P',Color.white,-1)
    return VBoard

def initPuzzle3()->list:
    VBoard=[['_']*8 for y in range(8)]
    VBoard[1][3]=Piece('K',Color.black)
    VBoard[4][4]=Piece('K',Color.white)
    VBoard[1][0]=Piece('R',Color.black)
    VBoard[3][4]=Pawn('P',Color.white,-1)
    VBoard[2][7]=Piece('R',Color.white)
    return VBoard


