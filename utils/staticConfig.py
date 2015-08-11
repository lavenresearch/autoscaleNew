from utils.autoScaleLog import autoscaleLog
import random

class staticConfig():
    staticConf = {}
    logger = None
    def __init__(self):
        self.staticConf["allNodes"] = ["192.168.0.98","192.168.0.99","192.168.16.122","192.168.16.123"]
        self.staticConf["infoCLocation"] = {"ipInfoC":"192.168.16.123", "portInfoC":6379}
        self.staticConf["path"] = "/opt/suyi/autoscale706kylin/"
        self.staticConf["gmCandidates"] = ["192.168.16.123"]
        self.staticConf["hostInterfaceMap"] = {"ds01":"eth0",
                                               "ds02":"eth0",
                                               "ds03":"eth0",
                                               "ds04":"eth0",
                                               "0-98":"bond0",
                                               "0-99":"bond0"}
        self.staticConf["iscsiTargetType"] = {"groupManager":"scst",
                                              "storageProvider":"scst"} # another option is "tgt"
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
    def getTargetType(self,role):
        iscsiTargetTypes = self.staticConf.get("iscsiTargetType")
        if role == "groupManager":
            return iscsiTargetTypes.get("groupManager")
        elif role == "storageProvider":
            return iscsiTargetTypes.get("storageProvider")
        else:
            return None
    def getAllNodesList(self):
        return self.staticConf["allNodes"]
