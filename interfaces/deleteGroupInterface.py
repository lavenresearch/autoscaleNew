from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.codecSwitcher import codecSwitcher
from utils.executeCmd import executeCmdSp
import sys,os

# python main.py deleteGroupInterface groupname

def executeCmd(cmd):
    logger = autoscaleLog(__file__)
    print cmd
    #cmd = unicode(cmd,'utf-8')
    print [cmd]
    output = executeCmdSp(cmd)
    print output
    logger.writeLog(cmd)
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    cswitcher = codecSwitcher()
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    groupName = cswitcher.getEncode(arg[0])
    gmsConf = cHelper.getGroupMConf()
    gmConf = gmsConf.get(groupName)
    if gmConf == None:
        print "group do not exist"
        return False
    gmIP = gmConf.get("gmIP")
    print gmIP
    print path
    print groupName
    deleteGroupCmd = u"ssh -t root@"+gmIP+u" \"python "+path+u"main.py deleteGroup "+groupName+u"\""
    executeCmd(deleteGroupCmd)

if __name__ == '__main__':
    groupName = sys.argv[1]
    run([groupName])
