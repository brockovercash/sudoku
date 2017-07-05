import copy

def printCounts(grid):
  counts = [0] * 10
  for i in range(9):
    for j in range(9):
      counts[grid[i][j]] += 1
  for e in range(10):
    if counts[e] == 9:
      counts[e] = ' '
    print(e, ': ', counts[e], sep="")


def isRowSingular(grid, i, e):
  count = 0
  for j in range(9):
    count += grid[i][j].count(e)
  return count == 1


def isColSingular(grid, j, e):
  count = 0
  for i in range(9):
    count += grid[i][j].count(e)
  return count == 1


def isBoxSingular(grid, i, j, e):
  count = 0
  secTopX, secTopY = 3 *(i//3), 3 *(j//3)
  for x in range(secTopX, secTopX+3):
      for y in range(secTopY, secTopY+3):
          count += grid[x][y].count(e)
  return count == 1


def hasSingular(grid, i, j):
  return any([isRowSingular(grid,i,e) or isColSingular(grid,j,e) or isBoxSingular(grid,i,j,e) for e in grid[i][j]])


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 *(i//3), 3 *(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False
            return True
    return False

def solve(grid):
  output = copy.deepcopy(grid)
  for i in range(0 , 9):
    for j in range(0, 9):
      if grid[i][j] != 0:
        output[i][j] = []
      else:
        valid = []
        for e in range(1,10):
          if isValid(grid,i,j,e):
            valid.append(e)
        output[i][j] = valid
  return output

def printBigHint(grid):
  for i in range(0, 9):
    if i != 0 and i%3 == 0:
      print(150 * '_')
    for j in range(0, 9):
      print(grid[i][j], ((14 - len(str(grid[i][j]))) * ' '), end="")
      if j != 8 and (j + 1)%3 == 0:
        print('|    ', end="")
    print('')

def printHint(grid):
  for i in range(0, 9):
    if i != 0 and i%3 == 0:
      print((6 * '_') + '|' + (7 * '_') + '|' + (6 * '_'))
    for j in range(0, 9):
      print(len(grid[i][j]), end=" ")
      if j != 8 and (j + 1)%3 == 0:
        print('| ', end="")
    print('')

def printSingles(grid):
  for i in range(0, 9):
    if i != 0 and i%3 == 0:
      print((6 * '_') + '|' + (7 * '_') + '|' + (6 * '_'))
    for j in range(0, 9):
      if hasSingular(grid, i, j):
        print(1, end=" ")
      else:
        print(0, end=" ")
      if j != 8 and (j + 1)%3 == 0:
        print('| ', end="")
    print('')

# 'Very difficult' puzzle generated on 7 Sudoku
# http://www.7sudoku.com/view-puzzle?date=20170701
input = [[0, 6, 0, 0, 9, 3, 4, 0, 0],
         [1, 0, 3, 8, 7, 0, 9, 0, 0],
         [0, 4, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 5, 0, 0, 0, 0, 3],
         [0, 7, 0, 2, 0, 6, 0, 9, 0],
         [3, 0, 0, 0, 0, 8, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 0, 6, 0, 5, 1, 8, 0, 9],
         [0, 0, 1, 3, 8, 0, 0, 5, 0]]

output = solve(input)

printCounts(input)
print()
printHint(output)
print()
printBigHint(output)
print()
printSingles(output)
