from queue import *

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

NOT_VISITED = -1
BOARD_LEN = 8


############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for x in range(BOARD_LEN):
        print(board[x])
        for y in range(BOARD_LEN):
            
            if board[x][y] == colour:
                count += len(getAdjacentMoves(x, y, board))
    print(count)


        
# Changed so this now returns an array of the adjacent moves
# in form [(x,y),(x2,y2)...]
# Better for part 2 and easy to get count from len!
def getAdjacentMoves(x, y, board):
    count = 0
    moves = []
    for dir in DIRECTIONS:
        curr_x, curr_y = getCoordInDir(x,y, dir)

        #checks if out of bounds!
        if isOutOfBounds(curr_x,curr_y,board):
            #Can't move here
            continue
        
        curr_piece = board[curr_x][curr_y]

        #if a piece blocks its way, checks if it can jump over
        #this changes curr_x and curr_y to the jump ones
        if (curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE):
            curr_x, curr_y = getCoordInDir(curr_x, curr_y, dir)
            if (isOutOfBounds(curr_x, curr_y, board) or
                board[curr_x][curr_y] != EMPTY):
                #Can't jump over piece
                continue
            
        moves += [(curr_x,curr_y)]
    return moves             


def isOutOfBounds(x,y,board):
    if (x<0 or x>7 or y<0 or y>7 or board[x][y] == CORNER):
        return True
    return False

#gets the coordinate in the given direction
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

                findClosestPiece(killable[0][0])


# Checks if a peice is killable and returns the possible kill pairs as
# as an array of tuples
def isKillable(colour, x, y, board):
    killable = []

    # Checks horizontal pair
    if (isKillSpot(getCoordInDir(x,y,LEFT), board, colour) and
        isKillSpot(getCoordInDir(x,y,RIGHT), board, colour)):

        #this means killable = [[(2,4),(4,4)],[...]]
        #puts the array in the form [PAIR,PAIR,PAIR]...
        #first pair is accessed through k[0]
        #side of pair is accesssed through k[0][0]
        #x of side of pair is accessed through k[0][0][0]
        killable += [[(getCoordInDir(x,y,LEFT)), getCoordInDir(x,y,RIGHT)]]
                
    # checks vertical pair
    if (isKillSpot(getCoordInDir(x,y,UP), board, colour) and
        isKillSpot(getCoordInDir(x,y,DOWN), board, colour)):
        killable += [[(getCoordInDir(x,y,UP)), (getCoordInDir(x,y,DOWN))]]
    #print(killable)
    return killable

        

def isKillSpot(coord, board, colour):

    if isOffBoard(coord, board):
        return False
    
    curr = board[coord[0]][coord[1]]
    return (curr == CORNER or
            curr == colour or
            curr == EMPTY)

#def findClosestPair():
    #TODO


#finds the closest piece
#loc is a tuple (x,y)
#Basically BFS

#currently get adjacent isn't checking for our pieces
#If we use the closer of the 2 
def findClosestPiece(loc):

    #init the visited array to NOT visisted
    visited = []
    for i in range(BOARD_LEN):
        temp_line = []
        for j in range(BOARD_LEN):
            temp_line.append(NOT_VISITED)
        visited.append(temp_line)
        
    dist = 0
    visited[loc[0]][loc[1]] = dist

    #init the queue
    q = Queue()
    q.put(loc)
    
    while not q.empty(): #TODO
        dist += 1
        curr = q.get()
        adj = getAdjacentMoves(curr[0],curr[1],board)
        for i in range(len(adj)):
            next = adj[i]
            if visited[adj[i][0]][adj[i][1]] == NOT_VISITED:
                q.put(next)
                visited[adj[i][0]][adj[i][1]] = visited[curr[0]][curr[1]]+1

    printBoard(visited)


def printBoard(board):
    print("Printing out the current board:")
    for i in range(BOARD_LEN):
        print("|",end="")
        for j in range(BOARD_LEN):
            print("{0:3d}".format(board[i][j]),end="")
        print("|")    
                  

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
