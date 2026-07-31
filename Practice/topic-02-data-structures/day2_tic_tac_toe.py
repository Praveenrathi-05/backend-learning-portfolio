# Topic 2, Day 2 Homework
# Nested lists + slicing practice using a tic-tac-toe board

board = [
    ["O", "X", " "],
    ["O", " ", "X"],
    ["X", "O", " "]
]

print(board[1])       # middle row
print(board[1][1])    # center square (row 1, column 1)
print(board[0:2])     # first two rows via slicing
