# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: In short, for a given sudoku problem, the naked twins strategy adds an additional constraint on the possible permutations of values _boxes_ within a single _unit_ that are allowed. If there are two or more _boxes_ inside a _unit_ that satisfy the following criteria, we have a set of naked twins:

  1. No more than two (2) values are possible inside the _box_
  2. At least two _boxes_ have the same possible values

We can interpret this as _if there is at least one set of naked twins inside a given unit, no other boxes in this unit can take on the values the naked twins allow._ This means that we can propagate which values are allowed inside every unit by eliminating the values any pair of naked twins allow from all other boxes inside the same unit. If we iterate this procedure over all units, we've (likely) reduced the number of possible permutations of values for each _box_ inside the entire sudoku grid. In other words, we've decreased the set of possible paths that a solver could follow in search for a solution to the sudoku.

In bullet form, the technique could look as follows:

  1. Pick a _unit_
    1. For each _box_ in _unit_
      1. Find all _boxes_ with exactly _two_ possible values
    2. For each 'two-valued' _box_
      1. Find all sets _boxes_ with the same _two_ possible values
    3. For each possible 'twin value' in the set of twins
      1. Check if any _box_ in _unit_ has more than _two_ possible values **and** if one of these is the same as the 'twin value'
        1. Remove the 'twin value' from these _boxes_

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: A diagonal sudoku imposes additional restrictions on the allowed permutations of values for a given box through two new _units_. These two new restrictions, or constraints, are the two diagonals of the sudoku grid:

  1. `[['A1','B2', 'C3', 'D4','E5','F6', 'G7', 'H8', 'I9']]`
  2. `[['A9', 'B8', 'C7', 'D6','E5', 'F4', 'G3', 'H2', 'I1']]`.

In order to account for these added constraints, all we need to do is to update the number of _units_ that we iterate over as we eliminate possible values for every _box_ inside each unit.

These diagonal constraints also alter the number of _peers_ for each of the _boxes_ that reside along each of the diagonals. For example, _box_ `I9` has another 6 _peers_ (`G7` and `H8` are already accounted for) for a diagonal solution, as does `A9` and so on. Note that _box_ `E5` resides along both diagonals, and will need to be compared to another 12 _peers_ as the solver tries to eliminate possible values from each box in the grid.

Because `eliminate()` iterates over the possible _peers_ for each _box_ and `only_choice()` and `naked_twins()` over each _unit_, it is sufficient for us to simply add these new diagonal constraints to the total number of _units_ and their impact on the number of _peers_ for each unique _box_ in order to leverage constraint propagation. Please see `sudoku_utils.py` and `solution.py` for more details on the implementation.

### Data and Notes

The data consists of a text file of diagonal sudokus for you to solve.

> **Note 1:** This does not seem to be the case. I cannot find any text file with diagonal sudokus to try my solver on. I went ahead and downloaded a series of 'hard' sudokus from Project Euler `./sudokus/hard_sudokus.txt` and ran some tests on those. They're not diagonal, but the solver seemed to work for them.

> **Note 2:** I've changed the `main()` method of `solution.py` so that the user can decide whether to visualize a solution path, and I've run the solver on a number of 'hard' sudokus to look at the performance of the implementations. Notably, naked_twins improved the solution speed on average from 0.8 seconds per sudoku, down to 0.5 seconds. An improvement of 37.5%.
