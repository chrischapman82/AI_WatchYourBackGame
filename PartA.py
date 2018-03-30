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

NOT_VISITED = 99
BOARD_LEN = 8
MOVE_COST = 1


# Class for coordinates because they're easier like this
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

class Piece:
    def __init__(self, coord, colour):
        self.coord = coord
        self.colour = colour
        self.move_costs = do_bfs(coord)  # creates a map with the given move costs

    def __repr__(self):
        return str(self.coord) + " " + str(self.colour)

class Node:
    def __init__(self, coord, g, h):
        self.coord = coord
        self.g = g
        self.h = h
        self.f = h + g

    def __str__(self):  # For printing
        out = str(self.coord) + ":" + str(self.g) + " " + str(self.h) + " " + str(self.f)
        return out


############## MOVES ################
def countMovesByColour(colour, board):
    count = 0

    for y in range(BOARD_LEN):
        print(board[y])
        for x in range(BOARD_LEN):

            if board[y][x] == colour:
                curr_coord = Coordinate(x, y)  # todo use this for getAdj
                count += len(get_adj_moves(curr_coord, board))
    print(count)


def print_board_state(board):
    for y in range(BOARD_LEN):
        print(board[y])

# Changed so this now returns an array of the adjacent moves
# in form [(x,y),(x2,y2)...]
# Better for part 2 and easy to get count from len!
def get_adj_moves(coord, board):
    count = 0
    moves = []
    #print("base coord:", coord)
    for dir in DIRECTIONS:
        curr = get_coord_in_dir(coord, dir)
        #print(curr)

        # checks if out of bounds!
        if is_out_of_bounds(curr, board) or board[curr.y][curr.x] == CORNER:  # && corner
            # Can't move here
            continue

        curr_piece = board[curr.y][curr.x]  # todo
        #print(curr_piece)
        #print_board(board)
        # if a piece blocks its way, checks if it can jump over
        # this changes curr_x and curr_y to the jump ones
        if curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE:
            curr = get_coord_in_dir(curr, dir)  # todo

            if is_out_of_bounds(curr, board) or board[curr.y][curr.x] != EMPTY:
                # Can't jump over piece
                continue

        moves += [curr]  # todo
        #print("moves")
        #print(moves)
    return moves


# getting the adjacent moves when returning!
# allows a piece to move to where the piece is
def get_adj_moves_returning(coord, board, piece):

    moves = []
    for dir in DIRECTIONS:
        curr = get_coord_in_dir(coord, dir)

        if is_out_of_bounds(curr, board) or board[curr.y][curr.x] == CORNER:
            continue

        curr_piece = board[curr.y][curr.x]
        if curr_piece == WHITE_PIECE or curr_piece == BLACK_PIECE:
            curr = get_coord_in_dir(curr, dir)

            # the only part changed
            if is_out_of_bounds(curr, board) or board[curr.y][curr.x] != EMPTY:
                #print(curr, piece.coord)
                #print(curr.x == piece.coord.x and curr.y == piece.coord.y)
                if not (curr.x == piece.coord.x and curr.y == piece.coord.y):
                    continue

        moves += [curr]
    return moves


def is_out_of_bounds(coord, board):  # todo
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7: # todo use static variables
        return True
    return False


# gets the coordinate in the given direction
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

# Init Killable Black Array:
# Get pos of all kill pairs
# Could get pairs of kill spots!
# killable if 2 opposite spaces are open
# For each kill pair:
# While Black array is !empty -> keep running

def killThemAll(board):

    black_pieces = get_pieces_of_colour(BLACK_PIECE, board)
    while len(black_pieces) != 0:

        # if no killable... return...
        print(len(black_pieces), "black pieces left")
        kill_something(board, black_pieces)
        black_pieces = get_pieces_of_colour(BLACK_PIECE, board)


def kill_something(board, enemy_pieces):
    killable = []

    white_pieces = get_pieces_of_colour(WHITE_PIECE, board)
    black_pieces = enemy_pieces

    # create kill_pair array
    # should be a priority queue,
    # use white_pieces.board[y][x] to get dist to given spot

    print(black_pieces)

    # go through the killable spots
    shortest_moves = []

    print("looping thorugh black pieces")
    for piece in black_pieces:
        print("next black piece", piece.coord)
        # killable is an array of kill pair spots
        # killable += (isKillable(WHITE_PIECE, piece.coord, board))
        killable = isKillable(WHITE_PIECE, piece.coord, board)
        print("killable = ", killable)

        # pair has form [coord1, coord2] OR [coord1]
        arr = []
        for pair in killable:
            print("pair = ", pair)

            # print("closest", get_closest_piece(Coordinate(4,4), white_pieces))
            # print("Getting 2 closest pieces")
            # arr.append(get_closest_2_pieces(pair, white_pieces))
            # print("arr = ", arr)
            white_pieces = get_pieces_of_colour(WHITE_PIECE, board)
            print("returns", get_closest_2_pieces(pair, white_pieces))
            curr = get_closest_2_pieces(pair, white_pieces)

            # store the shortest moves
            if len(shortest_moves) == 0:
                shortest_moves = curr
                #easiest_enemy = piece   # the easiest enemy to kill


            # compares the lengths of the two
            elif curr[0] < shortest_moves[0]:
                shortest_moves = curr
                easiest_enemy = piece
    print("The shortest moves are:")
    print(shortest_moves)
    # shortest_moves[0] is the total dist
    # shortest_moves[1][i][0] is the ith piece, ...[1] is the dest square

    print("here we go")
    print(shortest_moves[1][0][0])
    print(shortest_moves[1][0][1])
    for closest_set in shortest_moves[1]:
        print(closest_set)
        print(closest_set[0])
        print(closest_set[1])
        piece = closest_set[0]
        final_loc = closest_set[1]

        moves = get_moves(piece, final_loc)

        format_print_moves(moves)

        # changing the board to its new state


        update_board(piece.coord, EMPTY, board)     # remove the piece from its old spot
        update_board(final_loc, WHITE_PIECE, board) # add the piece to its new location
        update_board(easiest_enemy.coord, EMPTY, board)
        print_board_state(board)



# print out as specified by the final question
def format_print_moves(moves):
    prev = moves[0]
    for i in range(len(moves)-1):
        curr = moves[i+1]
        #print("(%d, %d) -> (%d, %d)".format(prev.x, prev.y, currx, curr.y))
        out = "(" + str(prev.x) + ", " + str(prev.y) + ") " + "-> "
        out += "(" + str(curr.x) + ", " + str(curr.y) + ")"

        print(out)
        prev = curr


# changes the board, changing the piece at the given coordinate to char
def update_board(coord, char, board):

    board[coord.y][coord.x] = char

def get_moves(piece, dest):
    print("running get moves")
    moves = []
    moves.insert(0, dest) #initial
    curr = dest

    print(piece.coord)
    print(dest)
    while not (curr.x == piece.coord.x and curr.y == piece.coord.y):
        curr_cost = piece.move_costs[curr.y][curr.x]

        adj = get_adj_moves_returning(curr, board, piece)
        #print(adj)
        for i in range(len(adj)):
            nxt = adj[i]
            if piece.move_costs[nxt.y][nxt.x] == curr_cost - 1:  # if visited - ignore
                moves.append(nxt)
                curr = nxt
                continue

    print("moves = ", moves)
    return moves



# gets the total number of moves to get pieces to the given coords
# coords - an array of coordinates. Going to be 2 or 1 for this
# assumes there's at least 1 piece
def get_closest_piece(coord, pieces):
    print("get closest piece!", pieces)
    lo = 1000
    min_piece = None
    #print("get closest pieces", pieces)
    for piece in pieces:
        curr = piece.move_costs[coord.y][coord.x]

        print(piece, curr)
        if curr < lo:
            min_piece = piece
            lo = curr
    print("the closest is:", min_piece);
    return min_piece


def get_closest_2_pieces(target_pair, pieces):
    targets = target_pair   # to save from in place changing
    attacking_pieces = pieces
    tot_dist = 0
    closest_pieces = []
    print("pieces = ", pieces)

    # don't check if the piece is already there!
    for coord in targets:

        if get_piece_from_coord(coord, board) == WHITE_PIECE:
            targets.remove(coord)
            attacking_pieces.remove(get_closest_piece(coord, attacking_pieces))

    print("target_pair =", target_pair)

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




#def get_closest(target_coord):


#def get_killable_pairs():


# Returns an array of the pieces of a given colour

# returns peices of type Piece
def get_pieces_of_colour(colour, board):
    pieces = []
    for x in range(BOARD_LEN):
        for y in range(BOARD_LEN):
            if board[y][x] == colour:
                #print(x, y)
                #print("x,y")
                piece = Piece(Coordinate(x, y), colour)
                pieces.append(piece)
    return pieces


# returns the minigun distance
def getManhattanDistance(start, finish):
    return abs(start.x - finish.x) + abs(start.y - finish.y)


# Checks if a piece is killable and returns the possible kill pairs as
# as an array of tuples
# colour is the colour of the pieces trying to take the given piece
def isKillable(colour, coord, board):
    killable = []

    # Checks horizontal pair

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
        print(curr)
        killable += [curr]

        #killable += [[up, down]]    # add a pair

    #print("killable = ", killable)
    return killable


#[(coord1,coord2),(coord1,coord2)]

def isKillSpot(coord, board, colour):
    if is_off_board(coord):
        return False

    curr = get_piece_from_coord(coord, board)
    return (curr == CORNER or
            curr == colour or
            curr == EMPTY)


def is_off_board(coord):
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7:
        return True
    return False

def get_piece_from_coord(coord, board):
    return board[coord.y][coord.x]


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
    visited[coord.y][coord.x] = dist

    # init the queue
    q = Queue()
    q.put(coord)

    while not q.empty():  # TODO
        dist += 1
        curr = q.get()
        adj = get_adj_moves(curr, board)  # todo
        for i in range(len(adj)):
            next = adj[i]
            if visited[next.y][next.x] == NOT_VISITED:  # if visited - ignore
                q.put(next)
                visited[next.y][next.x] = visited[curr.y][curr.x] + 1
                # visited[adj[i][0]][adj[i][1]] = visited[curr[0]][curr[1]]+1

    print_board(visited)


def do_bfs(coord):
    print()
    print(coord)
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


def print_board(board):
    print("Printing out the current board:")
    for i in range(BOARD_LEN):
        print("|", end="")
        for j in range(BOARD_LEN):
            print("{0:3d}".format(board[i][j]), end="")
        print("|")



def isOffBoard(coord, board):  # todo cahnge to otehr
    x = coord.x
    y = coord.y
    if x < 0 or x > 7 or y < 0 or y > 7 or board[y][x] == CORNER:
        return True
    return False


# Using Heap queues from: https://dbader.org/blog/priority-queues-in-python
'''
def a_star(start, finish):
    Q = []  # init priority queue
    # In the form: Node(coord, g,h)
    curr = Node(start, 0, getManhattanDistance(start, finish))
    print(curr)
    # visited = init_visited()  # init the visited coordinates
    # push the current node with the f value for the prio q

    # init visited array
    visited = []
    for i in range(BOARD_LEN):
        temp_line = []
        for j in range(BOARD_LEN):
            temp_line.append(None)
        visited.append(temp_line)

    heapq.heappush(Q, (curr.g, curr))
    visited[curr.coord.y][curr.coord.x] = curr
    closed = []

    # go through all possible adjacent moves

    while len(Q) != 0:
        # get the node with the lowest f value

        print(curr)
        curr = heapq.heappop(Q)[1]  # ignores the prio q value

        # have we found our goal?
        if curr.coord == finish:
            break

        # adding to the closed set

        # check adjacent squares for unvisited coordinates
        adj = get_adj_moves(curr.coord, board)
        for next_coord in adj:
            # TODO add constant for +1

            nxt = Node(next_coord, curr.g + MOVE_COST, getManhattanDistance(next_coord, finish))
            if (visited[nxt.coord.y][nxt.coord.x] == None or
                    (nxt.g < visited[nxt.coord.y][nxt.coord.x].g)):  # TODO do I have to compare f values
                # add node to q
                # add coord to visited
                heapq.heappush(Q, (nxt.g, nxt))

                visited[nxt.coord.y][nxt.coord.x] = nxt

    printBoardNodes(visited)


def printBoardNodes(board):
    print("Printing out the current board:")
    for i in range(BOARD_LEN):
        print("|", end="")
        for j in range(BOARD_LEN):
            if board[i][j] == None:
                print("-1", end="")
            else:
                print(board[i][j].f, end="")
            # print(board[i][j])
        print("|")

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
'''

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

#a = "X - - - - - - X - - - - - - - - - - - - - 0 0 - - - - - @ 0 - - - - - - - - - - - - - - - 0 - - - - - - @ - @ @ X - - - - - - X"

a = ["X - - - - - - X", "- - - - - - - -", "- - - - - O - -", "- - - - @ O - -", "- - - - - - O -", "- - - - - O @ -", "- - - - - - - @", "X - - - - - - X"]

for i in range(BOARD_LEN):
    temp_line = a[i].split(" ")
    board.append(temp_line)


'''
def initBoard():
    for i in range(BOARD_LEN):
        temp_line = input().split(" ")
        board.append(temp_line)

initBoard()
'''
print(board)
# if move:
# count Moves by Colour

# if (input() = "Moves"):


countMovesByColour(BLACK_PIECE, board)
countMovesByColour(WHITE_PIECE, board)

# a_star(Coordinate(1, 3), Coordinate(7, 5))
killThemAll(board)
