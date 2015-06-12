from utils.autoScaleLog import autoscaleLog
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from interfaces import getUsageInfo
import sys,os,time

class timeManager():
    sConf = None
    cHelper = None
    logger = None
    time = 0
    def __init__(self):
        self.logger = autoscaleLog(__file__)
        self.sConf = staticConfig()
        infoCLocation = self.sConf.getInfoCLocation()
        self.cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
        self.getTime()
    def setTime(self, time):
    	self.time = int(time)
    	self.cHelper.setTimeManager(self.time)
    def getCurrentTime(self):
    	curTime = int(time.time())
    	return curTime
    def getTime(self):
    	self.time = self.cHelper.getTimeManager()
    	if self.time == None or self.time == -1:
    		self.time = self.getCurrentTime()
    	return self.time

def run(arg):
    tm = timeManager()
    print arg
    if len(arg) == 0:
        print tm.getTime()
	sys.exit(0)
    t = arg[0]
    tm.setTime(t)
    print tm.getTime()
