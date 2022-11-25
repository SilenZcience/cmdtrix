import argparse
from sys import exit as sysexit
from datetime import datetime
from os import path
from cmdtrix import __version__, __sysversion__, __author__

class ArgsHandler:
    file = None
    workingDir = None
    
    params = None

    color = "green"
    dim = 0.0
    italic = 0.0
    synchronous = False
    
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

