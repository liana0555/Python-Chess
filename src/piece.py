class Color(enumerate):
    white="1";
    black="0"; 

class Piece():
    
    def __init__(self,name:str,color:Color)->None:
        self.name=name;
        self.color=color;
        self.possibleMoves=[['0']*8 for y in range(8)];
 
class Pawn(Piece):
        
    def __init__(self,name:str,color:Color,direction:int)->None:
        super().__init__(name,color);
        self.direction= direction; 
        self.possibleMoves=[['0']*8 for y in range(8)];  


def isPiece(bitmap:list,posY:int,posX:int)->bool:
    return  isinstance(bitmap[posY][posX], Piece) ;

def inBoard(posY:int,posX:int)->bool:
    return 0 <= posX < 8 and 0 <= posY < 8;

def isAlly(bitmap: list, startPosY: int, startPosX: int, targetPosY: int, targetPosX: int) -> bool:
 
    if not inBoard(startPosY, startPosX) or not inBoard(targetPosY, targetPosX):
        return False  

    if not isPiece(bitmap, startPosY, startPosX):
        return False  

    if not isPiece(bitmap, targetPosY, targetPosX):
        return False  
    startPiece = bitmap[startPosY][startPosX]
    targetPiece = bitmap[targetPosY][targetPosX]

    return startPiece.color == targetPiece.color


def isOpponent(bitmap: list, startPosY: int, startPosX: int, targetPosY: int, targetPosX: int) -> bool:
 
    if not inBoard(startPosY, startPosX) or not inBoard(targetPosY, targetPosX):
        return False  

    if not isPiece(bitmap, startPosY, startPosX):
        return False  

    if not isPiece(bitmap, targetPosY, targetPosX):
        return False  
    startPiece = bitmap[startPosY][startPosX]
    targetPiece = bitmap[targetPosY][targetPosX]

    return startPiece.color != targetPiece.color