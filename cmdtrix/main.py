
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
NUMBER_OF_MATRIXCOLUMNS = cols
MAX_SPEED_TICKS = 5
COLOR = "green"

EASTER_EGG_MESSAGE = b'\x4d\x61\x64\x65\x42\x79\x53\x69\x6c\x61\x73\x4b\x72\x61\x75\x6d\x65'.decode()

SYNCHRONOUS = False
CHANCE_FOR_DIM = 0.0
CHANCE_FOR_ITALIC = 0.0

coloramaInit()


class MatrixColumn:
    col = None
    finished = False
    currentTick = 0
    speedTicks = None
    speedTickCap = None
    
    lineLength = 0
    maxYPosition = 0
    yPositionSet = 1
    yPositionErased = 1
    lastChar = ""

    easter_egg = False
    easter_egg_gen = None

    def __init__(self, col):
        self.col = col
        self.speedTicks = randrange(1, MAX_SPEED_TICKS + 1)
        self.speedTickCap = (MAX_SPEED_TICKS if SYNCHRONOUS else self.speedTicks)
        
        self.lineLength = randrange(MINIMUM_LINE_LENGTH, MAXIMUM_LINE_LENGTH+1)
        self.maxYPosition = min(rows, randrange(2*rows))

        self.easter_egg = (random() < 0.9) and (self.maxYPosition > len(EASTER_EGG_MESSAGE) + 1)
        if self.easter_egg:
            self.easter_egg_gen = getNextChar(self.maxYPosition - len(EASTER_EGG_MESSAGE) - 1)

    def update(self):
        self.currentTick = (self.currentTick % self.speedTickCap + 1)
        
        if self.currentTick == self.speedTicks:
            if self.yPositionSet <= self.maxYPosition:
                if self.easter_egg:
                    self.lastChar = next(self.easter_egg_gen)
                if random() < CHANCE_FOR_DIM:
                    printCode("2m")
                if random() < CHANCE_FOR_ITALIC:
                    printCode("3m")               
                printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR)
                newChar = choice(charList)
                printAtPosition(newChar, self.col, self.yPositionSet, "white")
                self.lastChar = newChar
            elif self.yPositionSet == self.maxYPosition + 1 and self.maxYPosition >= rows:
                printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR)
            if self.yPositionSet > self.lineLength:
                printAtPosition(" ", self.col, self.yPositionErased, "black")
                self.yPositionErased += 1
            self.finished = (self.yPositionErased > self.maxYPosition)

            self.yPositionSet += 1
        elif self.yPositionSet <= self.maxYPosition:
            self.lastChar = choice(charList)
            printAtPosition(self.lastChar, self.col, self.yPositionSet-1, "white")

        
def getNextChar(xSpace):
    yield from choices(charList, k=randrange(1, xSpace+1)) + list(EASTER_EGG_MESSAGE)
    while True:
        yield choice(charList)


def printCode(code):
    print("\x1b[", code, sep="", end="")


def printAtPosition(text, x, y, color):
    printCode("%d;%df" % (y, x))  # set row and col position
    printCode(colorCodes[color] + "m")  # set color
    print(text, end="", flush=True)
    printCode("m") # reset attributes


def checkTerminalSize():
    global cols, rows
    colsNew, rowsNew = get_terminal_size()
    if cols != colsNew or rows != rowsNew:
        cols = colsNew
        rows = rowsNew
        global MAXIMUM_LINE_LENGTH
        MAXIMUM_LINE_LENGTH = rows
        global NUMBER_OF_MATRIXCOLUMNS
        NUMBER_OF_MATRIXCOLUMNS = cols
        printCode("2J")  # clear screen


def addNewMatrixColumns(matrixColumns):
    if len(matrixColumns) >= NUMBER_OF_MATRIXCOLUMNS:
        return
    col = randrange(cols+1)
    matrixColumns.add(MatrixColumn(col))


def updateMatrixColumns(matrixColumns):
    for matrixColumn in matrixColumns:
        matrixColumn.update()


def getFinishedColumns(matrixColumns):
    finishedColumns = set()
    for matrixColumn in matrixColumns:
        if matrixColumn.finished:
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
        global CHANCE_FOR_DIM
        CHANCE_FOR_DIM = argsHandler.getDim()
        global CHANCE_FOR_ITALIC
        CHANCE_FOR_ITALIC = argsHandler.getItalic()
        global SYNCHRONOUS
        SYNCHRONOUS = argsHandler.getSynchronous()
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
