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
    
    def __init__(self, file):
        self.file = file
        self.workingDir = path.dirname(path.realpath(self.file))
        self.parseArgs()
        self.translateArgs()

    def getVersion(self):
        return self.version

    def getColor(self):
        return self.color
    
    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--version", action="store_const", default=False,
                            const=True, dest="version", help="show program's version number and exit")
        parser.add_argument("-c", "--color", action="store", default="green",
                        choices=["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"], 
                        dest="color", metavar="[*]", help="set the color")
        
        self.params = parser.parse_args()
    
    def translateArgs(self):
        if getattr(self.params, 'version'):
            self._showVersion()
        self.color = getattr(self.params, 'color')
        
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

