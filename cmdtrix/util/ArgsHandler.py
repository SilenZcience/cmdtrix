import argparse
from sys import exit as sysexit
from datetime import datetime
from os import path
from cmdtrix import __version__, __sysversion__, __author__
from cmdtrix.web.UpdateChecker import printUpdateInformation


COLOR_CHOICES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def store_message(default_chance, default_color):
    """Action for argparse that allows a mandatory and optional
    argument, a string and integer, with a default for the integer.

    This factory function returns an Action subclass that is
    configured with the integer default.
    """
    class StringInteger(argparse.Action):
        """Action to assign a string and optional integer"""
        def __call__(self, parser, namespace, values, option_string=None):
            error = ''
            message, chance, color = '', default_chance, default_color
            if len(values) not in [1, 2, 3]:
                error = 'argument "{}" requires 1 to 3 arguments'.format(self.dest)
            message = values[0]
            if len(values) >= 2:
                try:
                    chance = int(values[1]) / 100
                    if not 0.0 <= chance <= 1.0:
                        raise ValueError
                except ValueError:
                    error = ('second argument to "{}" requires '
                               'an integer between 0 and 100'.format(self.dest))
            if len(values) == 3:
                if not values[2] in COLOR_CHOICES:
                    error = ('third argument to "{}" requires '
                               'to be of the choice: '.format(self.dest))
                    error += ', '.join(COLOR_CHOICES)
                color = values[2]
            if error:
                raise argparse.ArgumentError(self, error)
            currentAttribute = getattr(namespace, self.dest)
            if not currentAttribute:
                currentAttribute = []   
            setattr(namespace, self.dest, currentAttribute + [(message, chance, color)])
    return StringInteger
            

class ArgsHandler:
    def __init__(self, file):
        self.file = file
        self.workingDir = path.dirname(path.realpath(self.file))
        
        self.params = None

        self.color = "green"
        self.color_peak = "white"
        self.dim = 0.0
        self.italic = 0.0
        self.synchronous = False
        self.message = (b'\x4d\x61\x64\x65\x42\x79\x53\x69\x6c\x61\x73\x4b\x72\x61\x75\x6d\x65'.decode(), 0.01)
        self.messages = []
        self.alpha = ""
        self.frameDelay = 0.015
        self.timer = None
        self.onkey = False
        
        self.parseArgs()
        self.translateArgs()

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--version", action="store_const", default=False,
                            const=True, dest="version", help="show program's version number and exit")
        parser.add_argument("-s", "--synchronous", action="store_const", default=False,
                            const=True, dest="synchronous", help="sync the matrix columns speed")
        parser.add_argument("-c", "--color", action="store", default="green",
                            choices=COLOR_CHOICES,
                            dest="color", metavar="[*]", help="set the main-color to *")
        parser.add_argument("-p", "--peak", action="store", default="white",
                            choices=COLOR_CHOICES,
                            dest="peak", metavar="[*]", help="set the peak-color to *")
        parser.add_argument("-d", "--dim", action="store", default=1.0,
                            type=float, dest="dim", metavar="p",
                            help="add chance p (percent) for dim characters")
        parser.add_argument("-i", "--italic", action="store", default=1.0,
                            type=float, dest="italic", metavar="p",
                            help="add chance p (percent) for italic characters")
        parser.add_argument("-m", action=store_message(0.01, "red"), dest="messages",
                            nargs="+", metavar="* p c", help="hide a custom message * within the Matrix, with chance p and color c")
        parser.add_argument("--symbols", action="store", default="", type=str, dest="alpha",
                            metavar="CHARS", help="set a custom series of symbols to choose from")
        parser.add_argument("--framedelay", action="store", default=0.015, type=float,
                            dest="framedelay", metavar="DELAY", help="set the framedelay (in sec) to slow down the Matrix, default is 0.015")
        parser.add_argument("--timer", action="store", default=None, type=float,
                            dest="timer", metavar="DELAY", help="exit the Matrix after DELAY (in sec) automatically")
        parser.add_argument("--onkey", action="store_const", default=False,
                            const=True, dest="onkey", help="only spawn columns on key-press")
        
        self.params = parser.parse_args()
    
    def translateArgs(self):
        if getattr(self.params, 'version'):
            self._showVersion()
            sysexit(0)
        
        self.color = getattr(self.params, 'color')
        self.color_peak = getattr(self.params, 'peak')
        
        self.dim = getattr(self.params, 'dim') / 100
        if not 0.0 <= self.dim <= 1.0:
            print("The dim chance has to be between 0 and 100!")
            sysexit(1)
        
        self.italic = getattr(self.params, 'italic') / 100
        if not 0.0 <= self.italic <= 1.0:
            print("The italic chance has to be between 0 and 100!")
            sysexit(1)
        
        self.synchronous = getattr(self.params, "synchronous")
        
        self.messages = [(self.message[0], self.message[1], self.color)]
        if getattr(self.params, "messages"):
            self.messages += getattr(self.params, "messages")
        
        self.alpha = getattr(self.params, "alpha")
        
        self.frameDelay = getattr(self.params, "framedelay")
        if self.frameDelay < 0.0:
            print("A negative framedelay cannot be implemented!")
            sysexit(1)

        self.timer = getattr(self.params, "timer")
        
        self.onkey = getattr(self.params, 'onkey')
        
    def _showVersion(self):
        print()
        print("------------------------------------------------------------")
        print(f"cmdtrix {__version__} - from {self.workingDir}")
        print("------------------------------------------------------------")
        print()
        print(f"Python: \t{__sysversion__}")  # sys.version
        print(f"Build time: \t{datetime.fromtimestamp(path.getctime(path.realpath(__file__)))} CET")
        print(f"Author: \t{__author__}")
        printUpdateInformation("cmdtrix", __version__)

