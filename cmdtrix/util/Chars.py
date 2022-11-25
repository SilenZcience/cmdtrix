
def genCharList(unicode_start, unicode_end):
    return [chr(i) for i in range(unicode_start, unicode_end)]


basicLatinChars = genCharList(48, 127)
greekChars = genCharList(910, 1024)
cyrillicChars = genCharList(1024, 1154)


charList = basicLatinChars + greekChars + cyrillicChars
