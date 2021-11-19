import numpy as np 
import click
"""
1. Initialize board and pieces (images) and starting positions for each piece.
    By using functions.
2. Use Class to determine next moves and legal moves, starting game is an instance of the class
"""


class Board():
    """Class that, given the name and starting position of a chess piece 
       can determine its possible future positions and move the piece. 
    """
    def __init__(self):
        self.game = self.board()

    def __str__(self):
        print(self.game)
        return self.game


    def placer(self, displace, names, AMOUNT=2):
        positions = []
        row = [0, 7]
        
        if AMOUNT < 2:
            for i in range(len(names)):
                x = displace
                y = row[i]
                name = names[i]
                positions.append([y, x, name])
        
        
        if AMOUNT == 2:
            for i in range(AMOUNT):
                y = row[i] 
                name = names[i]
                for k in range(AMOUNT):
                    x = displace[k]
                    positions.append([y, x, name])
            
        if AMOUNT > 2:
            sign = [1, -1]
            for i in range(2):
                y = row[i] + sign[i]
                name = names[i]
                for dis in displace:
                    x = dis
                    positions.append([y, x, name])
                    
        return positions
     
       
    def board(self):
        SQUARES = 8
        grid = np.full((SQUARES, SQUARES), '--', dtype=np.dtype('U100'))

        pawns = self.placer([i for i in range(8)], ['Bp', 'Wp'], AMOUNT=8)
        rooks = self.placer([0, 7], ['Br', 'Wr'])
        horses = self.placer([1, 6], ['Bh', 'Wh'])
        bishops = self.placer([2, 5], ['Bb', 'Wb'])
        queens = self.placer(3, ['BQ', 'WQ'], AMOUNT = 1)
        kings = self.placer(4, ['BK', 'WK'], AMOUNT = 1)
        starts = pawns + rooks + horses + bishops + queens + kings

        for start in starts:
            grid[start[0], start[1]] = start[2]

        return grid
         

    def legal_moves(name, position):
        """Function that for each chess piece determines the possible spots it 
        can move to."""
        
        tiles = range(8)
        NAME = name[1]
        
        def diagonal(location, var):
            xd = location[1] - var
            yd = location[0] + var
            
            xm = location[1] + var
            ym = location[0] + var
                    
            if (0 <= xd < 8) and (0 <= yd < 8):
                if (0 <= xm < 8) and (0 <= ym < 8):
                    return [[yd, xd], [ym, xm]]
            
            if (0 <= xd < 8) and (0 <= yd < 8):
                return [yd, xd]
            
            if (0 <= xm < 8) and (0 <= ym < 8):
                return [ym, xm]
            

        if NAME == 'p':
            if name[0] == 'W':
                options = [[position[0] - 1, position[1]], 
                            [position[0] - 2, position[1]]]

            if name[0] == 'B':
                options = [[position[0] + 1, position[1]], 
                            [position[0] + 2, position[1]]]
        
    
        if NAME == 'r':
            options = [[[tile, position[1]] for tile in tiles],
                      [[position[0], tile] for tile in tiles]]
                       
            
        if NAME == 'h':
            displace = [-2, -1, 1, 2]
            options = []
            for i in displace:
                x = position[0] + i
                if x <= 0:
                    continue
                for k in displace:
                    y = position[1] + k 
                    if y <= 0:
                        continue
                    if np.abs(k) != np.abs(i):
                        options.append([x, y])
                    else:
                        continue
            
            
        if NAME == 'b':
            options = []
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
                
                
        if NAME == 'Q':
            options = []
                    
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
        
            for tile in range(-tiles[-1], tiles[-1] + 1):
                print(tile)
                xd = position[1] - tile
                yd = position[0] + tile
                
                xm = position[1] + tile
                ym = position[0] + tile
                
                if (0 <= xd < 8) and (0 <= yd < 8):
                    options.append([yd, xd])
            
                if (0 <= xm < 8) and (0 <= ym < 8):
                    options.append([ym, xm])
                    
                        
        if NAME == 'K':
            options = []
            signs = [-1, 1]
            for i in signs:
                xd = position[1] - i
                yd = position[0] + i
                
                xm = position[1] + i
                ym = position[0] + i
                
                if (0 <= xd < 8) and (0 <= yd < 8):
                    options.append([yd, xd])
            
                if (0 <= xm < 8) and (0 <= ym < 8):
                    options.append([ym, xm])
                    
                if (0 <= position[1] + i < 8):
                    options.append([position[0], position[1] + i])
                
                if (0 <= position[0] + i < 8):
                    options.append([position[0] + i, position[1]])
                    
        return options
    
    
    def move(self):
        @click.command()
        @click.option('--positions', prompt='What will be your next move?', nargs=2, type=str, help='Type two positions in chess format. The piece on position 1 will move to position 2.')
        def movement(positions):
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            positions = [pos for pos in positions]

            print(f"Received positions: {positions}")
            for index, pos in enumerate(positions):
                if pos.lower() in letters:
                    pos = int(letters.index(pos))
                    positions[index] = pos

            print(f"Modified positions: {positions}")
            old = [8 - int(positions[1]), int(positions[0])]
            new = [8 - int(positions[-1]), int(positions[-2])]
            print(old, new)
            
            name = self.game[old[0], old[1]]
            
            if new in Board.legal_moves(name, old):    
                self.game[new[0], new[1]] = name
                self.game[old[0], old[1]] = '--'
                print(self.game)
                return self.move()
            else:
                print('This is not a valid move')
                return self.move()
        movement()
    


def init():
    """Initialization function."""

    play = Board()
    print(play.game)
    play.move()
    

if __name__ == '__main__':
    init()


