#################################################
# Simplex Algorithm
# by David You
#################################################


#################################################

# Helper function for print2dList.
# Taken from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

#################################################

# Algorithmic thinking and sample problems taken from
# https://courses.cs.washington.edu/courses/cse521/13wi/slides/09lp.pdf
# https://www.youtube.com/watch?v=8_D3gkrgeK8
# https://www.youtube.com/watch?v=iwDiG2mR6FM
# https://www.geeksforgeeks.org/simplex-algorithm-tabular-method/
# http://fourier.eng.hmc.edu/e176/lectures/NM/node32.html
# http://www.ms.uky.edu/~rwalker/Class%20Work%20Solutions/class%20work%208%20solutions

import string
import copy

def removeExtraWords(L):
    # Takes in a list and removes the extra words 'Max' or 'Min'
    i = 0
    while i < len(L):
        elem = L[i]
        if ("Max" in elem) or ("Min" in elem):
            L.remove(elem)
        i += 1
    return L

def removeOperators(L):
    # Takes in a list and removes all the non-alphanumeric values
    # For negative signs, I add the negative sign in front of the following element
    i = 0
    while i < len(L):
        elem = L[i]
        if (("+" in elem) or ("=" in elem) or (">=" in elem) or ("<=" in elem)):
            L.remove(elem)
        elif ("-" in elem) and (len(elem) == 1):
            L[i+1] = "-" + L[i+1]
            L.remove(elem)
        i += 1
    return L  

def cleanUpConstraints(L):
    # Takes a list and returns a 2d list with each initial element as a list 
    # And each entry in the string as an item in the list
    outerList = []
    for elem in L: 
        innerList = elem.split(" ")
        outerList.append(innerList)
    return outerList

def addSlackVariables(constraint,slackVariable):
    #Takes a 1d list and adds in the slackVariable number (int) to the 
    #Second to last value of each list
    slackVariableStr = 's' + str(slackVariable)
    constraint.insert(-1,slackVariableStr)
    return constraint

def flipOptimizationFunctionSigns(L):
    # Takes in the optimization function list and flips the signs
    for i in range(len(L)):
        entry = L[i]
        if (entry != 'z') and ('x' in entry):
            if entry[0] == "-":
                L[i] = entry[1:]
                entry = entry[1:]
            else:
                L[i] = "-" + entry
    return L

def checkEasyChangeMinToMax(initialConstraints):
    # Checks to ensure that the all the constraints have linear expressions
    # With the variables less than or equal to a constant
    modifiedConstraints = initialConstraints[:-1]
    for constraint in modifiedConstraints:
        if ("<=" not in constraint):
            return False
    return True

def easyChangeMinToMax(optimizationFunction):
    # If the constraints involve linear expressions with the variables 
    # less than or equal to a constant. I use the trick that minimizing 
    # this function C is the same as maximizing the function p = −z
    optimizationFunctionList = optimizationFunction.split(" ")
    flipOptimizationFunctionSigns(optimizationFunctionList)
    optimizationFunctionList[0] = "Maximize:"
    newOptimiztionFunction = " ".join(optimizationFunctionList)
    return newOptimiztionFunction



problem8 = '''
Minimize: 3x1 + 9x2 = z
Constraints:
2x1 + x2 >= 8
x1 + 2x2 >= 8
x1, x2 >= 0
'''




def getKeyInformation(problem):
    # Given a text, the function returns the a 2d List of the key information
    # Key information: constraint equations with slack variables and
    # Optimization Function
    outerList = []
    textList = problem.splitlines()
    optimizationFunction = textList[1]

    # The last line of every problem is the lower bound, which is always going to be zero
    # This bound is not used in the simplex tableau
    initialConstraints = textList[3:-1]


    # If I start out with a minimization function, I want to change it 
    # To a maximization function
    if "Min" in optimizationFunction:
        if checkEasyChangeMinToMax(initialConstraints):
            optimizationFunction = easyChangeMinToMax(optimizationFunction)
        else:
            


    # I remove the extra words from the optimization line
    optimizationFunction = removeExtraWords(optimizationFunction.split(" "))

    # I want to remove all the operators and add a "-" sign to the next value if it's negative
    cleanedOptimizationFunction = removeOperators(optimizationFunction)
    cleanedConstraints = cleanUpConstraints(initialConstraints)
    for equation in cleanedConstraints:
        removeOperators(equation)

    # I move all variables in the optimization function to one side
    # Keeping z positive and flipping the signs of everything else
    optimizationFunctionWithFlippedSigns = flipOptimizationFunctionSigns(cleanedOptimizationFunction)

    # I add in the slack variables to the constraint equations
    for i in range(len(cleanedConstraints)):
        curConstraint = cleanedConstraints[i]
        slackVariable = i + 1
        constraintWithSlackVariables = addSlackVariables(curConstraint,slackVariable)

    # Finally I want to add the function I want to optimize at the end of the 2d list
    cleaned2dList = copy.deepcopy(cleanedConstraints)
    cleaned2dList.append(optimizationFunctionWithFlippedSigns)
    return cleaned2dList

def removeCoefficientsFromX(L):
    # Takes in the 2d list and removes the coefficient for every 'x'
    for innerList in L:
        for i in range(len(innerList)):
            entry = innerList[i]
            if ("x" in entry) and (entry.find('x') != 0):
                replacement = entry.find('x')
                newEntry = entry[replacement:]
                innerList[i] = newEntry
    return L

def makeListOfAllVariables(text):
    # Takes in a 2dList and creates a 1dList with all the different variables
    # Without the coefficients
    newList = (getKeyInformation(text))
    cleanedList = removeCoefficientsFromX(newList)
    variableList = []
    for innerList in newList:
        for entry in innerList:
            if (entry not in variableList) and (not entry.isdigit()):
                variableList.append(entry)
    return variableList

def addZerosToMatrix(problem):
    # For spaces where there is no variable, input 0
    # Add zero in the optimization function as well since
    # I am moving all variables on one side
    newList = getKeyInformation(problem)
    variableList = makeListOfAllVariables(problem)
    for i in range(len(variableList)):
        currentCol = variableList[i]
        for innerList in newList:
            for j in range(len(innerList)):
                innerListEntry = innerList[i]
                if i == j:
                    if currentCol not in innerListEntry:
                        innerList.insert(i,0)
    newList[-1].append(0)
    return newList

def addHeaderToMatrix(problem):
    # Adds a row with the variable name
    L = addZerosToMatrix(problem)
    variableList = makeListOfAllVariables(problem)
    variableList.append('num')
    L.insert(0,variableList)
    return L

def getCoefficient(entry):
    # Returns the numerical coefficients of algebraic values with the sign
    # Only 'x' will have coefficients besides 1
    if isinstance(entry,int):
        # Accounts for all the zeros I inserted
        return entry
    elif entry.isdigit():
        # Accounts for the non-zero integers
        return int(entry)
    else:
        # Accounts for all the variables
        if (entry[0].isalpha()):
            return 1
        else: 
            if ("x" in entry) :
                # Accounts for coefficients of -1 before the 'x'
                if ("-x" in entry):
                    return -1
                else:
                    replacement = entry.find('x')
                    coefficient = int(entry[:replacement])
                    return coefficient

def createSimplexTalbeau(problem):
    # Creates the matrix with the coefficients of the constraints
    # Moves all variables in the optimization function to one side
    # Includes a header to indicate the column identity
    origMatrix = addHeaderToMatrix(problem)
    rows,cols = len(origMatrix), len(origMatrix[0])
    for i in range(1,rows):
        for j in range(cols):
            entry = origMatrix[i][j]
            origMatrix[i][j] = getCoefficient(entry)
    return origMatrix

def getCol(header,startRow,stopRow,matrix):
    # Takes in a specific header, the starting row and ending row
    # And returns a list of that column
    rows = len(matrix[startRow:stopRow])
    headers = matrix[0]
    col = headers.index(header)
    colList = []
    for row in range(startRow,stopRow):
        entry = matrix[row][col]
        colList.append(entry)
    return colList

def getColWithMostNegVal(matrix):
    # Finds the column with the most negative value and 
    # Returns the column and the value
    # If two values are equal, then it retursn the leftmost one
    headers = matrix[0]
    lastRow = len(matrix) - 1
    mostNegVal = 0
    colWithMostNegVal = 0  
    storeHeader = headers[0]
    for i in range(len(headers)):
        header = headers[i]
        elem = getCol(header,lastRow,lastRow+1,matrix)[0]
        if elem < mostNegVal:
            mostNegVal = elem
            colWithMostNegVal = i 
            storeHeader = header
    return (colWithMostNegVal,storeHeader)

def largestConstraint(pivotColList,numColList):
    # Takes in two different columns and returns the
    # value in the pivot column and row where the biggest constraint occurs
    # If two constraints are the same, then it returns the upmost one
    mostStringent = 10**10 # Smallest value, the given values should never be <0
    constraintRow = 0
    for i in range(len(pivotColList)):
        pivotVal = pivotColList[i]
        numVal = numColList[i]
        if (pivotVal != 0):
            constraint = numVal/pivotVal
            if (constraint < mostStringent) and (constraint >= 0):
                mostStringent = constraint
                constraintRow = i             
    val = pivotColList[constraintRow]
    return (val,constraintRow,mostStringent)

def getPivot(matrix):
    # Finds the pivot value, row, and column that will be used 
    # for the basis of all calculations
    rows = len(matrix)
    (colWithMostNegVal,storeHeader) = getColWithMostNegVal(matrix)
    startRow, endRow = 1, rows-1
    pivotColList = getCol(storeHeader,startRow,endRow,matrix)
    numColList = getCol('num',startRow,endRow,matrix)
    (val, constraintRow, mostStringent) = largestConstraint(pivotColList,numColList)
    pivotRow = startRow + constraintRow
    return (val, pivotRow, colWithMostNegVal)

def makePivotOne(pivotVal,pivotRow,matrix):
    # Takes in the pivotRow and makes the pivot 1, changing all other
    # Values in the row accordingly
    pivotRowList = matrix[pivotRow]
    newPivotRowList = []
    multiplier = 1/pivotVal
    for value in pivotRowList:
        newValue = value*multiplier
        newValue = round(newValue,3)
        newPivotRowList.append(newValue)
    return newPivotRowList

def calculateNewRow(negativeMultiplier,otherRowList,pivotRowList):
    # Calculates the new row based on the pivot row and the original other row
    newOtherRow = []
    for i in range(len(pivotRowList)):
        pivotRowEntry = pivotRowList[i]
        otherRowEntry = otherRowList[i]
        newOtherRowEntry = (negativeMultiplier*pivotRowEntry) + otherRowEntry
        newOtherRow.append(round(newOtherRowEntry,3))
    return newOtherRow

def getPivotAdjustedRow(matrix,row,pivotRow,pivotCol):
    # Changes the other row so that it has a 0 in the pivot column
    negativeMultiplier = -(matrix[row][pivotCol])
    newRow = calculateNewRow(negativeMultiplier,matrix[row],matrix[pivotRow])
    return newRow

def simplexAlgorithm(matrix):
    # Recursively applies the simplex algorithm until all values in 
    # The last row are greater than 0
    rows, cols = len(matrix), len(matrix[0])
    lastRow = matrix[-1]
    if min(lastRow) >= 0:
        return matrix
    else:
        (pivotVal,pivotRow,pivotCol) = getPivot(matrix)
        newPivotRowList = makePivotOne(pivotVal,pivotRow,matrix)
        matrix[pivotRow] = newPivotRowList
        for row in range(1,pivotRow):
            newRow = getPivotAdjustedRow(matrix,row,pivotRow,pivotCol)
            matrix[row] = newRow
        for row in range(pivotRow + 1,rows):
            newRow = getPivotAdjustedRow(matrix,row,pivotRow,pivotCol)
            matrix[row] = newRow
        return simplexAlgorithm(matrix)

def simplexAlgorithmWrapper(problem):
    # Wrapper Function for the simplex algorithm
    matrix = createSimplexTalbeau(problem)
    optimizedMatrix = simplexAlgorithm(matrix)
    return optimizedMatrix

def getOptimizedValue(problem):
    # Takes in an optimized matrix and returns the optimized value
    optimizedMatrix = simplexAlgorithmWrapper(problem)
    rows,cols = len(optimizedMatrix), len(optimizedMatrix[0])
    lastRow,lastCol = rows-1,cols-1
    optimizedValue = round(optimizedMatrix[lastRow][lastCol])
    # If you want to see the 2d matrix, uncomment the next line
    #print(print2dList(optimizedMatrix))
    if "Min" in problem:
        return -1*optimizedValue
    return optimizedValue






#################################################
# Test Functions

# Note: 
# Although the code does not have 2dList function to output values,
# I used the print2dList function to help me see the matrices 
# Thus, I decided to include it in my citation
#################################################

def testRemoveOperators():
    print('Testing removeOperaters()...', end='')
    L = ['2x1', '+', '5x2', '=', 'z']
    assert(removeOperators(L) == ['2x1','5x2','z'])
    L = ['2x1', '-', '5x2', '=', 'z']
    assert(removeOperators(L) == ['2x1','-5x2','z'])
    L = ['x1', '+', 'x2', '=', '6']
    assert(removeOperators(L) == ['x1','x2','6'])
    L = ['-x1', '-', '4x2', '=', '-3']
    assert(removeOperators(L) == ['-x1','-4x2','-3'])
    L = ['x2', '<=', '3']
    assert(removeOperators(L) == ['x2','3'])
    print('Passed!')

def testGetKeyInformation():
    print('Testing getKeyInformation()...', end='')
    # Taken from https://www.geeksforgeeks.org/simplex-algorithm-tabular-method/
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    assert(getKeyInformation(problem) == [['x1','x2','s1','6'],
                                          ['x2','s2','3'],
                                          ['x1','2x2','s3','9'],
                                          ['-2x1','-5x2','z']])
    # Taken from https://www.youtube.com/watch?v=iwDiG2mR6FM
    problem1 = '''
Maximize: 8x1 + 10x2 + 7x3 = z
Constraints:
x1 + 3x2 + 2x3 <= 10
x1 + 5x2 + x3 <= 8
x1, x2, x3 >= 0
'''
    assert(getKeyInformation(problem1) == [['x1', '3x2', '2x3','s1','10'],
                                           ['x1', '5x2', 'x3' ,'s2', '8'],
                                           ['-8x1','-10x2','-7x3','z']])
    # Taken from https://courses.cs.washington.edu/courses/cse521/13wi/slides/09lp.pdf
    problem2 = '''
Maximize: 15x1 + 10x2 = z
Constraints:
x1 <= 2
x2 <= 3
x1 + x2 <= 4
x1, x2 >= 0
'''
    assert(getKeyInformation(problem2) == [['x1',  's1',  '2'],
                                           ['x2',  's2',  '3'],
                                           ['x1',  'x2',  's3','4'],
                                           ['-15x1','-10x2','z']])
    # Taken from http://fourier.eng.hmc.edu/e176/lectures/NM/node32.html
    problem3 = '''
Maximize: 2x1 + 3x2 = z
Constraints:
2x1 + x2 <= 18
6x1 + 5x2 <= 60
2x1 + 5x2 <= 40
x1, x2 >= 0
'''
    assert(getKeyInformation(problem3) == [['2x1', 'x2',  's1', '18'],
                                           ['6x1', '5x2', 's2', '60'],
                                           ['2x1', '5x2', 's3', '40'],
                                           ['-2x1', '-3x2', 'z']])
    print('Passed!')

def testAddHeaderToMatrix():
    print('Testing addHeaderToMatrix()...', end='')
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    assert(addHeaderToMatrix(problem) == [[ 'x1',    'x2', 's1', 's2', 's3', 'z', 'num'], 
                                          [ 'x1',    'x2', 's1',    0,    0,   0,  '6' ], 
                                          [    0,    'x2',    0, 's2',    0,   0,  '3' ], 
                                          [ 'x1',   '2x2',    0,    0, 's3',   0,  '9' ], 
                                          ['-2x1', '-5x2',    0,    0,    0, 'z',   0  ]])
    problem1 = '''
Maximize: 8x1 + 10x2 + 7x3 = z
Constraints:
x1 + 3x2 + 2x3 <= 10
x1 + 5x2 + x3 <= 8
x1, x2, x3 >= 0
'''
    assert(addHeaderToMatrix(problem1) == [[  'x1',    'x2',   'x3', 's1', 's2', 'z', 'num'], 
                                           [  'x1',   '3x2',  '2x3', 's1',    0,   0, '10' ], 
                                           [  'x1',   '5x2',   'x3',    0, 's2',   0,  '8' ], 
                                           ['-8x1', '-10x2', '-7x3',    0,    0,  'z',  0  ]])
    problem2 = '''
Maximize: 15x1 + 10x2 = z
Constraints:
x1 <= 2
x2 <= 3
x1 + x2 <= 4
x1, x2 >= 0
'''
    assert(addHeaderToMatrix(problem2) == [[   'x1', 's1',    'x2', 's2', 's3', 'z', 'num'], 
                                           [   'x1', 's1',       0,    0,    0,   0,  '2' ], 
                                           [      0,    0,    'x2', 's2',    0,   0,  '3' ], 
                                           [   'x1',    0,    'x2',    0, 's3',   0,  '4' ], 
                                           ['-15x1',    0, '-10x2',    0,    0, 'z',   0  ]])
    problem3 = '''
Maximize: 2x1 + 3x2 = z
Constraints:
2x1 + x2 <= 18
6x1 + 5x2 <= 60
2x1 + 5x2 <= 40
x1, x2 >= 0
'''
    assert(addHeaderToMatrix(problem3) == [[  'x1',   'x2', 's1', 's2', 's3', 'z', 'num'], 
                                           [ '2x1',   'x2', 's1',    0,    0,   0,  '18' ], 
                                           [ '6x1',  '5x2',    0, 's2',    0,   0,  '60' ], 
                                           [ '2x1',  '5x2',    0,    0, 's3',   0,  '40' ], 
                                           ['-2x1', '-3x2',    0,    0,    0, 'z',   0  ]])
    print('Passed!')

def testGetCoefficient():
    print('Testing getCoefficient()...', end='')
    assert(getCoefficient('x1') == 1)
    assert(getCoefficient('x2') == 1)
    assert(getCoefficient('s1') == 1)
    assert(getCoefficient('s2') == 1)
    assert(getCoefficient('z') == 1)
    assert(getCoefficient('3x1') == 3)
    assert(getCoefficient('12x2') == 12)
    assert(getCoefficient('15112x3') == 15112)
    assert(getCoefficient('-3x1') == -3)
    assert(getCoefficient('-12x2') == -12)
    assert(getCoefficient('-15112x3') == -15112)
    print('Passed!')

def testCreateSimplexTalbeau():
    print('Testing createSimplexTalbeau()...', end='')
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    assert(createSimplexTalbeau(problem) == [['x1', 'x2', 's1', 's2', 's3', 'z', 'num'], 
                                            [   1,    1,    1,    0,    0,   0,    6  ],
                                            [   0,    1,    0,    1,    0,   0,    3  ],
                                            [   1,    2,    0,    0,    1,   0,    9  ],
                                            [  -2,   -5,    0,    0,    0,   1,    0  ]])
    problem1 = '''
Maximize: 8x1 + 10x2 + 7x3 = z
Constraints:
x1 + 3x2 + 2x3 <= 10
x1 + 5x2 + x3 <= 8
x1, x2, x3 >= 0
'''
    assert(createSimplexTalbeau(problem1) == [['x1', 'x2', 'x3', 's1', 's2', 'z', 'num'],
                                             [    1,   3,    2,    1,    0,   0,    10 ],
                                             [    1,   5,    1,    0,    1,   0,     8 ],
                                             [   -8, -10,   -7,    0,    0,   1,     0 ]])
    problem2 = '''
Maximize: 15x1 + 10x2 = z
Constraints:
x1 <= 2
x2 <= 3
x1 + x2 <= 4
x1, x2 >= 0
'''
    assert(createSimplexTalbeau(problem2) == [['x1', 's1', 'x2', 's2', 's3', 'z', 'num'],
                                             [   1,    1,    0,    0,    0,   0,    2  ],
                                             [   0,    0,    1,    1,    0,   0,    3  ],
                                             [   1,    0,    1,    0,    1,   0,    4  ],
                                             [ -15,    0,  -10,    0,    0,   1,    0  ]])
    problem3 = '''
Maximize: 2x1 + 3x2 = z
Constraints:
2x1 + x2 <= 18
6x1 + 5x2 <= 60
2x1 + 5x2 <= 40
x1, x2 >= 0
'''
    assert(createSimplexTalbeau(problem3) == [['x1', 'x2', 's1', 's2', 's3', 'z', 'num'],
                                              [  2,    1,    1,    0,    0,   0,    18 ],
                                              [  6,    5,    0,    1,    0,   0,    60 ],
                                              [  2,    5,    0,    0,    1,   0,    40 ],
                                              [ -2,   -3,    0,    0,    0,   1,    0  ]])
    print('Passed!')


def testGetCol():
    print('Testing getCol()...', end='')
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    matrix = createSimplexTalbeau(problem)
    """
    matrix:
    [[  x1,  x2,  s1,  s2,  s3,   z, num ]
    [    1,   1,   1,   0,   0,   0,   6 ]
    [    0,   1,   0,   1,   0,   0,   3 ]
    [    1,   2,   0,   0,   1,   0,   9 ]
    [   -2,  -5,   0,   0,   0,   1,   0 ]]
    """
    assert(getCol('num',1,4,matrix) == [6, 3, 9])
    assert(getCol('x1',1,5,matrix) == [1, 0, 1, -2])
    assert(getCol('x2',0,3,matrix) == ['x2', 1, 1])
    assert(getCol('s1',0,0,matrix) == [])
    assert(getCol('s1',0,1,matrix) == ['s1'])
    assert(getCol('s3',0,5,matrix) == ['s3', 0, 0, 1, 0])
    assert(getCol('s3',5,5,matrix) == [])
    print('Passed!')

def testGetColWithMostNegVal():
    print('Testing getColWithMostNegVal()...', end='')
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    matrix = createSimplexTalbeau(problem)
    assert(getColWithMostNegVal(matrix) == (1,'x2'))
    problem1 = '''
Maximize: 8x1 + 10x2 + 7x3 = z
Constraints:
x1 + 3x2 + 2x3 <= 10
x1 + 5x2 + x3 <= 8
x1, x2, x3 >= 0
'''
    matrix = createSimplexTalbeau(problem1)
    assert(getColWithMostNegVal(matrix) == (1,'x2'))
    problem2 = '''
Maximize: 15x1 + 10x2 = z
Constraints:
x1 <= 2
x2 <= 3
x1 + x2 <= 4
x1, x2 >= 0
'''
    matrix = createSimplexTalbeau(problem2)
    assert(getColWithMostNegVal(matrix) == (0,'x1'))
    problem3 = '''
Maximize: 2x1 + 3x2 = z
Constraints:
2x1 + x2 <= 18
6x1 + 5x2 <= 60
2x1 + 5x2 <= 40
x1, x2 >= 0
'''
    matrix = createSimplexTalbeau(problem3)
    assert(getColWithMostNegVal(matrix) == (1,'x2'))
    print('Passed!')


def testGetOptimizedValue():
    print('Testing getOptimizedValue()...', end='')
    problem = '''
Maximize: 2x1 + 5x2 = z
Constraints:
x1 + x2 <= 6
x2 <= 3
x1 + 2x2 <= 9
x1, x2 >= 0
'''
    assert(getOptimizedValue(problem) == 21)
    problem1 = '''
Maximize: 8x1 + 10x2 + 7x3 = z
Constraints:
x1 + 3x2 + 2x3 <= 10
x1 + 5x2 + x3 <= 8
x1, x2, x3 >= 0
'''
    assert(getOptimizedValue(problem1) == 64)
    problem2 = '''
Maximize: 15x1 + 10x2 = z
Constraints:
x1 <= 2
x2 <= 3
x1 + x2 <= 4
x1, x2 >= 0
'''
    assert(getOptimizedValue(problem2) == 50)
    problem3 = '''
Maximize: 2x1 + 3x2 = z
Constraints:
2x1 + x2 <= 18
6x1 + 5x2 <= 60
2x1 + 5x2 <= 40
x1, x2 >= 0
'''
    assert(getOptimizedValue(problem3) == 28)

    # Additional Examples taken from
    # https://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf
    problem4 = '''
Maximze: 4x1 + 6x2 = z
Constraints:
-x1 + x2 <= 11
x1 + x2 <= 27
2x1 + 5x2 <= 90
x1, x2, >= 0
'''
    assert(getOptimizedValue(problem4) == 132)   
    problem5 = '''
Maximize: 2x1 - x2 + 2x3 = z
Constraints:
2x1 + x2 <= 10
x1 + 2x2 - 2x3 <= 20
x2 + 2x3 <= 5
x1, x2, x3 >= 0
'''
    assert(getOptimizedValue(problem5) == 15)  
    problem6 = '''
Maximize: 3x1 + 2x2 + x3 = z
Constraints:
4x1 + x2 + x3 = 30
2x1 + 3x2 + x3 <= 60
x2 + 2x3 <= 40
x1, x2, x3 >= 0
'''
    assert(getOptimizedValue(problem6) == 45)  
    problem7 = '''
Minimize: -2x1 + x2 = z
Constraints:
x1 + 2x2 <= 6
3x1 + 2x2 <= 12
x1, x2, >= 0
'''
    assert(getOptimizedValue(problem7) == -8)  
    print('Passed!')




def testAll():
    testRemoveOperators()
    testGetKeyInformation()
    testAddHeaderToMatrix()
    testGetCoefficient()
    testCreateSimplexTalbeau()
    testGetCol()
    testGetColWithMostNegVal()
    testGetOptimizedValue()

testAll()