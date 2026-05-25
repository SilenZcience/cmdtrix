
def genCharList(unicode_start, unicode_end):
    return [chr(i) for i in range(unicode_start, unicode_end)]


basicLatinChars = genCharList(   48,   127)

greekChars      = genCharList(  910,   930) # 930 broken
greekChars     += genCharList(  931,   994) # 994, 995 broken
greekChars     += genCharList(  996,  1018) # 1018, 1019 broken
greekChars     += genCharList( 1020,  1024)

cyrillicChars   = genCharList( 1024,  1120) # 1120, 1121 broken
cyrillicChars  += genCharList( 1122,  1124) # 1124 - 1133 broken
cyrillicChars  += genCharList( 1134,  1136) # 1136 - 1151 broken
cyrillicChars  += genCharList( 1152,  1154)

mathOps         = genCharList( 8705,  8709) # 9709 broken
mathOps        += genCharList( 8710,  8731) # 8731 - 8733 broken
mathOps        += genCharList( 8734,  8748) # 8748, 8749 broken
mathOps        += genCharList( 8750,  8751) # 8751, 8752 broken
mathOps        += genCharList( 8753,  8810) # 8810, 8811 broken
mathOps        += genCharList( 8812,  8853) # 8853 - 8875 broken
mathOps        += genCharList( 8876,  8920) # 8920, 8921 broken
mathOps        += genCharList( 8922,  8942) # 8942 - 8945 broken
mathOps        += genCharList( 8946,  8960)

japanese        = genCharList(65382, 65437) # half width katakana (ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜ)

charList = basicLatinChars + greekChars + cyrillicChars + mathOps
