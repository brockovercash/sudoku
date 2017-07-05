import copy


def sectionCoordinates(i, j):
    """Generate the top-left coords of the section of the puzzle i,j is in"""
    return 3 * (i//3), 3 * (j//3)


def isValid(puzzle, i, j, e):
    """Determine if a number is valid in a given cell

    Check row, column, and section for the number in that order. If an number
    exists in the row, column, or section, return false. Otherwise, return true
    """
    rowValid = all([e != puzzle[i][x] for x in range(9)])
    if rowValid:
        columnValid = all([e != puzzle[x][j] for x in range(9)])
        if columnValid:
            secStartX, secStartY = sectionCoordinates(i, j)
            for x in range(secStartX, secStartX+3):
                for y in range(secStartY, secStartY+3):
                    if puzzle[x][y] == e:
                        return False
            return True
    return False


def validCellInputs(puzzle, i, j):
    """Give all possible inputs for a cell in the grid

    No valid inputs exist if there is an existing input. If empty, check
    existing row, column, and section inputs.
    """
    if puzzle[i][j] != 0:
        return []
    else:
        valid = []
        for e in range(1, 10):
            if isValid(puzzle, i, j, e):
                valid.append(e)
        return valid


def generateHintMatrix(puzzle):
    """Turn an input grid into a matrix of valid cell inputs

    This is used by the print methods to produce the hints
    """
    hints = copy.deepcopy(puzzle)
    for i in range(0, 9):
        for j in range(0, 9):
            hints[i][j] = validCellInputs(puzzle, i, j)
    return hints


def printCounts(puzzle):
    """Prints the count of each number written in the input

    0 represents a blank cell.
    """
    counts = [0] * 10
    for i in range(9):
        for j in range(9):
            counts[puzzle[i][j]] += 1
    for e in range(10):
        if counts[e] == 9:
            counts[e] = ' '
        print(e, ': ', counts[e], sep='')


def printCountValidInputs(hints):
    """Prints a count of all valid inputs to a cell

    Useful because 1 represents that there is only one value that can be put
    into that location.
    """
    for i in range(0, 9):
        if i != 0 and i % 3 == 0:
            print((6 * '_') + '|' + (7 * '_') + '|' + (6 * '_'))
        for j in range(0, 9):
            print(len(hints[i][j]), end=' ')
            if j != 8 and (j + 1) % 3 == 0:
                print('| ', end='')
        print('')


def printValidInputs(hints):
    """Prints all valid inputs to a cell

    Useful to look across rows, columns, and sections to see whether there are
    certain inputs that aren't constrained by validity, but are the only
    location in their row/column/section where a number is possible.
    """
    for i in range(0, 9):
        if i != 0 and i % 3 == 0:
            print(150 * '_')
        for j in range(0, 9):
            print(hints[i][j], ((14 - len(str(hints[i][j]))) * ' '), end='')
            if j != 8 and (j + 1) % 3 == 0:
                print('|    ', end='')
        print('')


def isRowSingular(hints, i, e):
    """Check if a row contains only one cell that is valid for e"""
    count = 0
    for j in range(9):
        count += hints[i][j].count(e)
    return count == 1


def isColSingular(hints, j, e):
    """Check if a column contains only one cell that is valid for e"""
    count = 0
    for i in range(9):
        count += hints[i][j].count(e)
    return count == 1


def isSectionSingular(hints, i, j, e):
    """Check if a section contains only one cell that is valid for e"""
    count = 0
    secTopX, secTopY = 3 * (i//3), 3 * (j//3)
    for x in range(secTopX, secTopX+3):
        for y in range(secTopY, secTopY+3):
            count += hints[x][y].count(e)
    return count == 1


def hasSingular(hints, i, j):
    """Check if a column contains only one cell that is valid for e"""
    return any([isRowSingular(hints, i, e) or
                isColSingular(hints, j, e) or
                isSectionSingular(hints, i, j, e) for e in hints[i][j]])


def printSingles(hints):
    """Prints if a cell has a row/column/section constrained choice.

    Useful when there are no cells with only one valid input. Highlights rows,
    columns, and sections where certain inputs that aren't constrained by
    validity, but the cell is only location in their row/column/section where a
    number is possible.
    """
    for i in range(0, 9):
        if i != 0 and i % 3 == 0:
            print((6 * '_') + '|' + (7 * '_') + '|' + (6 * '_'))
        for j in range(0, 9):
            if hasSingular(hints, i, j):
                print(1, end=' ')
            else:
                print(0, end=' ')
            if j != 8 and (j + 1) % 3 == 0:
                print('| ', end='')
        print('')


# 'Very difficult' puzzle generated on 7 Sudoku
# http://www.7sudoku.com/view-puzzle?date=20170701
puzzle = [[0, 6, 0, 0, 9, 3, 4, 0, 0],
          [1, 0, 3, 8, 7, 0, 9, 0, 0],
          [0, 4, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 5, 0, 0, 0, 0, 3],
          [0, 7, 0, 2, 0, 6, 0, 9, 0],
          [3, 0, 0, 0, 0, 8, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 2, 0],
          [0, 0, 6, 0, 5, 1, 8, 0, 9],
          [0, 0, 1, 3, 8, 0, 0, 5, 0]]

# Intermediate representation needed for printing hints
hints = generateHintMatrix(puzzle)

# When solving a puzzle, start with all hints commented out and bring them
# in as needed.

# Prints the counts of each number already in the puzzle. This lets you see
# which numbers might make a good place to start looking and helps you keep
# track of your progress.
printCounts(puzzle)
print()

# Prints the number of valid inputs per cell. If 0, an input exists in this
# cell or you have messed up somewhere. If 1, there is only one valid option.
# If there are 2 or more, you may need to do some more work or look deeper.
printCountValidInputs(hints)
print()

# Prints all valid inputs for each cell. Helpful if you can't figure out why
# only one input is valid or to look across cels/rows/columns
printValidInputs(hints)
print()

# Prints a 1 when a cell contains a valid input that is unique to its row,
# column, or section. This is useful when all cells have 2+ valid inputs.
printSingles(hints)
