from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os
import json

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
    username = arg[0]
    logger = autoscaleLog(__file__)
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    consumersConf = cHelper.getConsumerConf()
    userConsumers = cHelper.getUserConsumers()
    consumers = userConsumers.get(username)
    if consumers == None:
        consumers = []
    userConsumersConf = {}
    for consumer in consumers:
        conf = consumersConf.get(consumer)
        if conf != None:
            userConsumersConf[consumer] = conf
    logger.writeLog(userConsumersConf)
    print json.dumps(userConsumersConf)
    logger.shutdownLog()

if __name__ == '__main__':
    run([])
