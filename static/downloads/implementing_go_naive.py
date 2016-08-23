from collections import namedtuple
N = 19
NN = N ** 2
WHITE, BLACK, EMPTY = 'O', 'X', '.'

def swap_colors(color):
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK
    else:
        return color

EMPTY_BOARD = EMPTY * NN

def flatten(c):
    return N * c[0] + c[1]

# Convention: coords that have been flattened have a "f" prefix
def unflatten(fc):
    return divmod(fc, N)

def is_on_board(c):
    return c[0] % N == c[0] and c[1] % N == c[1]

def get_valid_neighbors(fc):
    x, y = unflatten(fc)
    possible_neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
    return [flatten(n) for n in possible_neighbors if is_on_board(n)]

# Neighbors are indexed by flat coordinates
NEIGHBORS = [get_valid_neighbors(fc) for fc in range(NN)]

def unpack_bools(bool_array):
    return [i for i, b in enumerate(bool_array) if b]

def find_reached(board, fc):
    color = board[fc]
    chain = [False] * NN; chain[fc] = True
    reached = set()
    frontier = [fc]
    while frontier:
        current_fc = frontier.pop()
        chain[current_fc] = True
        for fn in NEIGHBORS[current_fc]:
            if board[fn] == color and not chain[fn]:
                frontier.append(fn)
            elif board[fn] != color:
                reached.add(board[fn])
    return unpack_bools(chain), reached

class IllegalMove(Exception): pass

def place_stone(color, board, fc):
    return board[:fc] + color + board[fc+1:]

def bulk_place_stones(color, board, stones):
    byteboard = bytearray(board) # create mutable version of board
    for fstone in stones:
        byteboard[fstone] = color
    return str(byteboard) # and cast back to string when done

def maybe_capture_stones(board, fc):
    chain, reached = find_reached(board, fc)
    if not EMPTY in reached:
        board = bulk_place_stones(EMPTY, board, chain)
        return board, chain
    else:
        return board, []

def play_move_incomplete(board, fc, color):
    if board[fc] != EMPTY:
        raise IllegalMove
    board = place_stone(color, board, fc)

    opp_color = swap_colors(color)
    opp_stones = []
    my_stones = []
    for fn in NEIGHBORS[fc]:
        if board[fn] == color:
            my_stones.append(fn)
        elif board[fn] == opp_color:
            opp_stones.append(fn)

    for fs in opp_stones:
        board, _ = maybe_capture_stones(board, fs)

    for fs in my_stones:
        board, _ = maybe_capture_stones(board, fs)

    return board


def is_koish(board, fc):
    'Check if fc is surrounded on all sides by 1 color, and return that color'
    if board[fc] != EMPTY: return None
    neighbor_colors = {board[fn] for fn in NEIGHBORS[fc]}
    if len(neighbor_colors) == 1 and not EMPTY in neighbor_colors:
        return list(neighbor_colors)[0]
    else:
        return None

class Position(namedtuple('Position', ['board', 'ko'])):
    @staticmethod
    def initial_state():
        return Position(board=EMPTY_BOARD, ko=None)

    def __str__(self):
        import textwrap
        return '\n'.join(textwrap.wrap(self.board, N))
    
    def play_move(self, fc, color):
        board, ko = self
        if fc == ko or board[fc] != EMPTY:
            raise IllegalMove

        possible_ko_color = is_koish(board, fc)
        new_board = place_stone(color, board, fc)

        opp_color = swap_colors(color)
        opp_stones = []
        my_stones = []
        for fn in NEIGHBORS[fc]:
            if new_board[fn] == color:
                my_stones.append(fn)
            elif new_board[fn] == opp_color:
                opp_stones.append(fn)

        opp_captured = 0
        for fs in opp_stones:
            new_board, captured = maybe_capture_stones(new_board, fs)
            opp_captured += len(captured)

        for fs in my_stones:
            new_board, captured = maybe_capture_stones(new_board, fs)

        if opp_captured == 1 and possible_ko_color == opp_color:
            new_ko = fc
        else:
            new_ko = None

        return Position(new_board, new_ko)

    def score(self):
        board = self.board
        while EMPTY in board:
            fempty = board.index(EMPTY)
            empties, border_colors = find_reached(board, fempty)
            if len(border_colors) == 1:
                border_color = list(border_colors)[0]
                board = bulk_place_stones(border_color, board, empties)
            else:
                # if an empty intersection reaches both white and black,
                # then it belongs to neither player. 
                board = bulk_place_stones('?', board, empties)
        return board.count(BLACK) - board.count(WHITE)
