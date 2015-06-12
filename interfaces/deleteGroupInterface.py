from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os

# python main.py deleteGroupInterface groupname

def executeCmd(cmd):
    logger = autoscaleLog(__file__)
    print cmd
    logger.writeLog(cmd)
    output = os.popen(cmd).read()
    print output
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    groupName = arg[0]
    gmsConf = cHelper.getGroupMConf()
    gmConf = gmsConf.get(groupName)
    if gmConf == None:
        print "group do not exist"
        return False
    gmIP = gmConf.get("gmIP")
    print gmIP
    print path
    print groupName
    deleteGroupCmd = "ssh -t root@"+gmIP+" \"python "+path+"main.py deleteGroup "+groupName+"\""
    executeCmd(deleteGroupCmd)

if __name__ == '__main__':
    groupName = sys.argv[1]
    run([groupName])
