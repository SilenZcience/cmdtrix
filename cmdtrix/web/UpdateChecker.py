from urllib.request import urlopen
from json import loads as loadJSON
try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        YELLOW = '\x1b[33m'
        LIGHTBLACK_EX = '\x1b[90m'
        RED = '\x1b[31m'
    class Style:
        RESET_ALL = '\x1b[m'


# UNSAFE:
# UPDATE MAY INCLUDE FUNDAMENTAL CHANGES
# recognized by a higher version number in earlier position
# !.!._
# SAFE:
# recognized by a higher version number in the last position
# _._.!
STATUS_UP_TO_DATE = 0
STATUS_STABLE_RELEASE_AVAILABLE = 1
STATUS_UNSAFE_STABLE_RELEASE_AVAILABLE = -1
STATUS_PRE_RELEASE_AVAILABLE = 2
STATUS_UNSAFE_PRE_RELEASE_AVAILABLE = -2


def getLastestPackageVersion(package: str) -> str:
    try:
        with urlopen(f"https://pypi.org/pypi/{package}/json", timeout=2) as _response:
            response = _response.read()
        return loadJSON(response)['info']['version']
    except:
        return '0.0.0'


def onlyNumeric(s: str) -> int:
    return int('0' + ''.join(filter(str.isdigit, s)))


def genVersionTuples(v: str, w: str) -> tuple:
    """
    "1.0.33.0", "1.1.0a"
    v
    (('01', '00', '33', '00'), ('01', '01', '0a', '00'))
    """
    vSplit, wSplit = v.split('.'), w.split('.')
    maxSplitLen = max(map(len, vSplit + wSplit))
    vList = [s.zfill(maxSplitLen) for s in vSplit]
    wList = [s.zfill(maxSplitLen) for s in wSplit]
    maxLength = max(len(vList), len(wList))
    vList += [''.zfill(maxSplitLen)] * (maxLength - len(vList))
    wList += [''.zfill(maxSplitLen)] * (maxLength - len(wList))
    return (tuple(vList), tuple(wList))

def newVersionAvailable(currentVersion: str, latestVersion: str) -> int:
    """
    Checks whether or not a new version is available by comapring
    two version strings. returns a numeric value identifying
    the case.
    """
    if currentVersion.startswith('v'):
        currentVersion = currentVersion[1:]
    if latestVersion.startswith('v'):
        latestVersion = latestVersion[1:]
    status = STATUS_UP_TO_DATE
    current, latest = genVersionTuples(currentVersion, latestVersion)
    i = 0
    for c, l in zip(current, latest):
        i += 1
        cNum, lNum = onlyNumeric(c), onlyNumeric(l)
        if cNum > lNum:
            break
        if cNum < lNum:
            status = STATUS_STABLE_RELEASE_AVAILABLE
            if not l.isdigit():
                status = STATUS_PRE_RELEASE_AVAILABLE
            break
        if c < l:
            status = STATUS_PRE_RELEASE_AVAILABLE
            break
    if i < len(current):
        status *= -1
    return status


def printUpdateInformation(package: str, currentVersion: str):
    latestVersion = getLastestPackageVersion(package)
    status = newVersionAvailable(currentVersion, latestVersion)
    if status == STATUS_UP_TO_DATE:
        return
    message = f""
    warning = f""
    if abs(status) == STATUS_STABLE_RELEASE_AVAILABLE:
        message += f"{Fore.YELLOW}"
        message += f"A new stable release of {package} is available: v{latestVersion}\n"
        message += f"To update, run:\n"
        message += f"python -m pip install --upgrade {package}"
    elif abs(status) == STATUS_PRE_RELEASE_AVAILABLE:
        message += f"{Fore.LIGHTBLACK_EX}"
        message += f"A new pre-release of {package} is available: v{latestVersion}"
    message += f"{Style.RESET_ALL}"
    if status < 0:
        warning += f"{Fore.RED}"
        warning += f"Warning: Due to the drastic version increase, backwards compatibility is no longer guaranteed!\n"
        warning += f"You may experience fundamental differences."
        warning += f"{Style.RESET_ALL}\n"
    print(message)
    print(warning)
