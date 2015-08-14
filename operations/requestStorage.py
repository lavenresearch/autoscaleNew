from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.codecSwitcher import codecSwitcher
from core.storageConsumer import storageConsumer
from interfaces import getUsageInfo
import sys,os

class requestStorage():
    groupName = ""
    stepSize = 0
    sConsumer = None
    cswitcher = None
    def __init__(self, args):
        print args
        self.cswitcher = codecSwitcher()
        self.groupName = self.cswitcher.getEncode(args[0])
        self.stepSize = args[1]
        self.mode = args[2]
        self.sConsumer = storageConsumer()
    def run(self):
        sConf = staticConfig()
        infoCLocation = sConf.getInfoCLocation()
        cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
        newDevices = self.sConsumer.requestStorage(self.groupName,self.stepSize,self.mode)
        if newDevices == []:
            print "706errorKEY"
            return
        print str(newDevices)
