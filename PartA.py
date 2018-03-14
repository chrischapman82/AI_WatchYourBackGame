
s = input()

EMPTY = "-"
CORNER = "X"
WHITE_PIECE = "O"
BLACK_PIECE = "@"

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

map = s.split(" ")

class Piece:
    x,y,colour


def countMovesByColour(colour, map):

    count = 0
    i = 0
    for c in map:
        if c == colour:
            getAdjacentMoves(c, i)

        i+=1


def getAdjacentMoves(piece):
    i=0
    for i in range(0,4):
        if (
    #for each adj space:


def getTileInDirection(piece, dir):
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
