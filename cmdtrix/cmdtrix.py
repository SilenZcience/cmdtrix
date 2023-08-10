from os import get_terminal_size, system, name as osname
from sys import exit
try:
    from colorama import init as coloramaInit
except ImportError:
    nop = lambda *_, **__: None; coloramaInit = nop
from random import choices, randrange, random
from time import sleep as delay_frame
from _thread import interrupt_main
from functools import lru_cache

from cmdtrix.util.EventTimer import EventTimer
from cmdtrix.util.Chars import charList, japanese
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
COLOR_PEAK = "white"

HIDDEN_MESSAGE = []

SYNCHRONOUS = False
CHANCE_FOR_DIM = 0.0
CHANCE_FOR_ITALIC = 0.0

ON_KEY_DETECTION = False
keyDetected = 0

coloramaInit()


class MatrixColumn:
    def __init__(self, col):
        self.reset(col)

    def reset(self, col):
        self.finished = False
        self.currentTick = 0
        
        self.yPositionSet = 1
        self.yPositionErased = 1
        self.lastChar = ""
        
        self.col = col
        self.speedTicks = randrange(1, MAX_SPEED_TICKS + 1)
        self.speedTickCap = (MAX_SPEED_TICKS if SYNCHRONOUS else self.speedTicks)

        self.lineLength = randrange(MINIMUM_LINE_LENGTH, MAXIMUM_LINE_LENGTH+1)
        self.maxYPosition = min(rows, randrange(2*rows))

        self.chars = choices(charList, k=self.speedTickCap * (self.maxYPosition - 1) + self.speedTicks)
        
        self.message_event = False
        self.message_chars = []
        self.message_color = None
        self.message_begin = 0
        self.message_length = 0
        for message, chance, color in HIDDEN_MESSAGE:
            self.message_event = (self.maxYPosition > len(message) + 1) and (random() < chance)
            if self.message_event:
                self.message_chars = list(message)
                self.message_color = color
                self.message_begin = randrange(1, self.maxYPosition - len(message)+1)
                self.message_length = len(self.message_chars)
                break

    def update(self):
        self.currentTick = (self.currentTick % self.speedTickCap + 1)

        if self.currentTick == self.speedTicks:
            if self.yPositionSet <= self.maxYPosition:
                if self.message_event and self.message_begin <= self.yPositionSet < self.message_begin + self.message_length:
                    self.lastChar = self.message_chars.pop(0)
                    printAtPosition(self.lastChar, self.col, self.yPositionSet-1, self.message_color,  ("2;" * (random() < CHANCE_FOR_DIM)) + ("3;" * (random() < CHANCE_FOR_ITALIC)))
                else:
                    printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR,  ("2;" * (random() < CHANCE_FOR_DIM)) + ("3;" * (random() < CHANCE_FOR_ITALIC)))
                self.lastChar = self.chars.pop()
                printAtPosition(self.lastChar , self.col, self.yPositionSet, COLOR_PEAK)
            elif self.yPositionSet - 1 == self.maxYPosition >= rows:
                printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR)
            if self.yPositionSet > self.lineLength:
                printAtPosition(" ", self.col, self.yPositionErased, "black")
                self.yPositionErased += 1
            self.finished = (self.yPositionErased > self.maxYPosition)

            self.yPositionSet += 1
        elif self.yPositionSet <= self.maxYPosition:
            self.lastChar = self.chars.pop()
            printAtPosition(self.lastChar, self.col, self.yPositionSet-1, COLOR_PEAK)


@lru_cache(maxsize=min(cols*rows, 5000))
def getCode(*code: str) -> str:
    return "\x1b[" + "\x1b[".join(code)


def printCode(*code: str) -> None:
    print(getCode(*code), end="")


def printAtPosition(text: str, x: int, y: int, color: str, style: str = "") -> None:
    # reset attributes, set position, set attributes and set color, concatenate with char
    print(getCode("m", "%d;%df" % (y, x), style + colorCodes[color] + "m"), text, sep="", end="", flush=True)


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


def updateMatrixColumns(matrixColumns: set) -> None:
    """
    add a new MatrixColumn every Tick, if the MAX has not been
    reached yet
    """
    global keyDetected
    for matrixColumn in matrixColumns:
        matrixColumn.update()
        if matrixColumn.finished and (not ON_KEY_DETECTION or keyDetected):
            col = randrange(cols+1)
            matrixColumn.reset(col)
            keyDetected = max(0, keyDetected-1)
    if len(matrixColumns) >= NUMBER_OF_MATRIXCOLUMNS or (ON_KEY_DETECTION and not keyDetected):
        return
    col = randrange(cols+1)
    matrixColumns.add(MatrixColumn(col))
    keyDetected = max(0, keyDetected-1)


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
    exitStatus = 0
    try:
        argsHandler = ArgsHandler(__file__)
        global COLOR
        COLOR = argsHandler.color
        global COLOR_PEAK
        COLOR_PEAK = argsHandler.color_peak
        global CHANCE_FOR_DIM
        CHANCE_FOR_DIM = argsHandler.dim
        global CHANCE_FOR_ITALIC
        CHANCE_FOR_ITALIC = argsHandler.italic
        global SYNCHRONOUS
        SYNCHRONOUS = argsHandler.synchronous
        global HIDDEN_MESSAGE
        HIDDEN_MESSAGE = argsHandler.messages
        global charList
        charList = [*argsHandler.alpha] if argsHandler.alpha else charList
        charList = japanese if argsHandler.japanese else charList
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
            updateMatrixColumns(matrixColumns)
            delay_frame(FRAME_DELAY)
            # stdout.flush()
    except KeyboardInterrupt:
        pass
    except Exception:
        exitStatus = 1
    finally:
        if not exitOnArg:
            deinit(eventTimer)
            system('cls' if osname == 'nt' else 'clear')
    exit(exitStatus)


if __name__ == '__main__':
    main()
