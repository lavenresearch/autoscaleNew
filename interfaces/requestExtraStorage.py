from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
from utils.codecSwitcher import codecSwitcher
from utils.executeCmd import executeCmdSp
from interfaces import getUsageInfo
import sys,os

# Needed arguments including:
#
# consumerIP : 192.168.1.162
# stepSize   : 100 (in MB)
# tag1       : highspeed
# tag2       : security
#
# the program will add $extendSize storage from $deviceGroup for apppserver $appserverIP
#
# after operation, update the information on configuration server.


# For example:
#
# python requestExtraStorage.py 192.168.1.162 100 highspeed security
#
# in which the "100" means 100MB

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
    cswithcer = codecSwitcher()
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    consumerLocation = arg[0]
    stepSize = arg[1]
    tagList = cswithcer.getEncode(arg[2:])

    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        print "failed1failed2failed"
        sys.exit(1)
    groupName = None
    for groupN in groupList:
        currentUsageInfo = getUsageInfo.run([])
        gsize = currentUsageInfo.get(groupN).get('groupSize')
        usize = currentUsageInfo.get(groupN).get('usedSize')
        asize = long(gsize) - long(usize) - 100
        ssize = long(stepSize)
        if ssize <= asize:
            groupName = groupN
            break
    if groupName == None:
        print "Do not have enough storage space requestSize:%d and asize:%d" % (ssize,asize)
        print "failed1failed2failed"
        sys.exit(1)
    requestStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py requestStorage "+groupName+" "+str(stepSize)+" extra\""
    out = executeCmd(requestStorageCmd)
    if out.find("706errorKEY") >= 0:
        print "failed1failed2failed"
        sys.exit(1)
    # deviceMap = output.split("\n")[-1]

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    stepSize = sys.argv[2]
    tag1 = sys.argv[3]
    tag2 = sys.argv[4]
    run([consumerLocation, stepSize, tag1, tag2])
