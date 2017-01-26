from sudoku_utils import *

# Game path
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values, is_diag=True):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        is_diag(bool): whether the sudoku is diagonal or not. Default is True.
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # If diag sudoku, set which unitlist
    u_list = []
    if is_diag:
        u_list = diag_unitlist
    else:
        u_list = unitlist

    # Loop through all units
    for unit in u_list:
        # Operate on actual values, as these are the ones we compare inside units
        unit_vals = [values[box] for box in unit]

        # Only look for twins among boxes with two possibilities
        double_vals = [vals for vals in unit_vals if len(vals) == 2]

        # Skip to next unit if no possible twins exist
        if len(double_vals) < 2:
            continue

        # Find all twins in unit
        twins = set([val for val in double_vals if double_vals.count(val) > 1])

        # Loop over possible values for each set of twins in unit
        for vals in list(twins):
            for val in vals:
                for box in unit:
                    # Only alter the sudoku board for boxes with more than 2 possible values and that contains the potential value
                    if len(values[box]) > 2 and val in values[box]:
                        assign_value(values, box, values[box].replace(val, ''))

    return values

def eliminate(values, is_diag=True):
    """Loop through all boxes and eliminate values from a box's peers when it is a single number.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the resulting remaining values for all boxes.
    """
    p_dict = {}
    if is_diag:
        p_dict = diag_peers
    else:
        p_dict = peers

    # Find all boxes with singular values
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]

    # Loop through the peers of all solved boxes and remove the solved box value from them
    for box in solved_boxes:
        for peer in p_dict[box]:
            assign_value(values, peer, values[peer].replace(values[box], ''))

    return values

def only_choice(values, is_diag=True):
    """Loop through all boxes and determine if any value can exist inside only one box for any given unit of boxes, e.g. perform the 'only choice' algorithm
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        is_diag(bool): whether the sudoku is diagonal or not. Default is True.
    Returns:
        the values dictionary after perfoming the only choice algorithm.
    """
    u_list = []
    if is_diag:
        u_list = diag_unitlist
    else:
        u_list = unitlist

    # Find all boxes with multiple possible values for each unit
    for unit in u_list:
        for val in cols:
            many_possibs = [box for box in unit if val in values[box]]

            # If only one value is possible, remove all other values in said box
            if len(many_possibs) == 1:
                assign_value(values, many_possibs[0], val)

    return values

def reduce_puzzle(values, is_diag=True):
    """Tries to reduce a sudoku puzzle using the eliminate and only choice algorithms.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        is_diag(bool): whether the sudoku is diagonal or not. Default is True.
    Returns:
        the reduced sudoku values dictionary.
    """

    final_vals = [box for box in values.keys() if len(values[box]) == 1]
    stuck = False

    while not stuck:
        # Check how many boxes have a determined value
        final_vals_pre = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the eliminate strategy
        values = eliminate(values, is_diag)

        # Use the only choice strategy
        values = only_choice(values, is_diag)

        # Use the naked twins strategy
        values = naked_twins(values, is_diag)

        # Check how many boxes have a determined value, to compare
        final_vals_post = len([box for box in values.keys() if len(values[box]) == 1])

        # If final_vals_post == 81 --> solved sudoku, break out of loop
        if final_vals_post == 81:
            break

        # If no new values were added, stop the loop.
        stuck = final_vals_pre == final_vals_post

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def solve(grid, is_diag=True):
    """Tries to solve a sudoku board.
    Args:
        grid(string): a string that represents the sudoku, e.g. '..2143...46...'
        is_diag(bool): whether the sudoku is diagonal or not. Default is True.
    Returns:
        the solved sudoku, if possible in the same format as values input.
    """
    values = grid_values(grid) # Turn sudoku string into dict
    values = search(values, is_diag)

    return values


def search(values, is_diag=True):
    """Apply depth-first search to look for possible solutions to a sudoku.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        is_diag(bool): whether the sudoku is diagonal or not. Default is True.
    Returns:
        the solved sudoku, if possible. Otherwise it returns false.
    """

    # Reduce puzzle
    values = reduce_puzzle(values, is_diag)

    # Check if successful or not
    if values is False:
        return False # Failure
    if all(len(values[box]) == 1 for box in boxes):
        return values # Success

    # Find a box with the fewest number of possible values > 1
    # Note: does not matter if '19' or '91' is chosen.
    _, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Recursively loop through sudoku to search for solutions
    for val in values[box]:
        # Copy to avoid changing original until we know if a path leads to a solution
        new_sudoku = values.copy()

        # Assign the first of the possible values for the given box
        assign_value(new_sudoku, box, val)

        # Try to solve the remaining sudoku
        attempt_path = search(new_sudoku, is_diag)
        if attempt_path:
            return attempt_path

if __name__ == '__main__':
    from time import time
    from statistics import mean

    # For fun, let's check how long it takes to solve some 'crazy' difficult sudoku problems from Project Euler.
    start = time()
    time_list = []
    with open('./sudokus/hard_sudokus.txt', 'rb') as sudokus:
        for sudoku in sudokus:
            assignments = [] # Flush assignments after each sudoku
            sudoku = sudoku.decode('utf-8').replace('\n','') # Decode byte

            # Time each solution
            tmp_time = time()
            solve(sudoku, is_diag=False)

            # Append time to time list
            time_list.append(time() - tmp_time)
    end = time() - start
    print('Time to solve 95 \'hard sudokus\': %.2f' % end, 'seconds')
    print('Average time to solve each puzzle: %.2f' % mean(time_list), 'seconds')

    # Original code
    # assignments = [] # Ensure that no previous paths hang around
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(solve(diag_sudoku_grid))

    # Allow user to decide whether to visualize solution path
    print('Visualize solution? (y/n):')
    viz = input()
    if viz == 'y':
        try:
            from visualize import visualize_assignments
            visualize_assignments(assignments)
        except:
            print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    else:
        import sys
        sys.exit()
