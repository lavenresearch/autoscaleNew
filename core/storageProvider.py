from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.executeCmd import executeCmdSp
import os,sys
import socket
import fcntl
import struct
import json

class storageProvider():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    hostIP = ""
    conf = {}
    initialCmds = []
    iscsiTargetType = ""
    logger = None
    path = "/usr/local/src/suyiAutoscale/src/"
    storageProviderConf = {}
    def __init__(self,deviceName,groupName):
        sConf = staticConfig()
        self.ipInfoC = sConf.getInfoCLocation()["ipInfoC"]
        self.iscsiTargetType = sConf.getTargetType("storageProvider")
        self.portInfoC = sConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        hostName = self.executeCmd("hostname")
        iframe = sConf.getHostInterface(hostName)
        self.hostIP = self.getLocalIP(iframe)
        self.conf["deviceName"] = deviceName
        self.conf["deviceGroup"] = groupName
        self.loadConf()
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        self.logger = autoscaleLog(__file__)
        sConf = staticConfig()
        self.path = sConf.getPath()+"core/"
        confPath = sConf.getPath()+"conf/storageProviderConf.json"
        with open(confPath,"r") as fspc:
            self.storageProviderConf = json.loads(fspc.read())

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def getDeviceSize(self,devicepathDev):
        print devicepathDev
        deviceType = len(devicepathDev.split("/"))
        if deviceType >= 3:
            lvDeviceName = devicepathDev.split("/")[-1]
            cmd = "lvs | grep "+lvDeviceName+" | awk '{print $4}'"
            size = self.executeCmd(cmd)
            s = size.split('\n')
            print "************************"
            print size
            print "************************"
            for si in s:
                if si[-1] == "G" or si[-1] == "M" or si[-1] == "T":
                    size = si
                    break
            sizeNum = float(size[:-1])
            sizeM = size[-1]
            if sizeM == "T":
                return int(sizeNum*1024*1024)
            elif sizeM == "G":
                return int(sizeNum*1024)
            else:
                return int(sizeNum)
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0)) # in MB

    def executeCmd(self,cmd):
        print cmd
        #tmp = os.popen(cmd).read()
        tmp = executeCmdSp(cmd)
        print tmp
        return tmp

    def loadConf(self):
        hostName = self.executeCmd("hostname").split("\n")[0]
        deviceNameShort = self.conf["deviceName"].split("/")[-1]
        self.conf["deviceLocation"] = self.hostIP
        self.conf["deviceIQN"] = "iqn.dsal.storage:"+hostName+"."+deviceNameShort
        deviceType = self.storageProviderConf.get(self.conf["deviceName"])
        if deviceType == None:
            self.conf["deviceType"] = "localDisk"
        elif deviceType.get("deviceType") == None:
            self.conf["deviceType"] = "localDisk"
        else:
            self.conf["deviceType"] = deviceType.get("deviceType")
        self.conf["deviceSize"] = self.getDeviceSize(self.conf["deviceName"])
        atid = self.cHelper.getAvailTid()
        tid = atid.get(self.hostIP)
        if tid == None:
            tid = 100
        self.conf["tid"] = str(tid)
        atid[self.hostIP] = tid+1
        self.cHelper.setAvailTid(atid)
        gmsConf = self.cHelper.getGroupMConf()
        gmConf = gmsConf.get(self.conf["deviceGroup"])
        if gmConf == None:
            print "Storage group do not exist!"
            print "706errorKEY"
            self.logger.writeLog("Storage group do not exist!")
            self.shutdownLog()
            sys.exit(1)
        self.conf["groupManagerIP"] = gmConf.get("gmIP")

    def exportStorage(self):
        cmd = self.path+"deployStorage.sh "+self.conf["deviceIQN"]+" "+self.conf["deviceName"]+" "+self.conf["tid"]+" "+self.conf["groupManagerIP"]
        out = self.executeCmd(cmd)
        if out.find("Error") >= 0 or out.find("FATAL") >=0 or out.find("error") >= 0:
            print "target building failed"
            print "706errorKEY"
            sys.exit(1)   
        self.updateInfoCenter(self.conf,'add')
        self.logger.shutdownLog()

    def stopProvider(self):
	confRemote = self.cHelper.getProviderConf()
	groupConfRemote = confRemote.get(self.conf["deviceGroup"])
        if groupConfRemote == None:
            return False
	deviceConfRemote = groupConfRemote.get(self.conf["deviceName"]+self.hostIP)
	if deviceConfRemote == None:
	    return False
        tid = deviceConfRemote.get("tid")
        if self.iscsiTargetType == "tgt":
            cmdStopProvider = "tgtadm --lld iscsi --op delete --mode target --tid "+tid
        elif self.iscsiTargetType == "scst":
            deviceIQN = deviceConfRemote.get("deviceIQN")
            deviceName = deviceConfRemote.get("deviceName")
            groupManagerIP = deviceConfRemote.get("groupManagerIP")
            cmdStopProvider = "scst-remove.sh "+deviceIQN+" "+tid+" "+tid+" 0 "+deviceName+" "+groupManagerIP
        else:
            print "iscsi Target Type do not match"
            print "706errorKEY"
            sys.exit()
        out = self.executeCmd(cmdStopProvider)
        if out.find("Error") >= 0 or out.find("FATAL") >=0 or out.find("error") >= 0:
            print "target remove failed"
            print "706errorKEY"
            sys.exit(1)
	atid = self.cHelper.getAvailTid()
        tid = atid.get(self.hostIP)
        if tid != None:
            atid[self.hostIP] = tid-1
            self.cHelper.setAvailTid(atid)

        self.updateInfoCenter(self.conf,'remove')


    def updateInfoCenter(self,conf,mode):
        '''
        conf in remote.
        {
            groupname1:{deviceID1:conf1,deviceID2:conf2,},
            groupname2:{},
        }
        '''
        confRemote = self.cHelper.getProviderConf()
        confGroupRemote = confRemote.get(conf["deviceGroup"])
        if confGroupRemote == None:
            confGroupRemote = {}
        deviceID = conf["deviceName"]+conf["deviceLocation"]
        if mode == "add":
            confGroupRemote[deviceID] = conf
        if mode == "remove":
            confGroupRemote.pop(deviceID)
        confRemote[conf["deviceGroup"]] = confGroupRemote
        self.cHelper.setProviderConf(confRemote)

if __name__ == '__main__':
    deviceName = "/dev/loop0"
    groupName = "newHighSpeedGroup"
    sProvider = storageProvider( deviceName, groupName)
    sProvider.exportStorage()
