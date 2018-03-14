
s = input()

%sample input
a ="X - - - - - - X - - - - - - - - - - - - - 0 0 - - - - - @ 0 - - - - - - - - - - - - - - - 0 - - - - - - @ - @ @ X - - - - - - X"

EMPTY = "-"
CORNER = "X"
WHITE_PIECE = "O"
BLACK_PIECE = "@"

DIRECTIONS = [0,1,2,3]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

s = input;
board = s.split(" ")




def countMovesByColour(colour, board):

    count = 0
    i = 0
    for c in map:
        if c == colour:
            getAdjacentMoves(c, i)

        i+=1

def getAdjacentMoves(piece_colour, piece_coord, board):
    i=0
    for i in DIRECTIONS:
        
        
    #for each adj space:


def getTileInDirection(piece_coord, dir):
    x = piece.x
    y = piece.y
    if dir == LEFT:
        x = x-1
    elif dir == UP:
        y = y+1
    elif dir == RIGHT
        x = x+1
    elif dir == DOWN:
        y = y-1

    return map[x][y]
