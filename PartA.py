from queue import *
import heapq

# sample input
a = "X - - - - - - X - - - - - - - - - - - - - 0 0 - - - - - @ 0 - - - - - - - - - - - - - - - 0 - - - - - - @ - @ @ X - - - - - - X"

# Constants
EMPTY = "-"
CORNER = "X"
WHITE_PIECE = "O"
BLACK_PIECE = "@"

DIRECTIONS = [0, 1, 2, 3]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

NOT_VISITED = -1
BOARD_LEN = 8


# Class for coordinates because they're easier like this
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):  # For printing
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __repr__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"


class Node:
    def __init__(self, coord, g, h):
        self.coord = coord
        self.g = g
        self.h = h
        self.f = h + g


############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for x in range(BOARD_LEN):
        print(board[x])
        for y in range(BOARD_LEN):

            if board[x][y] == colour:
                curr_coord = Coordinate(x, y)  # todo use this for getAdj
                count += len(getAdjacentMoves(curr_coord, board))
    print(count)


# Changed so this now returns an array of the adjacent moves
# in form [(x,y),(x2,y2)...]
# Better for part 2 and easy to get count from len!
def getAdjacentMoves(coord, board):
    count = 0
    moves = []
    for dir in DIRECTIONS:
        curr = getCoordInDir(coord, dir)

        # checks if out of bounds!

        if isOutOfBounds(curr, board):
            # Can't move here
            continue

        curr_piece = board[curr.x][curr.y]  # todo

        # if a piece blocks its way, checks if it can jump over
        # this changes curr_x and curr_y to the jump ones
        if (curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE):
            curr = getCoordInDir(curr, dir)  # todo
            if (isOutOfBounds(curr, board) or
                    board[curr.x][curr.y] != EMPTY):
                # Can't jump over piece
                continue

        moves += [curr]  # todo
    return moves


def isOutOfBounds(coord, board):  # todo
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7 or board[x][y] == CORNER:  # todo use static variables
        return True
    return False


# gets the coordinate in the given direction
def getCoordInDir(coord, dir):
    x = coord.x
    y = coord.y

    if dir == LEFT:
        x = x - 1
    elif dir == UP:
        y = y + 1
    elif dir == RIGHT:
        x = x + 1
    elif dir == DOWN:
        y = y - 1

    return Coordinate(x, y)


############## MASSACRE ################

# Init Killable Black Array:
# Get pos of all kill pairs
# Could get pairs of kill spots!
# killable if 2 opposite spaces are open
# For each kill pair:
# While Black array is !empty -> keep running

def killThemAll(board):
    killable = []

    for x in range(BOARD_LEN):
        for y in range(BOARD_LEN):
            if board[x][y] == BLACK_PIECE:
                print("Checking ")
                print(x, y)

                coord = Coordinate(x, y)
                # Checks for kill pairs. Then, adds them to array
                killable += (isKillable(WHITE_PIECE, coord.x, coord.y, board))
                for i in range(len(killable)):
                    findClosestPiece(killable[i][0])
                    findClosestPiece(killable[i][1])


# returns the minigun distance
def getManhattanDistance(start, finish):
    return abs(start.x - finish.x) + abs(start.y - finish.y)


# Checks if a peice is killable and returns the possible kill pairs as
# as an array of tuples
def isKillable(colour, x, y, board):
    killable = []  # todo change signature to coord

    # Checks horizontal pair

    coord = Coordinate(x, y)
    if (isKillSpot(getCoordInDir(coord, LEFT), board, colour) and
            isKillSpot(getCoordInDir(coord, RIGHT), board, colour)):
        # this means killable = [[(2,4),(4,4)],[...]]
        # puts the array in the form [PAIR,PAIR,PAIR]...
        # first pair is accessed through k[0]
        # side of pair is accesssed through k[0][0]
        # x of side of pair is accessed through k[0][0][0]
        killable += [[(getCoordInDir(coord, LEFT)), getCoordInDir(coord, RIGHT)]]

    # checks vertical pair
    if (isKillSpot(getCoordInDir(coord, UP), board, colour) and
            isKillSpot(getCoordInDir(coord, DOWN), board, colour)):
        killable += [[(getCoordInDir(coord, UP)), (getCoordInDir(coord, DOWN))]]
    # print(killable)
    return killable


def isKillSpot(coord, board, colour):
    if isOffBoard((coord.x, coord.y), board):
        return False

    curr = getPieceFromCoord(coord, board)
    return (curr == CORNER or
            curr == colour or
            curr == EMPTY)


def getPieceFromCoord(coord, board):
    return board[coord.x][coord.y]


# finds the closest piece
# loc is a tuple (x,y)
# Basically BFS

# currently get adjacent isn't checking for our pieces
# If we use the closer of the 2
def findClosestPiece(coord):
    # init the visited array to NOT visisted
    visited = []
    for i in range(BOARD_LEN):
        temp_line = []
        for j in range(BOARD_LEN):
            temp_line.append(NOT_VISITED)
        visited.append(temp_line)

    dist = 0
    visited[coord.x][coord.y] = dist

    # init the queue
    q = Queue()
    q.put(coord)

    while not q.empty():  # TODO
        dist += 1
        curr = q.get()
        adj = getAdjacentMoves(curr, board)  # todo
        for i in range(len(adj)):
            next = adj[i]
            if visited[next.x][next.y] == NOT_VISITED:  # if visited - ignore
                q.put(next)
                visited[next.x][next.y] = visited[curr.x][curr.y] + 1
                # visited[adj[i][0]][adj[i][1]] = visited[curr[0]][curr[1]]+1

    printBoard(visited)


def printBoard(board):
    print("Printing out the current board:")
    for i in range(BOARD_LEN):
        print("|", end="")
        for j in range(BOARD_LEN):
            print("{0:3d}".format(board[i][j]), end="")
        print("|")


def isOffBoard(coord, board):  # todo cahnge to otehr
    coord = Coordinate(coord[0], coord[1])
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7 or board[x][y] == CORNER:
        return True
    return False


# Using Heap queues from: https://dbader.org/blog/priority-queues-in-python
def a_star(start, finish):
    Q = []  # init priority queue
    # In the form: Node(coord, g,h)
    curr = Node(start, 0, getManhattanDistance(start, finish))

    visited = init_visited()  # init the visited coordinates
    # push the current node with the f value for the prio q
    heapq.heappush(Q, (curr.f, curr))
    visited[curr.coord.x][curr.coord.y] = curr.f
    closed = []
    # go through all possible adjacent moves

    while len(Q) != 0:
        # get the node with the lowest f value
        curr = heapq.heappop(Q)[1]  # ignorses the prio q value
        curr_coord = curr.coord
        # have we found the end?
        if curr.coord == finish:
            break

        # adding to the closed set

        # check adjacent squares for unvisited coordinates
        adj = getAdjacentMoves(curr.coord, board)
        for next_coord in adj:
            # TODO add constant for +1

            next = Node(next_coord, visited[curr.coord.x][curr.coord.y] + 1, getManhattanDistance(next_coord, finish))
            if (visited[next.coord.x][next.coord.y] == NOT_VISITED or
                    (next.f < visited[next.coord.x][next.coord.y])):  # TODO do I have to compare f values
                # add node to q
                # add coord to visited

                visited[next.coord.x][next.coord.y] = next.f

    printBoard(visited)

    # add node to priority Q w/ value f
    # f = g + h
    # g = dist from prev to here
    # h = dist from here to goal

    # push start to prio Q
    # while Q !empty
    # curr = Q.pop
    # if curr == end:
    # exit
    # get adjacent
    # for each adj:
    # update values:
    # g = curr + distToAdj (1)
    # recalc h from adj to finish
    # recalc f


def init_visited():
    visited = []
    for i in range(BOARD_LEN):
        temp_line = []
        for j in range(BOARD_LEN):
            temp_line.append(NOT_VISITED)
        visited.append(temp_line)
    return visited


############## START PROGRAM ################

# Reads in input
board = []


# s = input()


def initBoard():
    for i in range(BOARD_LEN):
        temp_line = input().split(" ")
        board.append(temp_line)


initBoard()

print(board)
# if move:
# count Moves by Colour

# if (input() = "Moves"):


countMovesByColour(BLACK_PIECE, board)
countMovesByColour(WHITE_PIECE, board)



a_star(Coordinate(3, 3), Coordinate(5, 5))
killThemAll(board)
