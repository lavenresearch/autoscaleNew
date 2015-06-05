from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
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
    output = os.popen(cmd).read()
    print output
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    sConf = staticConfig()
    path = sConf.getPath()
    consumerLocation = arg[0]
    stepSize = arg[1]
    tagList = arg[2:]

    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        return False
    groupName = groupList[0]
    requestStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py requestStorage "+groupName+" "+str(stepSize)+"\""
    output = executeCmd(requestStorageCmd)
    deviceMap = output.split("\n")[-1]
    releaseCandidateKey = deviceMap+"@"+consumerLocation
    releaseCandidates = cHelper.getReleaseCandidates()
    releaseCandidates[releaseCandidateKey] = int(stepSize)
    cHelper.setReleaseCandidates(releaseCandidates)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    stepSize = sys.argv[2]
    tag1 = sys.argv[3]
    tag2 = sys.argv[4]
    run([consumerLocation, stepSize, tag1, tag2])
