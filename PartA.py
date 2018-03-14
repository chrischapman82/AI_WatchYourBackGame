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





############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for x in range(board_len):
        print(board[x])
        for y in range(board_len):
            
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
#Get pos of all 
#While Black array is !empty





############## START PROGRAM ################

#Reads in input
board = []


#s = input()

board_len = 8
for i in range(board_len):
    temp_line = input().split(" ")
    board.append(temp_line)

print(board)
# if move:
# count Moves by Colour

if (input() = "Moves"):
    

countMovesByColour(BLACK_PIECE, board)
countMovesByColour(WHITE_PIECE, board)


