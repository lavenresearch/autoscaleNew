#coding=utf-8
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.groupManager import groupManager
from utils.codecSwitcher import codecSwitcher
import sys,os

# python main.py deleteGroup.py highSpeedGroup

class deleteGroup():
    cswitcher = None
    groupName = ""
    groupManager = None
    def __init__(self, args):
        self.cswitcher = codecSwitcher()
        self.groupName = self.cswitcher.getEncode(args[0])
        print [self.groupName]
        self.groupManager = groupManager(self.groupName)
        self.logger = autoscaleLog(__file__)
    def run(self):
        self.groupManager.deleteGroup()

