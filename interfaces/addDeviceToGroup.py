from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.codecSwitcher import codecSwitcher
from utils.executeCmd import executeCmdSp
import sys,os

# python addDeviceToGroup.py 192.168.1.137 /dev/loop0 highSpeedGroup

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
    deviceLocation = arg[0]
    deviceName = arg[1]
    groupName = cswitcher.getEncode(arg[2])
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    gmConf = cHelper.getGroupMConf().get(groupName)
    if gmConf == None:
        print "Group do not exist"
        print "failed1failed2failed"
        sys.exit(1)
    providersConf = cHelper.getProviderConf()
    providerID = deviceName+deviceLocation
    for groupProvidersConf in providersConf.values():
        if providerID in groupProvidersConf.keys():
            print "Storage Device have been already added into system!"
            print "failed1failed2failed"
            sys.exit(1)
    startProviderCmd = "ssh -t root@"+deviceLocation+" \"python "+path+"main.py startProvider "+deviceName+" "+groupName+"\""
    out = executeCmd(startProviderCmd)
    if out.find("706errorKEY") >= 0:
        print "failed1failed2failed"
        sys.exit(1)
    gmIP = gmConf.get("gmIP")
    extendGroupCmd = "ssh -t root@"+gmIP+" \"python "+path+"main.py extendGroup "+groupName+"\""
    out = executeCmd(extendGroupCmd)
    if out.find("706errorKEY") >= 0:
        print "failed1failed2failed"
        sys.exit(1)

if __name__ == '__main__':
    deviceLocation = sys.argv[1]
    deviceName = sys.argv[2]
    groupName = sys.argv[3]
    run([deviceLocation, deviceName, groupName])
