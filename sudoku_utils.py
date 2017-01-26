# Utility functions from class quizzes
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

# Basic sudoku grid
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

# Row, column and 3x3 square helper lists
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Helpers for all rows, cols and squares where values must be unique
unitlist = row_units + col_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

# Utilities for diagonal sudokus
first_diag = [['A1','B2', 'C3', 'D4','E5','F6', 'G7', 'H8', 'I9']]
second_diag = [['A9', 'B8', 'C7', 'D6','E5', 'F4', 'G3', 'H2', 'I1']]
diag_unitlist = row_units + col_units + square_units + first_diag + second_diag
diag_units = dict((s, [u for u in diag_unitlist if s in u]) for s in boxes)
diag_peers = dict((s, set(sum(diag_units[s], [])) - set([s])) for s in boxes)

# Functions
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1 + max(len(values[s]) for s in boxes) # Set maximum width of unit
    line = '+'.join(['-'*(width*3)]*3) # Create grid lines
    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '')
                    for c in cols))
        if r in 'CF':
            print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    vals = []
    digits = '123456789'
    for val in grid:
        if val == '.':
            vals.append(digits)
        else:
            vals.append(val)
    assert len(vals) == 81
    return dict(zip(boxes, vals))
