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
    logger = autoscaleLog(__file__)
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    consumersConf = cHelper.getConsumerConf()
    providersConf = cHelper.getProviderConf()
    tagsManager = cHelper.getTagsManager()
    allConf = {}
    allConf["dev"] = providersConf
    allConf["appserver"] = consumersConf
    allConf["tags"] = tagsManager
    logger.writeLog(allConf)
    print json.dumps(allConf)
    logger.shutdownLog()
    return allConf

if __name__ == '__main__':
    run([])
