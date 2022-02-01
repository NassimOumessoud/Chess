import numpy as np 
import click


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
            self.player = 'White'

        else:
            pass


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

        colours = ['White', 'Black']
        self.player = colours[self.count % 2]

        if name != self.player[0]:
            self.error(type_='Turn')
        self.player = colours[1 - self.count % 2]


    def error(self, type_='False', redo=True, block=None):
        """"Function used to call appropriate error messages for invalid moves."""

        if type_ == 'False':
            print("This is not a valid move")

        if type_ == 'Block':
            print(f'The {self.game[block[0], block[1]]} piece on {self.letters[block[1]]}{8 - block[0]} is blocking your path, please type a valid move.')

        if type_ == 'Own':
            print("You can not take your own piece, please provide a valid move.")

        if type_ == 'Turn':
            print(f'It is {self.player}\'s turn, please enter a valid move')    

        if redo:
            return self.move()


    def diagonal(self, location, vars=7):
        """Fucntion to provide diagonal positions when given a certain position on the chess board. 
        Where the length of the diagonal can be adjusted."""
        options  = []
        signs = [-1, 1]
        
        for sign in signs:
            for var in range(1, vars + 1):
                xd = location[1] - sign*var
                yd = location[0] + sign*var

                if (0 <= xd < 8) and (0 <= yd < 8):
                    options.append([yd, xd])

        for sign in signs:
            for var in range(1, vars + 1):
                xm = location[1] + sign*var
                ym = location[0] + sign*var
                
                if (0 <= xm < 8) and (0 <= ym < 8):
                    options.append([ym, xm])

        return options


    def blocking(self, current, new, possible_moves):
        """"Function to check whether pieces are blocking the move to be made."""
        step_0 = 1
        step_1 = 1
        yn = new[0]
        xn = new[1]

        if current[0] > new[0]:
            step_0 = -1
            yn -= 2
        if current[1] > new[1]:
            step_1 = -1
            xn -= 2

        if current[0] == new[0]:
            for j in range(current[1] + step_1, new[1], step_1):
                if self.game[current[0], j] != '--':
                    self.error(type_='Block', block=[current[0], j])

        if current[1] == new[1]:
            for i in range(current[0] + step_0, new[0], step_0):
                if self.game[i, current[1]] != '--':
                    self.error(type_='Block', block=[i, current[1]])
        
        for i in range(current[0], yn + 1, step_0):
            for j in range(current[1], xn + 1, step_1):
                if np.abs(current[0] - i) == np.abs(current[1] - j):
                    if [i, j] in possible_moves:
                        if (self.game[i, j] != '--') and ([i, j] != current) and ([i, j] != new):
                            self.error('Block', block=[i, j])


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
            return options
            

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
 
            for i in signs:
                if (0 <= position[1] + i < 8):
                    options.append([position[0], position[1] + i])
                
                if (0 <= position[0] + i < 8):
                    options.append([position[0] + i, position[1]])

            diagonal_options = self.diagonal(position, vars=1)
            options.extend(diagonal_options)
            return options


        self.blocking(position, new_position, options)

        return options
    
    
    def move(self):

        @click.command()
        @click.option('--positions', prompt=f'What will be {self.player}\'s next move?', nargs=2, type=str, help='Type two positions in chess format. The piece on position 1 will move to position 2.')
        def movement(positions):
            
            positions = [position for position in positions]
            
            move = [f"{positions[0]}{positions[1]} --> {positions[-2]}{positions[-1]}"]

            for index, position in enumerate(positions):
                if position.lower() in self.letters:
                    positions[index] = int(self.letters.index(position))

            #Change format to [y, x], i.e. E2 --> 2,'5'
            #Notation in script is now [0:7, 0:7] --> [up:down, left:right]
            old = [8 - int(positions[1]), int(positions[0])]
            new = [8 - int(positions[-1]), int(positions[-2])]
            name = self.game[old[0], old[1]]
            
            self.turn(name[0])
            
            if name[0] == self.game[new[0], new[1]][0]:
                self.error(type_='Own')

            options = Board.legal_moves(self, name, old, new)
            

            for option in options:
                if option == new:
                    self.game[new[0], new[1]] = name
                    self.game[old[0], old[1]] = '--'
                    self.count += 1
                    self.moves[self.count] = move

                    print(self.game)
                    return self.move()

            self.error()
            return self.move()
        movement()
    
