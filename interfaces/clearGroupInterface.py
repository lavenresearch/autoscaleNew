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
    logger.writeLog(cmd)
    #output = os.popen(cmd).read()
    output = executeCmdSp(cmd)
    print output
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
        print "failed1failed2failed"
        return False
    gmIP = gmConf.get("gmIP")
    clearGroupCmd = "ssh -t root@"+gmIP+" \"python "+path+"main.py clearGroup "+groupName+"\""
    out = executeCmd(clearGroupCmd)
    if out.find("706errorKEY") >= 0:
        print "failed1failed2failed"
        sys.exit(1)

if __name__ == '__main__':
    groupName = sys.argv[1]
    run([groupName])
