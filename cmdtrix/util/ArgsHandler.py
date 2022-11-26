import argparse
from sys import exit as sysexit
from datetime import datetime
from os import path
from cmdtrix import __version__, __sysversion__, __author__

def string_integer(default_value):
    """Action for argparse that allows a mandatory and optional
    argument, a string and integer, with a default for the integer.

    This factory function returns an Action subclass that is
    configured with the integer default.
    """
    class StringInteger(argparse.Action):
        """Action to assign a string and optional integer"""
        def __call__(self, parser, namespace, values, option_string=None):
            message = ''
            if len(values) not in [1, 2]:
                message = 'argument "{}" requires 1 or 2 arguments'.format(
                    self.dest)
            if len(values) == 2:
                try:
                    values[1] = int(values[1]) / 100
                    if not 0.0 <= values[1] <= 1.0:
                        raise ValueError
                    values = (values[0], values[1])
                except ValueError:
                    message = ('second argument to "{}" requires '
                               'an integer between 0 and 100'.format(self.dest))
            else:
                values = (values[0], default_value)
            if message:
                raise argparse.ArgumentError(self, message)            
            setattr(namespace, self.dest, values)
    return StringInteger
            

class ArgsHandler:
    file = None
    workingDir = None
    
    params = None

    color = "green"
    dim = 0.0
    italic = 0.0
    synchronous = False
    message = [(b'\x4d\x61\x64\x65\x42\x79\x53\x69\x6c\x61\x73\x4b\x72\x61\x75\x6d\x65'.decode(), 0.01)]
    frameDelay = 0.015
    timer = None
    
    def __init__(self, file):
        self.file = file
        self.workingDir = path.dirname(path.realpath(self.file))
        self.parseArgs()
        self.translateArgs()

    def getVersion(self):
        return self.version

    def getColor(self):
        return self.color
    
    def getDim(self):
        return self.dim
    
    def getItalic(self):
        return self.italic
    
    def getSynchronous(self):
        return self.synchronous
    
    def getMessage(self):
        return self.message
    
    def getFrameDelay(self):
        return self.frameDelay
    
    def getTimer(self):
        return self.timer
    
    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--version", action="store_const", default=False,
                            const=True, dest="version", help="show program's version number and exit")
        parser.add_argument("-s", "--synchronous", action="store_const", default=False,
                            const=True, dest="synchronous", help="sync the matrix columns speed")
        parser.add_argument("-c", "--color", action="store", default="green",
                        choices=["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"], 
                        dest="color", metavar="[*]", help="set the color to *")
        parser.add_argument("-d", "--dim", action="store", default=1.0,
                            type=float, dest="dim", metavar="x%",
                            help="add chance for dim characters")
        parser.add_argument("-i", "--italic", action="store", default=1.0,
                            type=float, dest="italic", metavar="x%",
                            help="add chance for italic characters")
        parser.add_argument("-m", action=string_integer(0.01), dest="message",
                            nargs="+", metavar="* x%", help="hide a custom message within the Matrix")
        parser.add_argument("--framedelay", action="store", default=0.015, type=float,
                            dest="framedelay", metavar="DELAY", help="set the framedelay (in sec) to slow down the Matrix, default is 0.015")
        parser.add_argument("--timer", action="store", default=None, type=float,
                            dest="timer", metavar="DELAY", help="exit the Matrix after DELAY (in sec)")
        
        self.params = parser.parse_args()
    
    def translateArgs(self):
        if getattr(self.params, 'version'):
            self._showVersion()
        
        self.color = getattr(self.params, 'color')
        
        self.dim = getattr(self.params, 'dim') / 100
        if not 0.0 <= self.dim <= 1.0:
            print("The dim chance has to be between 0 and 100!")
            sysexit(1)
        
        self.italic = getattr(self.params, 'italic') / 100
        if not 0.0 <= self.italic <= 1.0:
            print("The italic chance has to be between 0 and 100!")
            sysexit(1)
        
        self.synchronous = getattr(self.params, "synchronous")
        
        if getattr(self.params, "message"):
            self.message += [getattr(self.params, "message")]
            
        self.frameDelay = getattr(self.params, "framedelay")
        if self.frameDelay < 0.0:
            print("A negative framedelay cannot be implemented!")
            sysexit(1)

        self.timer = getattr(self.params, "timer")
        
    def _showVersion(self):
        print()
        print("------------------------------------------------------------")
        print(f"cmdtrix {__version__} - from {self.workingDir}")
        print("------------------------------------------------------------")
        print()
        print(f"Python: \t{__sysversion__}")  # sys.version
        print(f"Build time: \t{datetime.fromtimestamp(path.getctime(path.realpath(__file__)))} CET")
        print(f"Author: \t{__author__}")
        sysexit(0)

