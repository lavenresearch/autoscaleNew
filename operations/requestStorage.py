from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.storageConsumer import storageConsumer
from interfaces import getUsageInfo
import sys,os

class requestStorage():
    groupName = ""
    stepSize = 0
    sConsumer = None
    def __init__(self, args):
        print args
        self.groupName = args[0]
        self.stepSize = args[1]
        self.mode = args[2]
        self.sConsumer = storageConsumer()
    def run(self):
        sConf = staticConfig()
        infoCLocation = sConf.getInfoCLocation()
        cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
        currentUsageInfo = getUsageInfo.run([])
        asize = currentUsageInfo.get(self.groupName).get('groupSize')
        asize = int(asize)
        ssize = int(self.stepSize)
        if ssize > asize:
            print "do not have enough storage space stepSize:%d and asize:%d" % (ssize,asize)
            return False
        newDevices = self.sConsumer.requestStorage(self.groupName,self.stepSize,self.mode)
        print str(newDevices)
