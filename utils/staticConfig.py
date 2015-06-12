from utils.autoScaleLog import autoscaleLog
import random

class staticConfig():
    staticConf = {}
    logger = None
    def __init__(self):
        self.staticConf["infoCLocation"] = {"ipInfoC":"192.168.16.123", "portInfoC":6379}
        self.staticConf["path"] = "/opt/suyi/autoscale706/"
        self.staticConf["gmCandidates"] = ["192.168.16.123"]
        self.staticConf["hostInterfaceMap"] = {"ds01":"eth0",
                                               "ds02":"eth0",
                                               "ds03":"eth0",
                                               "ds04":"eth0"}
        self.logger = autoscaleLog(__file__)
        self.logger.writeLog(self.staticConf)
        self.logger.shutdownLog()

    def getInfoCLocation(self):
        return self.staticConf["infoCLocation"]

    def getPath(self):
        return self.staticConf["path"]

    def getGroupMIP(self):
        gmip = random.choice(self.staticConf.get("gmCandidates"))
        return gmip
    def getHostInterface(self, hostname):
        hostnameShort = hostname.split("\n")[0].split(".")[0]
        hostInterfaceMap = self.staticConf["hostInterfaceMap"]
        return hostInterfaceMap[hostnameShort]
