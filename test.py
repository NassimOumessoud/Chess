import chess_engine


def init():
    """Initialization function."""

    play = chess_engine.Board()
    print(play.game)
    play.move()
    

if __name__ == '__main__':
    init()
