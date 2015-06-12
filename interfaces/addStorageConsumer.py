from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os

# python addStorageConsumer.py user1 consumerLocation

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
    userName = arg[0]
    consumerLocation = arg[1]
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    cmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py startConsumer "+userName+"\""
    userConsumers = cHelper.getUserConsumers()
    userC = userConsumers.get(userName)
    if userC == None:
        userC = []
    if consumerLocation in userC:
        print "consumer already exist!"
        return False
    userC.append(consumerLocation)
    userConsumers[userName] = userC
    cHelper.setUserConsumers(userConsumers)
    executeCmd(cmd)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    run([consumerLocation])
