from utils.autoScaleLog import autoscaleLog
import random

class staticConfig():
    staticConf = {}
    logger = None
    def __init__(self):
        self.staticConf["allNodes"] = ["192.168.0.98","192.168.0.97","192.168.0.99",
                                       "192.168.16.121","192.168.16.122","192.168.16.123","192.168.16.124",
                                       "192.168.16.101","192.168.16.102","192.168.16.103","192.168.16.104",
                                       "192.168.16.105","192.168.16.106","192.168.1.88",
                                       "192.168.16.111","192.168.16.112","192.168.16.113","192.168.16.114"]
        self.staticConf["infoCLocation"] = {"ipInfoC":"192.168.16.123", "portInfoC":6379}
        self.staticConf["path"] = "/opt/suyi/autoscale706kylin/"
        self.staticConf["gmCandidates"] = ["192.168.16.111"]
        self.staticConf["hostInterfaceMap"] = {"ds01":"eth0",
                                               "ds02":"eth0",
                                               "ds03":"eth0",
                                               "ds04":"eth0",
                                               "0-97":"bond0",
                                               "0-98":"bond0",
                                               "0-99":"bond0",
                                               "client01":"eth3",
                                               "client02":"eth3",
                                               "client03":"eth9",
                                               "client04":"eth5",
                                               "client05":"eth2",
                                               "client06":"eth3",
                                               "mds01":"eth0",
                                               "mds02":"eth0",
                                               "mds03":"eth0",
                                               "mds04":"eth0",
                                               "jm":"eth0"}
        self.staticConf["iscsiTargetType"] = {"groupManager":"tgt",
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
