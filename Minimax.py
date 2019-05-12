from math import inf as infinity
from random import choice

HUMAN = -1
COMPUTER = 1

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def print_board(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
         0: '-'
    }
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(" " + symbol + " ", end='')
        print('\n')


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],

        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],

        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def evaluate_state(state):
    if wins(state, COMPUTER):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score


def game_over(state):
    return wins(state, HUMAN) or wins(state, COMPUTER) or is_full()


def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def is_full():
    depth = len(empty_cells(board))
    if depth == 0:
        return True
    return False


def is_valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if is_valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def min_max(state, depth, player):
    if player == COMPUTER:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if game_over(state):
        score = evaluate_state(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = min_max(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def ai_turn(c_choice, h_choice):
    if game_over(board):
        return

    print("Computer Turn")
    print_board(board, c_choice, h_choice)

    if len(empty_cells(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = min_max(board, len(empty_cells(board)), COMPUTER)
        x, y = move[0], move[1]

    set_move(x, y, COMPUTER)


def human_turn(c_choice, h_choice):
    if game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    print("Human Turn")
    print_board(board, c_choice, h_choice)

    while move < 1 or move > 9:
        move = int(input('Use numpad (1..9): '))
        coord = moves[move]
        can_move = set_move(coord[0], coord[1], HUMAN)
        if not can_move:
            print('Bad move')
            move = -1


def main():
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    while h_choice != 'O' and h_choice != 'X':
        print('')
        h_choice = input('Choose X or O\nChosen: ').upper()

    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    while first != 'Y' and first != 'N':
        first = input('First to start?[y/n]: ').upper()

    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    if wins(board, HUMAN):
        print("Human Turn")
        print_board(board, c_choice, h_choice)
        print('YOU WIN!')

    elif wins(board, COMPUTER):
        print("Computer Turn")
        print_board(board, c_choice, h_choice)
        print("YOU LOSE!")

    else:
        print_board(board, c_choice, h_choice)
        print("DRAW!")

    exit()


main()
