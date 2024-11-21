class Color(enumerate):
    white="1";
    black="0"; 

class Piece():
    
    def __init__(self,name:str,color:Color,cordY:int,cordX:int)->None:
        self.name=name;
        self.color=color;
        self.cordY=cordY;
        self.cordX=cordX;
        self.possibleMoves=[['0']*8 for y in range(8)];
    

def isPiece(bitmap:list,posY:int,posX:int)->bool:
    return  type(bitmap[posY][posX]) == Piece;

def isAlly(bitmap:list,startPosY:int,startPosX):
    print("yes") ;   
    
