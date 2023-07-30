
def genCharList(unicode_start, unicode_end):
    return [chr(i) for i in range(unicode_start, unicode_end)]


basicLatinChars = genCharList(48, 127)

greekChars = genCharList(910, 930) # 930 broken
greekChars += genCharList(931, 1024)

cyrillicChars = genCharList(1024, 1154)

japanese = genCharList(65382, 65437) # half width katakana ()
# basicLatin + katakana = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜ0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~"

charList = basicLatinChars + greekChars + cyrillicChars
