#coding=utf-8
import re
def chineseHash(s):
    ufts = unicode(s,'utf-8')
    zhPattern = re.compile([\u4e00-\u9fa5])
    match = zhPattern.search(ufts)
    if match == True:
        groupNameHash = str(abs(hash(s)))
        return 'group'+groupNameHash
    else:
        return s
if __name__=='__main__':
    a = "死了看得见发的"
    print chineseHash(a)
    print chineseHash("skjdf")
