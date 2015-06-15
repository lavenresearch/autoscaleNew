from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.codecSwitcher import codecSwitcher
from core.storageProvider import storageProvider
import sys
import json

class startProvider():
    deviceName = ""
    groupName = ""
    sProvider = None
    cswitcher = None
    def __init__(self,args):
        print args
        self.cswitcher = codecSwitcher()
        self.deviceName = args[0]
        self.groupName = self.cswitcher.getEncode(args[1])
        self.sProvider = storageProvider(self.deviceName,self.groupName)
    def run(self):
        self.sProvider.exportStorage()
