from piece import *;
import random;


def initBoardW()->list:
    VBoard=[['_']*8 for y in range(8)];
    for i in range(8):
        VBoard[0][i]=Piece('RNBQKBNR'[i],Color.black,0,i);
        VBoard[1][i]=Piece('P',Color.black,1,i);
        VBoard[7][i]=Piece('RNBQKBNR'[i],Color.white,7,i);
        VBoard[6][i]=Piece('P',Color.white,6,i);
    return VBoard;
def initBoardB()->list:
    VBoard=[['_']*8 for y in range(8)];
    for i in range(8):
        VBoard[0][i]=Piece('RNBQKBNR'[i],Color.white,0,i);
        VBoard[1][i]=Piece('P',Color.white,1,i);
        VBoard[7][i]=Piece('RNBQKBNR'[i],Color.black,7,i);
        VBoard[6][i]=Piece('P',Color.black,6,i);
    return VBoard;    

def initBoardR()->list:
    return initBoardW() if random.randint(0,1)==1 else initBoardB();
     

def testBoardPrint(bitmap:list)->None:
    for i in range(len(bitmap)):
        row:list=['']*8; 
        for j in range(len(bitmap)):
            
            if type(bitmap[i][j]) == Piece:
                row[j]= bitmap[i][j].name;
               
            else:
                row[j]= bitmap[i][j];
        print(row);

        

