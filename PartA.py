from queue import *
import heapq

# sample input
#a = "X - - - - - - X - - - - - - - - - - - - - 0 0 - - - - - @ 0 - - - - - - - - - - - - - - - 0 - - - - - - @ - @ @ X - - - - - - X"

# BOARD SYMBOLS
EMPTY = "-"
CORNER = "X"
WHITE_PIECE = "O"
BLACK_PIECE = "@"

# PART NAME
MOVES = "Moves"
MASSACRE = "Massacre"

# DIRECTION CONSTANT
DIRECTIONS = [0, 1, 2, 3]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# CONSTANTS
MAX_COST = 1000
NOT_VISITED = 99
BOARD_LEN = 8
MOVE_COST = 1


# Class for coordinates containing an x and y value
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):  # For printing
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __repr__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __eq__(self, coord):
        return self.x == coord.x and self.y == coord.y

    def __ne__(self, coord):
        return not self.__eq__(self, coord)


# Class piece: contains information about a piece, including the cost to move from its current position to another
class Piece:
    def __init__(self, coord, colour):
        self.coord = coord
        self.colour = colour
        self.move_costs = do_bfs(coord)  # creates a map with the given move costs

    def __repr__(self):
        return str(self.coord) + " " + str(self.colour)


############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for y in range(BOARD_LEN):
        for x in range(BOARD_LEN):

            if board[y][x] == colour:
                curr_coord = Coordinate(x, y)  # todo use this for getAdj
                count += len(get_adj_moves(curr_coord, board))
    print(count)


# for testing, prints the current board state
def print_board_state(board):
    for y in range(BOARD_LEN):
        print(board[y])

# Returns an array of moves adjacent to a given coordinate (coord) based on the given board state
def get_adj_moves(coord, board):

    moves = []

    # iterates throgh all the directions
    for dir in DIRECTIONS:
        curr = get_coord_in_dir(coord, dir)

        # checks if out of bounds!
        if is_out_of_bounds(curr, board) or board[curr.y][curr.x] == CORNER:  # && corner
            # Can't move here
            continue

        curr_piece = board[curr.y][curr.x]  # todo
        # if a piece blocks its way, checks if it can jump over
        # this changes curr_x and curr_y to the jump ones

        if curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE:
            curr = get_coord_in_dir(curr, dir)  # todo

            if is_out_of_bounds(curr, board) or board[curr.y][curr.x] != EMPTY:
                # Can't jump over piece
                continue

        moves += [curr]  # todo
    return moves


# Very similar ot adj moves, but counts the coordinate of the peice as adjacent!
# Used for getting the moves from bfs
def get_adj_moves_returning(coord, board, piece):

    moves = []
    for dir in DIRECTIONS:
        curr = get_coord_in_dir(coord, dir)

        if is_out_of_bounds(curr, board) or board[curr.y][curr.x] == CORNER:
            continue

        if curr.x == piece.coord.x and curr.y == piece.coord.y:
            moves += [curr]
            continue

        curr_piece = board[curr.y][curr.x]
        if curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE:
            curr = get_coord_in_dir(curr, dir)


            # the only part changed
            if is_out_of_bounds(curr, board) or board[curr.y][curr.x] != EMPTY:
                if not (curr.x == piece.coord.x and curr.y == piece.coord.y):
                    continue

        moves += [curr]
    return moves


# returns true if the given coordinate is in the bounds of the map
# otherwise, false
def is_out_of_bounds(coord,board):  # todo
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7:
        return True
    return False


# returns the coordinate in the given direction from coord
def get_coord_in_dir(coord, dir):
    x = coord.x
    y = coord.y

    if dir == LEFT:
        x = x - 1
    elif dir == UP:
        y = y - 1
    elif dir == RIGHT:
        x = x + 1
    elif dir == DOWN:
        y = y + 1

    return Coordinate(x, y)


############## MASSACRE ################


# main function for massacre:
# kills all the enemies
def killThemAll(board):

    black_pieces = get_pieces_of_colour(BLACK_PIECE, board)
    while len(black_pieces) != 0:

        # if no killable... return...
        kill_something(board, black_pieces)
        black_pieces = get_pieces_of_colour(BLACK_PIECE, board)


# kills the closest enemy.
def kill_something(board, enemy_pieces):

    black_pieces = enemy_pieces # an array of enemy pieces
    shortest_moves = []         # contains the shortest moves

    for piece in black_pieces:
        # killable is an array of kill pair spots
        killable = isKillable(WHITE_PIECE, piece.coord, board)

        # for each of the pairs around an enemy, check if one of these require the least amount of
        # moves ot get to
        for pair in killable:
            white_pieces = get_pieces_of_colour(WHITE_PIECE, board)
            curr = get_closest_2_pieces(pair, white_pieces)

            # store the shortest moves
            if len(shortest_moves) == 0:
                shortest_moves = curr
                easiest_enemy = piece   # the easiest enemy to kill


            # compares the lengths of the two
            elif curr[0] < shortest_moves[0]:
                shortest_moves = curr
                easiest_enemy = piece

    # for the closest moves, move towards them!
    for closest_set in shortest_moves[1]:
        piece = closest_set[0]
        final_loc = closest_set[1]

        moves = get_moves(piece, final_loc)

        # adding to the final output
        format_print_moves(moves)

        # changing the board to its new state
        update_board(piece.coord, EMPTY, board)     # remove the piece from its old spot
        update_board(final_loc, WHITE_PIECE, board) # add the piece to its new location
        update_board(easiest_enemy.coord, EMPTY, board)


# print out as specified by the final question
def format_print_moves(moves):
    prev = moves[0]
    for i in range(len(moves)-1):
        curr = moves[i+1]
        out = "(" + str(curr.x) + ", " + str(curr.y) + ") " + "-> "
        out += "(" + str(prev.x) + ", " + str(prev.y) + ")"

        print(out)
        prev = curr


# changes the board, changing the piece at the given coordinate to char
def update_board(coord, char, board):

    board[coord.y][coord.x] = char

# retraces the pieces move cost chart in order to get the shortest path from piece.coord to
# the destination (dest)
def get_moves(piece, dest):
    moves = []
    moves.insert(0, dest) #initial
    curr = dest
    while not (curr.x == piece.coord.x and curr.y == piece.coord.y):
        curr_cost = piece.move_costs[curr.y][curr.x]

        adj = get_adj_moves_returning(curr, board, piece)
        for i in range(len(adj)):
            nxt = adj[i]
            if piece.move_costs[nxt.y][nxt.x] == curr_cost - 1:  # if visited - ignore
                moves.append(nxt)
                curr = nxt
                break
    return moves


# gets the total number of moves to get pieces to the given coords
# coords - an array of coordinates. Going to be 2 or 1 for this
# assumes there's at least 1 piece
def get_closest_piece(coord, pieces):
    lo = 1000
    min_piece = None
    for piece in pieces:
        curr = piece.move_costs[coord.y][coord.x]
        if curr < lo:
            min_piece = piece
            lo = curr
    return min_piece


# gets all the shortest pieces
# returns the closest pieces to a given pair, and the total distance to get to the square
def get_closest_2_pieces(target_pair, pieces):
    targets = target_pair   # to save from in place changing
    attacking_pieces = pieces
    tot_dist = 0
    closest_pieces = []

    # don't check if the piece is already there!#
    for coord in targets:

        # if a piece is already there, remove from candidates to move to pair
        if get_piece_from_coord(coord, board) == WHITE_PIECE:
            targets.remove(coord)
            attacking_pieces.remove(get_closest_piece(coord, attacking_pieces))

    # goes through array targets, getting the closest 2 pieces to the given location
    for coord in targets:
        piece = get_closest_piece(coord, attacking_pieces)        #

        # keeps getting available pieces that haven't been mentioned before
        while piece in closest_pieces:

            # can it be a case where it doesn't exist
            attacking_pieces.remove(piece)
            piece = get_closest_piece(coord, attacking_pieces)

        tot_dist += piece.move_costs[coord.y][coord.x]
        closest_pieces.append([piece, coord])
    return [tot_dist, closest_pieces]



# Returns an array of the pieces of a given colour

# returns peices of type Piece
def get_pieces_of_colour(colour, board):
    pieces = []
    for x in range(BOARD_LEN):
        for y in range(BOARD_LEN):
            if board[y][x] == colour:
                piece = Piece(Coordinate(x, y), colour)
                pieces.append(piece)
    return pieces


# returns the manhattan distance. The heuristic we chose to use
def getManhattanDistance(start, finish):
    return abs(start.x - finish.x) + abs(start.y - finish.y)


# Checks if a piece is killable and returns the possible kill pairs as
# as an array of tuples
# colour is the colour of the pieces trying to take the given piece
def isKillable(colour, coord, board):
    killable = []

    # the characters at the given spot
    left = get_coord_in_dir(coord, LEFT)
    right = get_coord_in_dir(coord, RIGHT)
    up = get_coord_in_dir(coord, UP)
    down = get_coord_in_dir(coord, DOWN)

    if (isKillSpot(left, board, colour) and
            isKillSpot(right, board, colour)):
        curr = []
        if get_piece_from_coord(left, board) != CORNER:
            curr += [left]

        if get_piece_from_coord(right, board) != CORNER:
            curr += [right]

        killable += [curr] # add a pair

    # checks vertical pair

    if (isKillSpot(up, board, colour) and
            isKillSpot(down, board, colour)):
        curr = []

        if get_piece_from_coord(up, board) != CORNER:
            curr += [up]

        if get_piece_from_coord(down, board) != CORNER:
            curr += [down]
        killable += [curr]
    return killable


# checks if the given coordinate can lead to, or help in the death of an enemy
def isKillSpot(coord, board, colour):
    if is_off_board(coord):
        return False

    curr = get_piece_from_coord(coord, board)
    return (curr == CORNER or
            curr == colour or
            curr == EMPTY)


# checks if the given coordinate is off the board
def is_off_board(coord):
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7:
        return True
    return False

# helper fn
# gets the piece at the given coordinate of board
def get_piece_from_coord(coord, board):
    return board[coord.y][coord.x]

# performs bfs, storing all the distances in the board
def do_bfs(coord):
    visited = init_visited()
    dist = 0
    visited[coord.y][coord.x] = dist

    q = Queue()
    q.put(coord)

    while not q.empty():
        dist += 1
        curr = q.get()
        adj = get_adj_moves(curr, board)
        for i in range(len(adj)):
            nxt = adj[i]
            if visited[nxt.y][nxt.x] == NOT_VISITED:  # if visited - ignore
                q.put(nxt)
                visited[nxt.y][nxt.x] = visited[curr.y][curr.x] + MOVE_COST

    #print_board(visited) #remove to stop printing
    return visited


# prints the bboard for checking
def print_board(board):
    print("Printing out the current board:")
    for i in range(BOARD_LEN):
        print("|", end="")
        for j in range(BOARD_LEN):
            print("{0:3d}".format(board[i][j]), end="")
        print("|")


# checks if off the baord, includes corners
def isOffBoard(coord, board):
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7 or board[y][x] == CORNER:
        return True
    return False


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

# for initialising the board
def init_board(board):
    for i in range(BOARD_LEN):
        temp_line = input().split(" ")
        board.append(temp_line)


board = []
init_board(board)
instruction = input()
if instruction == MOVES:
    countMovesByColour(WHITE_PIECE, board)
    countMovesByColour(BLACK_PIECE, board)
elif instruction == MASSACRE:
    killThemAll(board)



