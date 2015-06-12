from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.groupManager import groupManager
import sys,os

# python main.py deleteGroup.py highSpeedGroup

class deleteGroup():
    groupName = ""
    groupManager = None
    def __init__(self, args):
        self.groupName = args[0]
        self.groupManager = groupManager(self.groupName)
        self.logger = autoscaleLog(__file__)
    def run(self):
        self.groupManager.deleteGroup()

