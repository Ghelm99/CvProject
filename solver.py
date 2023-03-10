################ SUDOKU SOLVER ################

# The code takes as input a 2D array representing a partially filled
# sudoku board with zeros representing empty cells. 
# It implements a backtracking (brute force) algorithm 
# to solve the sudoku using recursion. 

# function that solves the sudoku
def solve(board):
    # retrieve the first empty cell
    empty_cell = find_empty(board)
    # if there's not an empty cell the board is solved
    if not empty_cell:
        return True
    else:
        row, col = empty_cell
    for i in range(1,10):
        # check if the number is valid calling valid()
        if valid(board, i, (row, col)):
            board[row][col] = i
            # the function calls itself with the updated board 
            # if the recursion returns True the sudoku is solved,
            # otherwise it backtracks by assigning zero to the current cell
            # and tries next number
            if solve(board):
                return True
            board[row][col] = 0
    return False

# function that checks if the given number is valid in the given position
def valid(board, num, pos):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        # check columns
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    # check box
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

# function that finds an empty cell in the board
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  
    return None