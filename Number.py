

pictures_folder = "pictures"

class Pawn(object):
    def __init__(self, color):  # Инициализация нового объекта
        self.color = color
    
    def __repr__(self):  # Отображение в тексте
        return ('P', 'p')[self.color]

    def get_image_key(self):  # Ключ для изображения
        return ('pawn_w', 'pawn_b')[self.color]


class Knight(object):
    def __init__(self, color): 
        self.color = color
    
    def __repr__(self):
        return ('K', 'k')[self.color]

    def get_image_key(self):
        return ('knight_w', 'knight_b')[self.color]

class Bishop(object):
    def __init__(self, color):
        self.color = color
    
    def __repr__(self):
        return ('B', 'b')[self.color]

    def get_image_key(self):
        return ('bishop_w', 'bishop_b')[self.color]

class Rook(object):
    def __init__(self, color):
        self.color = color
    
    def __repr__(self):
        return ('R', 'r')[self.color]

    def get_image_key(self):
        return ('rook_w', 'rook_b')[self.color]

class Queen(object):
    def __init__(self, color):  
        self.color = color
    
    def __repr__(self):
        return ('Q', 'q')[self.color]

    def get_image_key(self):
        return ('queen_w', 'queen_b')[self.color]

class King(object):
    def __init__(self, color): 
        self.color = color
    
    def __repr__(self):
        return ('K', 'k')[self.color]

    def get_image_key(self):
        return ('king_w', 'king_b')[self.color]