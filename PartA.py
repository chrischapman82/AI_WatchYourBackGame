#sample input
a ="X - - - - - - X - - - - - - - - - - - - - 0 0 - - - - - @ 0 - - - - - - - - - - - - - - - 0 - - - - - - @ - @ @ X - - - - - - X"

#Constants
EMPTY = "-"
CORNER = "X"
WHITE_PIECE = "O"
BLACK_PIECE = "@"

DIRECTIONS = [0,1,2,3]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


BOARD_LEN = 8


############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for x in range(BOARD_LEN):
        print(board[x])
        for y in range(BOARD_LEN):
            
            if board[x][y] == colour:
                
                count += getAdjacentMoves(x, y, board)
    print(count)
        

def getAdjacentMoves(x, y, board):
    count = 0
    for dir in DIRECTIONS:
        curr_x, curr_y = getCoordInDir(x,y, dir)
        
        if isOutOfBounds(curr_x,curr_y,board):
            #Can't move here
            continue
        
        curr_piece = board[curr_x][curr_y]
    
        if (curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE):
            curr_x, curr_y = getCoordInDir(curr_x, curr_y, dir)
            if (isOutOfBounds(curr_x, curr_y, board) or
                board[curr_x][curr_y] != EMPTY):
                #Can't move there
                continue
        count += 1
    return count             


def isOutOfBounds(x,y,board):
    if (x<0 or x>7 or y<0 or y>7 or board[x][y] == CORNER):
        return True
    return False

def getCoordInDir(x,y, dir):
 
    if dir == LEFT:
        x = x-1
    elif dir == UP:
        y = y+1
    elif dir == RIGHT:
        x = x+1
    elif dir == DOWN:
        y = y-1

    return x,y


############## MASSACRE ################

#Init Killable Black Array:
#Get pos of all kill pairs
#Could get pairs of kill spots!
    #killable if 2 opposite spaces are open
    #For each kill pair:
        #
#While Black array is !empty -> keep running

def killThemAll(board):
    
    killable = []
    
    for x in range(BOARD_LEN):
        for y in range(BOARD_LEN):
            if board[x][y] == BLACK_PIECE:
                print("Checking ")
                print(x,y)
                # Checks for kill pairs. Then, adds them to array
                killable += (isKillable(WHITE_PIECE, x, y, board))

                print(killable)


# Checks if a peice is killable and returns the possible kill pairs as
# as an array of tuples
def isKillable(colour, x, y, board):
    killable = []

    # Checks horizontal pair
    if (isKillSpot(getCoordInDir(x,y,LEFT), board, colour) and
        isKillSpot(getCoordInDir(x,y,RIGHT), board, colour)):
        killable += (x,y)

    # checks vertical pair
    if (isKillSpot(getCoordInDir(x,y,UP), board, colour) and
        isKillSpot(getCoordInDir(x,y,DOWN), board, colour)):
        killable += (x,y)
    #print(killable)
    return killable

        

def isKillSpot(coord, board, colour):

    if isOffBoard(coord, board):
        return False
    
    curr = board[coord[0]][coord[1]]
    return (curr == CORNER or
            curr == colour or
            curr == EMPTY)
    

def isOffBoard(coord,board):
    x = coord[0]
    y = coord[1]
    if (x<0 or x>7 or y<0 or y>7):
        return True
    return False
        

############## START PROGRAM ################

#Reads in input
board = []


#s = input()


def initBoard():
    for i in range(BOARD_LEN):
        temp_line = input().split(" ")
        board.append(temp_line)

initBoard()

print(board)
# if move:
# count Moves by Colour

#if (input() = "Moves"):
    

countMovesByColour(BLACK_PIECE, board)
countMovesByColour(WHITE_PIECE, board)

killThemAll(board)


