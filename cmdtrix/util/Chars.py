
def genCharList(unicode_start, unicode_end):
    return [chr(i) for i in range(unicode_start, unicode_end)]


basicLatinChars = genCharList(48, 127)
greekChars = genCharList(910, 930) #930 broken
greekChars += genCharList(931, 1024)
cyrillicChars = genCharList(1024, 1154)


charList = basicLatinChars + greekChars + cyrillicChars
