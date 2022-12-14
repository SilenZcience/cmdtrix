
from os import get_terminal_size, system, name as osname
from colorama import init as coloramaInit
from random import choice, choices, randrange, random
from time import sleep as delay_frame
from _thread import interrupt_main

from cmdtrix.util.EventTimer import EventTimer
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

HIDDEN_MESSAGE = []

SYNCHRONOUS = False
CHANCE_FOR_DIM = 0.0
CHANCE_FOR_ITALIC = 0.0

ON_KEY_DETECTION = True
keyDetected = 0

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

    message_event = False
    message_event_gen = None

    def __init__(self, col):
        self.col = col
        self.speedTicks = randrange(1, MAX_SPEED_TICKS + 1)
        self.speedTickCap = (MAX_SPEED_TICKS if SYNCHRONOUS else self.speedTicks)

        self.lineLength = randrange(MINIMUM_LINE_LENGTH, MAXIMUM_LINE_LENGTH+1)
        self.maxYPosition = min(rows, randrange(2*rows))

        for i in range(len(HIDDEN_MESSAGE)):
            self.message_event = (random() < HIDDEN_MESSAGE[i][1]) and (
                self.maxYPosition > len(HIDDEN_MESSAGE[i][0]) + 1)
            if self.message_event:
                self.message_event_gen = getNextChar(
                    HIDDEN_MESSAGE[i][0], self.maxYPosition - len(HIDDEN_MESSAGE[i][0]) - 1)
                break

    def update(self):
        self.currentTick = (self.currentTick % self.speedTickCap + 1)

        if self.currentTick == self.speedTicks:
            if self.yPositionSet <= self.maxYPosition:
                if self.message_event:
                    self.lastChar = next(self.message_event_gen)
                printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR,  ("2;" if random() < CHANCE_FOR_DIM else "") + ("3;" if random() < CHANCE_FOR_ITALIC else ""))
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


def getNextChar(hMessage: str, xSpace: int) -> str:
    yield from choices(charList, k=randrange(1, xSpace+1)) + list(hMessage)
    while True:
        yield choice(charList)


def printCode(*code: str) -> None:
    print("\x1b[" + "\x1b[".join(code), end="")


def printAtPosition(text: str, x: int, y: int, color: str, style: str = "") -> None:
    printCode("m", "%d;%df" % (y, x), style + colorCodes[color] + "m") # reset attributes, set position, set attributes and set color
    print(text, end="", flush=True)


def checkTerminalSize() -> None:
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


def on_press(key):
    global keyDetected
    keyDetected += 1


def addNewMatrixColumns(matrixColumns: set, condition) -> None:
    """
    add a new MatrixColumn every Tick, if the MAX has not been
    reached yet
    """
    if len(matrixColumns) >= NUMBER_OF_MATRIXCOLUMNS or not condition:
        return
    col = randrange(cols+1)
    matrixColumns.add(MatrixColumn(col))
    global keyDetected
    keyDetected = max(0, keyDetected-1)


def updateMatrixColumns(matrixColumns: set) -> None:
    for matrixColumn in matrixColumns:
        matrixColumn.update()


def getFinishedColumns(matrixColumns: set):
    finishedColumns = set()
    for matrixColumn in matrixColumns:
        if matrixColumn.finished:
            finishedColumns.add(matrixColumn)

    return finishedColumns


def init() -> None:
    printCode("?25l", "2J")  # hide cursor, clear screen
    return EventTimer(10, checkTerminalSize)


def deinit(eventTimer: list) -> None:
    printCode("m", "2J", "?25h")  # reset attributes, clear screen, show cursor
    for timer in eventTimer:
        timer.cancel()

def main():
    eventTimer = []
    exitOnArg = True
    try:
        argsHandler = ArgsHandler(__file__)
        global COLOR
        COLOR = argsHandler.color
        global CHANCE_FOR_DIM
        CHANCE_FOR_DIM = argsHandler.dim
        global CHANCE_FOR_ITALIC
        CHANCE_FOR_ITALIC = argsHandler.italic
        global SYNCHRONOUS
        SYNCHRONOUS = argsHandler.synchronous
        global HIDDEN_MESSAGE
        HIDDEN_MESSAGE = argsHandler.message
        global FRAME_DELAY
        FRAME_DELAY = argsHandler.frameDelay
        global ON_KEY_DETECTION
        ON_KEY_DETECTION = argsHandler.onkey
        exitOnArg = False
        
        eventTimer.append(init())
        timer = argsHandler.timer
        if timer != None:
            eventTimer.append(EventTimer(timer, interrupt_main, 'Timer'))
        if ON_KEY_DETECTION:
            eventTimer.append(EventTimer(None, None, 'keyboardListener', on_press=on_press))
            print('', flush=True)
        
        
        matrixColumns = set()
        while True:
            addNewMatrixColumns(matrixColumns, not ON_KEY_DETECTION or keyDetected)
            delay_frame(FRAME_DELAY)
            updateMatrixColumns(matrixColumns)
            # stdout.flush()
            matrixColumns.difference_update(getFinishedColumns(matrixColumns))
    except KeyboardInterrupt:
        pass
    finally:
        if not exitOnArg:
            deinit(eventTimer)
            system('cls' if osname == 'nt' else 'clear')


if __name__ == '__main__':
    main()
