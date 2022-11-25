
from os import get_terminal_size, system, name as osname
from colorama import init as coloramaInit
from random import choice, choices, randrange, random
from time import sleep as delay_frame
from sys import stdout

from cmdtrix.util.RepeatedTimer import RepeatedTimer
from cmdtrix.util.Chars import charList
from cmdtrix.util.ArgsHandler import ArgsHandler


colorCodes = {"black": "30", "red": "31", "green": "32", "yellow": "33",
              "blue": "34", "magenta": "35", "cyan": "36", "white": "37"}
cols, rows = get_terminal_size()

FRAME_DELAY = 0.015

MINIMUM_LINE_LENGTH = 10
MAXIMUM_LINE_LENGTH = rows
NUMBER_OF_MATRIXCOLUMNS = 600
MAX_SPEED_TICKS = 5
COLOR = "green"
EASTER_EGG_MESSAGE = "MadeBySilasKraume"

coloramaInit()


class MatrixColumn:
    col = None
    finished = False
    currentTick = 0
    speedTicks = None

    lineLength = 0
    maxYPosition = 0
    yPositionSet = 1
    yPositionErased = 1
    lastChar = ""

    easter_egg = False
    easter_egg_gen = None
    
    def __init__(self, col):
        self.col = col
        self.speedTicks = randrange(1, MAX_SPEED_TICKS+1)

        self.lineLength = randrange(MINIMUM_LINE_LENGTH, MAXIMUM_LINE_LENGTH+1)
        self.maxYPosition = min(rows, randrange(2*rows))
        
        self.easter_egg = (random() < 0.01) and (self.maxYPosition > len(EASTER_EGG_MESSAGE)+1)
        if self.easter_egg:
            self.easter_egg_gen = getNextChar(self.maxYPosition - len(EASTER_EGG_MESSAGE) - 1)

    def isFinished(self):
        return self.finished

    def update(self):
        if self.currentTick == self.speedTicks:
            if self.yPositionSet <= self.maxYPosition:
                if self.easter_egg:
                    self.lastChar = next(self.easter_egg_gen)
                printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR)
                newChar = choice(charList)
                printAtPosition(newChar, self.col, self.yPositionSet, "white")
                self.lastChar = newChar
            if self.yPositionSet == self.maxYPosition + 1 and self.maxYPosition >= rows:
                printAtPosition(self.lastChar, self.col,  self.yPositionSet-1, COLOR)
            if self.yPositionSet > self.lineLength:
                printAtPosition(" ", self.col, self.yPositionErased, "black")
                self.yPositionErased += 1
            if self.yPositionErased > self.maxYPosition:
                self.finished = True

            self.yPositionSet += 1
        elif self.yPositionSet <= self.maxYPosition:
            newChar = choice(charList)
            printAtPosition(newChar, self.col, self.yPositionSet-1, "white")
            self.lastChar = newChar

        self.currentTick += 1
        if self.currentTick > MAX_SPEED_TICKS:
            self.currentTick = 0


def getNextChar(xSpace):
    for r in choices(charList, k=randrange(1, xSpace+1)):
        yield r
    for i in EASTER_EGG_MESSAGE:
        yield i
    while True:
        yield choice(charList)

def printCode(code):
    print("\x1b[", code, sep="", end="")


def printAtPosition(text, x, y, color):
    printCode("%d;%df" % (y, x))
    printCode(colorCodes[color] + "m")
    print(text, end="", flush=True)


def checkTerminalSize():
    global cols, rows
    colsNew, rowsNew = get_terminal_size()
    if cols != colsNew or rows != rowsNew:
        cols = colsNew
        rows = rowsNew
        global MAXIMUM_LINE_LENGTH
        MAXIMUM_LINE_LENGTH = rows
        printCode("2J")  # clear screen


def addNewMatrixColumns(matrixColumns):
    if len(matrixColumns) >= NUMBER_OF_MATRIXCOLUMNS:
        return
    if random() > 0.5:
        return
    col = randrange(cols+1)
    matrixColumns.add(MatrixColumn(col))


def updateMatrixColumns(matrixColumns):
    for matrixColumn in matrixColumns:
        matrixColumn.update()


def getFinishedColumns(matrixColumns):
    finishedColumns = set()
    for matrixColumn in matrixColumns:
        if matrixColumn.isFinished():
            finishedColumns.add(matrixColumn)

    return finishedColumns


def init():
    printCode("?25l")  # hide cursor
    printCode("2J")  # clear screen
    return RepeatedTimer(10, checkTerminalSize)


def deinit(repeatedTimer: RepeatedTimer):
    printCode("m")  # reset attributes
    printCode("2J")  # clear screen
    printCode("?25h")  # show cursor
    if repeatedTimer != None:
        repeatedTimer.stop()
    return


def main():
    repeatedTimer = None
    exitOnArg = True
    try:
        argsHandler = ArgsHandler(__file__)
        global COLOR
        COLOR = argsHandler.getColor()
        
        exitOnArg = False
        repeatedTimer = init()
        matrixColumns = set()
        while True:
            addNewMatrixColumns(matrixColumns)
            delay_frame(FRAME_DELAY)
            updateMatrixColumns(matrixColumns)
            # stdout.flush()
            matrixColumns.difference_update(getFinishedColumns(matrixColumns))
    except KeyboardInterrupt:
        pass
    finally:
        if not exitOnArg:
            deinit(repeatedTimer)
            system('cls' if osname == 'nt' else 'clear')



if __name__ == '__main__':
    main()
