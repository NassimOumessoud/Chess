import numpy as np 

"""
1. Initialize board and pieces (images) and starting positions for each piece.
2. Determine whose turn it is
3. determine all legal moves

"""

class Piece():
    """Class that, given the name and starting position of a chess piece 
       can determine its possible future positions and move the piece. 
       
    """
    def __init__(self, name, position):
        self.name = name
        self.starting_position = position
        
    def legal_moves(self, position):
        
        tiles = range(8)
        print(tiles)
        if self.name == 'pawn':
            
            if position != self.starting_position:
                options = [position[0], position[1] + 1]
                
            elif position == self.starting_position:
                options = [[position[0], position[1] + 1], 
                          [position[0], position[1] + 2]]
    
        if self.name == 'rook':
            options = [[[tile, position[1]] for tile in tiles],
                      [[position[0], tile] for tile in tiles]]
                       
        if self.name == 'horse':
            options = []
            for i in [-2, -1, 1, 2]:
                x = position[0] + i
                if x <= 0:
                    continue
                for k in [2, 1, -1, -2]:
                    y = position[1] + k 
                    if y <= 0:
                        continue
                    if np.abs(k) != np.abs(i):
                        options.append([x, y])
                    else:
                        continue
            
        if self.name == 'bishop':
            options = []
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
                
        if self.name == 'queen':
            options = []
            def add(x, y):
                if x and y < 8 :
                    options.append([x, y])
                    
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
                for sign in range(5):

                    if sign == 1:
                        x = position[0] + tile
                        y = position[1] + tile
                        add(x, y)
                    if sign == 2:
                        
                        x = position[0] - tile
                        y = position[1] - tile
                        if x and y >= 0:
                            add(x, y)
                    if sign == 3:
                        x = position[0] - tile
                        y = position[1] + tile
                        if x and y >= 0:
                            add(x, y)
                    if sign == 4:
                        x = position[0] + tile
                        y = position[1] - tile
                        if x and y >= 0:
                            add(x, y)
                    
#        if self.name == 'king':
        
        return options
    
    
    def move():
        pass
    def take():
        pass

horse = Piece('horse', [2, 1])
pawn_position = [4, 2]

print(horse.legal_moves([2, 1]))

queen = Piece('queen', [4, 1])
print(queen.legal_moves([4, 1])) 


def board(start, positions):
    squares = 8
    grid = np.full((squares, squares), '-', dtype=str)
    grid[start[1], start[0]] = 'x'
    for position in positions:
        x = position[0]
        y = position[1]
        grid[y, x] = 'o'
    print(grid)
        
board([4, 4], queen.legal_moves([4, 4]))


