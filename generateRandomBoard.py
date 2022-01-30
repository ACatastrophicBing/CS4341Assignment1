#!/usr/bin/env python

import numpy as np
from numpy import *

# Defined in main, do not use these...
arrayCols = 100
arrayRows = 100

def placeS(arrayCols, arrayRows, board):
    startCol = np.random.randint(0, arrayCols - 1)
    startRow = np.random.randint(0, arrayRows - 1)
    if board[startCol][startRow] == -1:
        placeS(arrayCols, arrayRows, board)
    else:
        board[startCol][startRow] = '-2'


def getBoard(cols, rows):
    arrayCols = cols
    arrayRows = rows

    board = np.random.randint(9, size=(arrayCols, arrayRows))+1

    goalCol = np.random.randint(0, arrayCols - 1)
    goalRow = np.random.randint(0, arrayRows - 1)

    board[goalCol][goalRow] = '-1'

    placeS(arrayCols, arrayRows, board)

    nparr= np.array(board)
    nparr = np.where(board == -1, 'G', board)
    nparr = np.where(board == -2, 'S', nparr)

    #print(nparr)

    return board

