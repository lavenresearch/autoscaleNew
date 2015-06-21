from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.executeCmd import executeCmdSp
from utils.codecSwitcher import codecSwitcher
import os,glob,re,time,sys
import socket
import fcntl
import struct

class storageConsumer():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    conf = {}
    hostIP = ""
    logger = None
    # initialCmds = ["dos2unix *","chmod +x *","service iptable stop","setenforce 0","lvmconf --disable-cluster"]
    initialCmds = []
    def __init__(self):
        self.logger = autoscaleLog(__file__)
        sConf = staticConfig()
        self.ipInfoC = sConf.getInfoCLocation()["ipInfoC"]
        self.portInfoC = sConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        hostName = self.executeCmd("hostname")
        iframe = sConf.getHostInterface(hostName)
        self.hostIP = self.getLocalIP(iframe)
        self.loadConf()
        for cmd in self.initialCmds:
            self.executeCmd(cmd)


    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def executeCmd(self,cmd):
        print cmd
        self.logger.writeLog(cmd)
        #tmp = os.popen(cmd).read()
        tmp = executeCmdSp(cmd)
        print tmp
        self.logger.writeLog(tmp)
        return tmp

    def remoteCmd(self,rcmd,remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        return self.executeCmd(cmd)

    def loadConf(self):
        consumerID = self.hostIP
        remoteConf = self.cHelper.getConsumerConf()
        remoteConsumerConf = remoteConf.get(consumerID)
        if remoteConsumerConf != None:
            self.conf = remoteConsumerConf
            return
        hostName = self.executeCmd("hostname").split("\n")[0]
        remoteIQN = "iqn.dsal.consumer:"+hostName+"."+"disk"
        remoteLV = "consumer"+hostName+"remoteLV"
        remoteDiskAmount = 0
        consumerLocation = self.hostIP
        self.conf["remoteIQN"] = remoteIQN
        self.conf["remoteLV"] = remoteLV
        self.conf["remoteDiskAmount"] = remoteDiskAmount
        self.conf["consumerLocation"] = consumerLocation
        self.conf["consumerID"] = consumerID
        # remoteConf[consumerID] = self.conf
        remoteConsumerConf = self.conf
        self.cHelper.setConsumerConf(remoteConf)

    def getDeviceSize(self,devicepathDev):
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0)) # in MB

    def getDevicesInfo(self):
        devices = []
        devicesDev = []
        dev_pattern = ['sd.*']
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    devices.append(device)
        for d in devices:
            dpathdev = "/dev/"+d.split("/")[-1]
            devicesDev.append(dpathdev)
        return devicesDev

    def requestStorage(self,groupName,stepSize,mode):
        extraDeviceConf = {}
        remoteConsumersConf = self.cHelper.getConsumerConf()
        remoteConsumerConf = remoteConsumersConf[self.conf["consumerID"]]
        remoteGroupManagersConf = self.cHelper.getGroupMConf()
        remoteGroupManagerConf = remoteGroupManagersConf[groupName]
        remoteConsumerConf["remoteDiskAmount"] += 1
        extraDeviceConf["remoteLV"] = remoteConsumerConf["remoteLV"]+str(remoteConsumerConf["remoteDiskAmount"])
        cswitcher = codecSwitcher()
        extraDeviceConf["remoteVG"] = cswitcher.getHash(groupName)+"VG"
        extraDeviceConf["remoteLVPath"] = "/dev/"+extraDeviceConf["remoteVG"]+"/"+extraDeviceConf["remoteLV"]
        extraDeviceConf["remoteIQN"] = remoteConsumerConf["remoteIQN"]+str(remoteConsumerConf["remoteDiskAmount"])
        extraDeviceConf["groupName"] = groupName
        extraDeviceConf["remoteSize"] = stepSize
        remoteGroupManagerConf["currentTid"] += 1
        extraDeviceConf["remoteTid"] = remoteGroupManagerConf["currentTid"]
        groupManagerIP = remoteGroupManagerConf["gmIP"]

        # createRemoteStorage

        self.remoteCmd("lvcreate -L "+str(extraDeviceConf["remoteSize"])+"M -n "+extraDeviceConf["remoteLV"]+" "+extraDeviceConf["remoteVG"], groupManagerIP)
        # self.remoteCmd("tgtadm --lld iscsi --op new --mode target --tid "+str(extraDeviceConf["remoteTid"])+" -T "+extraDeviceConf["remoteIQN"] , groupManagerIP)
        # self.remoteCmd("setenforce 0;tgtadm --lld iscsi --op new --mode logicalunit --tid "+str(extraDeviceConf["remoteTid"])+" --lun 1 -b "+extraDeviceConf["remoteLVPath"] , groupManagerIP)
        # self.remoteCmd("tgtadm --lld iscsi --op bind --mode target --tid "+str(extraDeviceConf["remoteTid"])+" -I "+self.hostIP , groupManagerIP)
        remoteIQN = extraDeviceConf["remoteIQN"]
        remoteTid = str(extraDeviceConf["remoteTid"])
        remoteLVPath = extraDeviceConf["remoteLVPath"]
        cmdScstCreate = "scst-create.sh "+remoteIQN+" "+remoteTid+" "+remoteTid+" 0 "+remoteLVPath+" "+self.hostIP 
        self.remoteCmd(cmdScstCreate,groupManagerIP)
        cmdScstRemove = "scst-remove.sh "+remoteIQN+" "+remoteTid+" "+remoteTid+" 0 "+remoteLVPath+" "+self.hostIP
        self.remoteCmd("echo "+cmdScstRemove+" >/root/"+remoteTid+".sh", groupManagerIP)

        # loadRemoteStorage

        baseDevices = self.getDevicesInfo()
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + groupManagerIP
        self.executeCmd(cmdDiscovery)
        cmdLogin = "iscsiadm -m node -T "+extraDeviceConf["remoteIQN"]+" --login"
        self.executeCmd(cmdLogin)
        time.sleep(5)
        devices = self.getDevicesInfo()
        newDevices = list(set(devices).difference(set(baseDevices)))
        print "baseDevice"+str(baseDevices)
        self.logger.writeLog("baseDevice"+str(baseDevices))
        print "allDevice"+str(devices)
        self.logger.writeLog("allDevice"+str(devices))
        print "newDevice"+str(newDevices)
        self.logger.writeLog("newDevice"+str(newDevices))
        if newDevices == []:
            print "Storage Load Failed"
            print "706errorKEY"
            self.logger.writeLog("Storage Load Failed")
            sys.exit()
        extraDeviceConf["localDeviceMap"] = newDevices

        # update Information center
        
        for d in newDevices:
            consuemrInfo = {"consumerLocation":self.hostIP,"localDeviceMap":str(d)}
            remoteGroupManagerConf["consumersLoaded"].append(consuemrInfo)
            if mode == "extra":
                releaseCandidateKey = str(d)+"@"+self.hostIP
                releaseCandidates = self.cHelper.getReleaseCandidates()
                if releaseCandidates == None:
                    releaseCandidates = {}
                releaseCandidates[releaseCandidateKey] = int(stepSize)
                self.cHelper.setReleaseCandidates(releaseCandidates)
        self.cHelper.setGroupMConf(remoteGroupManagersConf)
        remoteConsumerConf["extraDevicesList"].append(extraDeviceConf)
        self.cHelper.setConsumerConf(remoteConsumersConf)
        return newDevices

    def releaseStorage(self, localDeviceMap):
        remoteConf = self.cHelper.getConsumerConf()
        consumerID = self.conf["consumerID"]
        consumerConf = remoteConf[consumerID]
        devicesInfo = consumerConf["extraDevicesList"]
        deviceInfo = {}
        for d in devicesInfo:
            if localDeviceMap in d["localDeviceMap"]:
                deviceInfo = d
        if deviceInfo == {}:
            print "Device to be released do note exist!"
            print "706errorKEY"
            self.logger.writeLog("Device to be released do note exist!")
            self.logger.shutdownLog()
            sys.exit(1)
        devicesInfo.remove(deviceInfo)
        consumerConf["remoteDiskAmount"] -= 1
        groupMsConf = self.cHelper.getGroupMConf()
        groupMConf = groupMsConf.get(deviceInfo["groupName"])
        if groupMConf == None:
            print "group conf information do not exist"
            print "706errorKEY"
            self.logger.writeLog("group conf information do note exist!")
            self.logger.shutdownLog()
            sys.exit(1)
        gmIP = str(groupMConf["gmIP"])

        unloadDeviceCmd = "iscsiadm -m node -T "+deviceInfo["remoteIQN"]+" -p "+gmIP+" -u"
        self.executeCmd( unloadDeviceCmd)
        remoteTid = str(deviceInfo["remoteTid"])
        # self.remoteCmd("tgtadm --lld iscsi --op delete --mode target --tid "+remoteTid , gmIP)
        remoteIQN = deviceInfo["remoteIQN"]
        remoteLVPath = deviceInfo["remoteLVPath"]
        consumerIP = consumerConf["consumerLocation"]
        cmdScstRemove = "scst-remove.sh "+remoteIQN+" "+remoteTid+" "+remoteTid+" 0 "+remoteLVPath+" "+consumerIP
        self.remoteCmd(cmdScstRemove,gmIP)
        removeLVCmd = "lvchange -a n "+deviceInfo["remoteLVPath"]+" && lvremove "+deviceInfo["remoteLVPath"]
        self.remoteCmd(removeLVCmd, gmIP)
        self.cHelper.setConsumerConf(remoteConf)
        #remoteGroupManagersConf = self.cHelper.getGroupMConf()
        #remoteGroupManagerConf = remoteGroupManagersConf[groupName]        
        groupConsumerLoaded = groupMConf.get("consumersLoaded")
        if groupConsumerLoaded == None:
            print "groupConsumerLoaded key do not exist"
            print "706errorKEY"
            sys.exit(1)
        consuemrInfo = {"consumerLocation":self.hostIP,"localDeviceMap":localDeviceMap}
        groupConsumerLoaded.remove(consuemrInfo)
        self.cHelper.setGroupMConf(groupMsConf)
        releaseCandidates = self.cHelper.getReleaseCandidates()
	releaseCandidateKey = localDeviceMap+"@"+self.hostIP
	if releaseCandidates.has_key(releaseCandidateKey) == True:
            releaseCandidates.pop(releaseCandidateKey)
        self.cHelper.setReleaseCandidates(releaseCandidates)

if __name__ == '__main__':
    consumer = storageConsumer()
    groupName = "highSpeedGroup"
    stepSize = 100 #MB
    consumer.requestStorage( groupName, stepSize)
    consumer.releaseStorage("/dev/sdb")
