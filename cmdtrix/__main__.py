from sys import exit

try:
    import cmdtrix.cmdtrix as cmdtrix
except KeyboardInterrupt:
    exit(0)
except:
    print("an error occured while loading the module")
    exit(1)

def entry_point():
    cmdtrix.main()

if __name__ == '__main__':
    entry_point()