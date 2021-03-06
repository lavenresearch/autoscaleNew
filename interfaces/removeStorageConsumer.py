from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.executeCmd import executeCmdSp
import sys,os

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
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    consumersConf = cHelper.getConsumerConf()
    consumerConf = consumersConf.get(consumerLocation)
    for localDeviceConf in consumerConf.get("extraDevicesList"):
        localDeviceMap = localDeviceConf.get("localDeviceMap")
        if localDeviceMap == None:
            continue
        localDeviceMap = localDeviceMap.pop(0)
        if localDeviceMap == None:
            continue
        releaseStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py releaseStorage "+localDeviceMap+"\""
        out = executeCmd(releaseStorageCmd)
        if out.find("706errorKEY") >= 0:
            print "failed1failed2failed"
            sys.exit(1)
    del consumersConf[consumerLocation]
    cHelper.setConsumerConf(consumersConf)
    userConsumers = cHelper.getUserConsumers()
    for user, uConsumers in userConsumers.items():
        if consumerLocation in uConsumers:
            ucs = uConsumers
            ucs.remove(consumerLocation)
            userConsumers[user] = ucs
    cHelper.setUserConsumers(userConsumers)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    run([consumerLocation])
