# from vboard import *
testbitmap =[['0']*8 for y in range(8)];

def inBoard(posY:int,posX:int)->bool:
    return 0 <= posX < 8 and 0 <= posY < 8;

def clearMap(bitmap:list)->list:
    bitmap = [['0']*8 for y in range(8)];
    return bitmap;

def drawAxis(bitmap:list,startPosY:int,startPosX:int)->list: 
    bitmap[startPosY][startPosX] = '0';   
    if inBoard(startPosY,startPosX):
        for i in range(len(bitmap)):
            bitmap[startPosY][i] = '1';
            bitmap[i][startPosX] = '1'; 
        bitmap[startPosY][startPosX] = '0';
    else:
        raise ValueError("Coordinates out of bounds");
    return bitmap;

def drawDiags(bitmap:list,startPosY:int,startPosX:int)->list: 
    bitmap[startPosY][startPosX] = '0';
    if inBoard(startPosY,startPosX):
        for i in range(len(bitmap)):
            if 0 <= startPosX + startPosY - i < 8:
                bitmap[i][startPosX + startPosY - i] = '1';
            if 0 <= startPosX - startPosY + i < 8:
                bitmap[i][startPosX - startPosY + i] = '1';
        bitmap[startPosY][startPosX] = '0';
    else:
        raise ValueError("Coordinates out of bounds");
    return bitmap;

def drawKnight(bitmap:list,startPosY:int,startPosX:int)->list: 
    if inBoard(startPosY,startPosX):
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)];
        for move in moves:
            newPosX, newPosY = startPosX + move[0], startPosY + move[1];
            if inBoard(newPosY,newPosX):
                bitmap[newPosY][newPosX] = '1';
    else:
        raise ValueError("Coordinates out of bounds");
    return bitmap;    

# def drawKing(bitmap:list, startPosY:int, startPosX:int) -> list:
#     if inBoard(startPosY, startPosX):
#         moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)];
#         for move in moves:
#             newPosX, newPosY = startPosX + move[0], startPosY + move[1];
#             if inBoard(newPosY, newPosX):
#                 bitmap[newPosY][newPosX] = '1';
#     else:
#         raise ValueError("Coordinates out of bounds");
#     return bitmap;

def drawQween(bitmap:list, startPosY:int, startPosX:int) -> list:
    drawAxis(bitmap, startPosY, startPosX);
    drawDiags(bitmap, startPosY, startPosX);
    return bitmap;


def testPrint(bitmap:list)->None:
    for i in range(len(bitmap)):
        print(bitmap[i]);
 
# testPrint(drawQween(testbitmap,2,3));
# print("---------------------------------------------")
# testbitmap=clearMap(testbitmap);
# testPritnt(drawDiags(testbitmap,2,3));
# print("---------------------------------------------")
# testbitmap=clearMap(testbitmap);
# testPritnt(drawAxis(testbitmap,2,3));
# print("---------------------------------------------")
# testbitmap=clearMap(testbitmap);
# drawAxis(testbitmap,2,3);
# testPritnt(drawDiags(testbitmap,2,3));
# def drawBasicBitMap(piece:Piece):
