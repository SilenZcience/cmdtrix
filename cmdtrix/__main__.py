from sys import exit as sysexit

try:
    import cmdtrix.cmdtrix as cmdtrix
except KeyboardInterrupt:
    sysexit(0)
except Exception as e:
    print('an error occured while loading the modul')
    # print(e)
    sysexit(1)

def entry_point():
    cmdtrix.main()

if __name__ == '__main__':
    entry_point()
