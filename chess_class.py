import numpy as np 

"""
1. Initialize board and piece images and starting positions for each piece.
2. 
"""

class Piece():
    def __init__(self, position):
        self.position = position

    def move(self, ):
        


    def take():
        pass


squares = 8

def board():
    """
    Initialize the board and positional grid, along with starting position of each piece.
    """
    size = 8
    rows = [i for i in range(1, size)]
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    colors = ['B', 'W']

    grid = np.full((size, size), '-', dtype=str)

    for i in [2, 7]:
        for j in range(size):
            pawn = Piece((i, j))
            if i == 2:
                grid[i, j] = 'bP'
            if i == 7:
                grid[i, j] = 'wP'

        
    
    print(grid)


board()


