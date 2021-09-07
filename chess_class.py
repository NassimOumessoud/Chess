import numpy as np 
import click
"""
1. Initialize board and pieces (images) and starting positions for each piece.
2. Determine whose turn it is
3. determine all legal moves

"""


class Piece():
    """Class that, given the name and starting position of a chess piece 
       can determine its possible future positions and move the piece. 
       
    """
    def __init__(self, name, init_position):
        self.name = name
        self.starting_position = init_position
                
                    
    def legal_moves(self, position):
        """Function that for each chess piece determines the possible spots it 
        can move to."""
        
        tiles = range(8)
        
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
            
            
        if self.name == 'bishop':
            options = []
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
                
                
        if self.name == 'queen':
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
                    
                        
        if self.name == 'king':
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
    
    
    def move(self, position, new_position):
        if new_position in self.legal_moves(position):
            return new_position
        
        
    def take():
        pass
    
    
def placer(displace, row=[0, 7], amount=2):
    positions = []
    
    if amount == 2:
        for i in range(amount):
            x = displace[i]   
            y = row[i]
            positions.append([y, x])
        
    if amount > 2:
        names = ['Bp', 'Wp']
        sign = [1, -1]
        for i in range(2):
            y = row[i] + sign[i]
            name = names[i]
            for dis in displace:
                x = dis
                positions.append([y, x, name])
                
    return positions
            
def board(starts):
    squares = 8
    grid = np.full((squares, squares), '--', dtype=np.dtype('U100'))
    for start in starts:
        print(start[2])
        grid[start[0], start[1]] = start[2]
    return grid


@click.command()
@click.option('--menu', prompt="""Welcome to our 1v1 chess player, please type 'start' to play.
                                  To see the game rules please type: 'rules'
                                  To see a tutorial please type: 'tutorial'""",
              help='The main menu')
def init(menu):
    if menu.lower() == 'start':
        click.echo("Let's start!")    
        
    pawns = placer([i for i in range(8)], amount=8)
    print(pawns)
    game = board(pawns)
    click.echo(game)
    
if __name__ == '__main__':
    init()


