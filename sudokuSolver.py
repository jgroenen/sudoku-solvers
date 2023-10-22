sudoku = [
    [0, 8, 3, 0, 9, 0, 7, 5, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 7, 0, 0, 0, 0, 6],
    [3, 0, 0, 1, 0, 0, 8, 7, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 2, 0, 0, 1, 3, 0],
    [0, 9, 0, 0, 0, 4, 0, 0, 0]
]

sudoku = [
    [4, 0, 0, 0, 0, 0, 3, 0, 2],
    [9, 0, 0, 0, 5, 6, 1, 8, 0],
    [0, 0, 8, 2, 0, 9, 0, 5, 0],
    [0, 0, 0, 0, 1, 3, 0, 6, 8],
    [0, 0, 0, 0, 7, 0, 5, 1, 0],
    [0, 0, 0, 9, 0, 0, 7, 0, 0],
    [0, 3, 7, 8, 0, 0, 2, 0, 5],
    [0, 0, 4, 7, 2, 0, 0, 0, 1],
    [0, 5, 0, 0, 6, 0, 8, 0, 0]
]

def printSudoku():
    print(" ", end="  ")
    for i in range(9):
        print(i+1, end=" ")
    print()
    print()
    for i in range(9):
        print(i+1, end="  ")
        for j in range(9):
            print(sudoku[i][j] if sudoku[i][j] else "_", end=" ")
        print()
    print()

def printOptions():
    for i in range(9):
        for j in range(9):
            for k in range(9):
                print(k+1 if options[i][j] & (0x1 << k) else "_", end="")
            print("", end=" ")
        print()
        print()
    print()

def sudokuIsFullyFilled():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return False
    return True

def loadOptionsFromSudoku():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]:
                setOptionsCellValue(i, j, sudoku[i][j])

def value(x):
    return int(x & -x).bit_length()

def known(x):
	return x.bit_count() == 1
	
def updateSudokuFromOptions():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0 and known(options[i][j]):
                sudoku[i][j] = value(options[i][j])
                print("rij", i+1, "kolom", j+1, "krijgt waarde", sudoku[i][j])
                print()

def setOptionsCellValue(i, j, k):
    options[i][j] = 0x1 << k-1

    # remove option from all other cells in column
    for I in range(9):
        if I != i:
            options[I][j] &= ~options[i][j]
    
    # remove option from all other cells in row
    for J in range(9):
        if J != j:
            options[i][J] &= ~options[i][j]
    
    # remove option from all other cells in block
    for B in range(9):
        I = 3 * (i // 3) + (B // 3)
        J = 3 * (j // 3) + (B % 3)
        if sudoku[I][J] == 0 and I != i or J != j:
            options[I][J] &= ~options[i][j]
    
# if there are two cells that have the same two options, the rest of that block will not have those two options
def checkTwos(i, j):
    if options[i][j].bit_count() != 2:
        return
    
    # check col
    for I in range(9):
        if I != i and options[I][j] == options[i][j]:
            for X in range(9):
                if X != i and X != I:
                    options[X][j] &= ~options[i][j]
    
    # check row
    for J in range(9):
        if J != j and options[i][J] == options[i][j]:
            for X in range(9):
                if X != j and X != J:
                    options[i][X] &= ~options[i][j]
    
    # check block
    for B in range(9):
        I = 3 * (i // 3) + (B // 3)
        J = 3 * (j // 3) + (B % 3)
        if (I != i or J != j) and options[i][j] == options[I][J]:
            for X in range(9):
                XI = 3 * (i // 3) + (X // 3)
                XJ = 3 * (j // 3) + (X % 3)
                if (XI != i and XI != I) or (XJ != j and XJ != J):
                    options[XI][XJ] &= ~options[i][j]

def checkUnique(i, j):
    if known(options[i][j]):
        return
        
    # check col
    x = options[i][j]
    for I in range(9):
        if I != i:
            x &= ~options[I][j]
    if known(x):
        options[i][j] = x 
        print("rij", i+1, "kolom", j+1, "is de enige in kolom die waarde", value(x), "kan hebben")
        print()
        return
        
    # check row
    x = options[i][j]
    for J in range(9):
        if J != j:
            x &= ~options[i][J]
    if known(x):
        options[i][j] = x
        print("rij", i+1, "kolom", j+1, "is de enige in rij die waarde", value(x), "kan hebben")
        print()
        return

    # check block
    x = options[i][j]
    for B in range(9):
        I = 3 * (i // 3) + (B // 3)
        J = 3 * (j // 3) + (B % 3)
        if I != i or J != j:
            x &= ~options[I][J]
    if known(x):
        options[i][j] = x
        print("rij", i+1, "kolom", j+1, "is de enige in blok die waarde", value(x), "kan hebben")
        print()
        return

options = [[0b111111111] * 9 for i in range(9)]
            
while not sudokuIsFullyFilled():

    printSudoku()

    loadOptionsFromSudoku()

    #printOptions()

    # check two's
    for i in range(9):
        for j in range(9):
            checkTwos(i, j)

    #printOptions()

    # check uniques
    for i in range(9):
        for j in range(9):
            checkUnique(i, j)

    #printOptions()

    updateSudokuFromOptions()

printSudoku()
