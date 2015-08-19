from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from interfaces import getInfo
import sys,os
import json
import pprint


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
    path = sConf.getPath()
    logFile = path+"suyiAutoscale.log"
    try:
        mode = arg.pop(0)
        print mode
        if mode == "status":
            allInfo = {}
            allInfo = getInfo.run([])
            print json.dumps(allInfo,indent=1)
            return
        elif mode == "log":
            logPath = arg.pop()
            if logPath[-1] == "/":
                logFile = logPath + "suyiAutoscale.log"
            else:
                logFile = logPath + "/suyiAutoscale.log"
            print logFile
            with open(logFile,"r") as log:
                print log.read().replace('\\n','\n').replace('\\r','\r')
                return
        else:
            print "Wrong mode"
            return
    except:
        print 'wrong arguments'
        return

if __name__ == '__main__':
    run([])
