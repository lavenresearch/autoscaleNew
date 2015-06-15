from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.groupManager import groupManager
from utils.codecSwitcher import codecSwitcher
import sys,os

# python main.py clearGroup.py highSpeedGroup

class clearGroup():
    groupName = ""
    groupManager = None
    cswitcher = None
    def __init__(self, args):
    	self.cswitcher = codecSwitcher()
        self.groupName = self.cswitcher.getEncode(args[0])
        self.groupManager = groupManager(self.groupName)
        self.logger = autoscaleLog(__file__)
    def run(self):
	self.groupManager.clearGroup()

