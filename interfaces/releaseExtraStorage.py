from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.executeCmd import executeCmdSp
import sys,os

# python releaseExtraStorage.py 192.168.3.137 /dev/sdb

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
    consumerLocation = arg[0]
    localDeviceMap = arg[1]
    sConf = staticConfig()
    path = sConf.getPath()
    releaseStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py releaseStorage "+localDeviceMap+"\""
    out = executeCmd(releaseStorageCmd)
    if out.find("706errorKEY") >= 0:
        print "failed1failed2failed"
        sys.exit(1)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    localDeviceMap = sys.argv[2]
    run([consumerLocation, localDeviceMap])
