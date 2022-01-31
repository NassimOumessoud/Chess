import numpy as np 
import click
"""
1. Initialize board and pieces (images) and starting positions for each piece.
    By using functions.
2. Use Class to determine next moves and legal moves, starting game is an instance of the class
"""


class Board():
    """
    Chess engine to initialize standard and custom chess games.
    """
    def __init__(self, mode='standard'):

        if mode == 'standard':
            self.game = self.board()
            self.count = 0
            self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            self.moves = {}

        else:
            pass
            

    #def __str__(self):
    #    print(self.game)
    #    return self.game


    def board(self):
        """
        Creates a standard chess board with pieces in place, white pieces on the bottom columns.
        """
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
         

    def turn(self, name):
        """"Function to check whether the right player makes the move."""
        if self.count % 2 == 0:
            color = 'W'

        elif self.count % 2 == 1:
            color = 'B'

        if name[0] != color:
            print('It is not your turn, please wait until the other player has made a move!')
            return self.move()


    def diagonal(self, location, vars=7):
            options  = []
            name = self.game[location[1], location[0]]
            for sign in [-1, 1]:
                for var in range(1, vars + 1):
                    xd = location[1] - sign*var
                    yd = location[0] + sign*var

                    if (0 <= xd < 8) and (0 <= yd < 8):
                        if self.game[yd, xd][0] == self.turn(name):
                            break
                        options.append([yd, xd])


            for sign in [-1, 1]:
                for var in range(1, vars + 1):
                    xm = location[1] + sign*var
                    ym = location[0] + sign*var
                    
                    if (0 <= xm < 8) and (0 <= ym < 8):
                        if self.game[ym, xm][0] == self.turn(name):
                            break
                        options.append([ym, xm])

            return options


    def legal_moves(self, name, position, new_position):
        """Function that for each chess piece determines the possible spots it 
        can move to."""
        
        tiles = range(8)
        NAME = name[1]
        signs = [-1, 1]


        if NAME == 'p':
            if name[0] == 'W':
                sign = signs[0]
            elif name[0] == 'B':
                sign = signs[1]


            for value in self.moves.values():
                value = value[0]
                cn_position = self.letters[position[1]]

                if f"{str(cn_position), str(position[0])}" == f"{value[-2], value[-1]}":
                    options = [[position[0] + sign, position[1]]]
                    return options


            options = [[position[0] + sign, position[1]], 
                                [position[0] + 2 * sign, position[1]]]
            
    
        if NAME == 'b':
            options = self.diagonal(position)
            

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
            
            
        if NAME == 'r':
            options = []
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])

                
        if NAME == 'Q':
            options = []
                    
            for tile in tiles:
                options.append([position[0], tile])
                options.append([tile, position[1]])
            diagonal_options = self.diagonal(position)
            
            options.extend(diagonal_options)
                        
                        
        if NAME == 'K':
            options = []
 
            for i in [-1, 1]:
                if (0 <= position[1] + i < 8):
                    options.append([position[0], position[1] + i])
                
                if (0 <= position[0] + i < 8):
                    options.append([position[0] + i, position[1]])

            diagonal_options = self.diagonal(position, vars=1)
            options.extend(diagonal_options)
            
          
        return options
    
    
    def move(self):

        @click.command()
        @click.option('--positions', prompt='What will be your next move?', nargs=2, type=str, help='Type two positions in chess format. The piece on position 1 will move to position 2.')
        def movement(positions):

            #if positions == 'o-o-o':     

            
            positions = [position for position in positions]
            
            move = [f"{positions[0]}{positions[1]} --> {positions[-2]}{positions[-1]}"]

            for index, position in enumerate(positions):
                if position.lower() in self.letters:
                    positions[index] = int(self.letters.index(position))


            old = [8 - int(positions[1]), int(positions[0])]
            new = [8 - int(positions[-1]), int(positions[-2])]
            path = [old[0]-new[0], old[1]-new[1]]
            print(path)
            name = self.game[old[0], old[1]]
            
            self.turn(name)

            options = Board.legal_moves(self, name, old, new)
            for option in options:
    
                if option != new and name[1] != 'h':
                    if self.game[option[0], option[1]] != '--':
                        print(option, new)
                        print('This is not a valid move, another piece is in the way. Please provide a new move.')        
                        return self.move()

            for option in options:
                if option == new:
                    self.game[new[0], new[1]] = name
                    self.game[old[0], old[1]] = '--'
                    self.count += 1
                    self.moves[self.count] = move

                    print(self.game)
                    return self.move()

            print("This is not a valid move, please type a valid move.")
            return self.move()
        movement()
    
