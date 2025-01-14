from piece import *
import random # Python library

#   Drawing board
def initClearb()->list:
    return [['0']*8 for y in range(8)]

#   Drawing board foe white
def initBoardW()->list:
    VBoard=[['_']*8 for y in range(8)]
    for i in range(8):
        VBoard[0][i]=Piece('RNBQKBNR'[i],Color.black)
        VBoard[1][i]=Pawn('P',Color.black,1)
        VBoard[7][i]=Piece('RNBQKBNR'[i],Color.white)
        VBoard[6][i]=Pawn('P',Color.white,-1)
    return VBoard

#   Drawing board for black
def initBoardB()->list:
    VBoard=[['_']*8 for y in range(8)]
    for i in range(8):
        VBoard[0][i]=Piece('RNBQKBNR'[i],Color.white)
        VBoard[1][i]=Pawn('P',Color.white,1)
        VBoard[7][i]=Piece('RNBQKBNR'[i],Color.black)
        VBoard[6][i]=Pawn('P',Color.black,-1)
    return VBoard    

#   Drawing random board
def initBoardR()->list:
    return initBoardW() if random.randint(0,1)==1 else initBoardB()
     
# Testing how the board looks
def testBoardPrint(bitmap:list)->None:
    for i in range(len(bitmap)):
        row:list=['']*8 
        for j in range(len(bitmap)):
            
            if type(bitmap[i][j]) == Piece:
                row[j]= bitmap[i][j].name
               
            else:
                row[j]= bitmap[i][j]
        print(row)

 
