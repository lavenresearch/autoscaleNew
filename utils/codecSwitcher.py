#coding=utf-8
class codecSwitcher():
    codeName = ""
    def __init__(self,codeName = 'utf-8'):
        self.codeName = codeName
    def getEncode(self, s):
        if isinstance(s,(list)):
            sNew = []
            for e in s:
                if isinstance(e,unicode) == True:
                    sNew.append(e)
                else:
                    sNew.append(unicode(e, self.codeName))
            return sNew
        if isinstance(s,unicode) == True:
            return s
        else:
            return unicode(s, self.codeName)

if __name__ == '__main__':
    cswitcher = codecSwitcher()
    a = '到了就阿斗开房间阿地方'
    print [a]
    print a
    b = cswitcher.getEncode(a)
    print [b]
    a = ["大大的","弹道导弹"]
    b = cswitcher.getEncode(a)
    print a
    print b
    c = [u'本来就是']
    b = cswitcher.getEncode(c)
    print b
