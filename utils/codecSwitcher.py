#coding=utf-8
import hashlib
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
        if isinstance(s,str) == True:
            return unicode(s, self.codeName)
        else:
            return unicode(str(s), self.codeName)
    def getHash(self, s):
        if isinstance(s,unicode) == True:
            smd5 = hashlib.md5(s.encode('utf8'))
            smd5v = smd5.hexdigest()
            return str(smd5v)
        elif isinstance(s,str) == True:
            s = unicode(s,self.codeName)
            smd5 = hashlib.md5(s.encode('utf8'))
            smd5v = smd5.hexdigest()
        else:
            s = str(s)
            smd5 = hashlib.md5(s.encode('utf8'))
            smd5v = smd5.hexdigest()
        return str(smd5v)

if __name__ == '__main__':
    cswitcher = codecSwitcher()
    a = '到了就阿斗开房间阿地方'
    print [a]
    print a
    b = cswitcher.getEncode(a)
    print [b]
    b = cswitcher.getHash(a)
    print b
    a = ["大大的","弹道导弹"]
    b = cswitcher.getEncode(a)
    print a
    print b
    b = cswitcher.getHash(a)
    print b
    c = [u'本来就是']
    b = cswitcher.getEncode(c)
    print b
    b = cswitcher.getHash(11111111111)
    print b
