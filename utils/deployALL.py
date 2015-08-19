from utils.staticConfig import staticConfig
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os
# cmd = "mkdir -p "+path
# cmd = "scp -r ../ "+destinationIP+":"+path
# initCmd = []

class deployALL():
    destinationIP = ""
    path = ""
    initialCmds = ["service iptable stop","setenforce 0","lvmconf --disable-cluster","yum install scsi-target-utils.x86_64 iscsi-initiator-utils.x86_64 reiserfs-utils --nogpgcheck -y"]
    # initialCmds = ["service iptable stop","setenforce 0"]
    currentPwd = "./"
    def __init__(self, arg):
        self.destinationIP = arg[0]
        sConf = staticConfig()
        self.path = sConf.getPath()
        self.executeCmd("ssh-copy-id -i root@"+self.destinationIP)
        self.currentPwd = os.popen("pwd").read()
        self.currentPwd = self.currentPwd.split("\n")[0]+"/"
        print self.currentPwd

    def executeCmd(self, cmd):
        logger = autoscaleLog(__file__)
        print cmd
        logger.writeLog(cmd)
        output = os.popen(cmd).read()
        print output
        logger.writeLog(output)
        logger.shutdownLog()
        return output

    def executeRemoteCmd(self, rcmd , remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        self.executeCmd(cmd)

    def run(self):
        rcmd = "rm -rf "+self.path
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "mkdir -p "+self.path
        self.executeRemoteCmd(rcmd, self.destinationIP)
        cmd = "scp -r "+self.currentPwd+"* root@"+self.destinationIP+":"+self.path
        self.executeCmd(cmd)
        rcmd = "dos2unix "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "chmod +x "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        for rcmd in self.initialCmds:
            self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "tar -zxvf "+self.path+"packages/redis-2.10.3.tar.gz -C "+self.path+"packages/"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "cd "+self.path+"packages/redis-2.10.3/ && python setup.py install"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        self.executeRemoteCmd("cp "+self.path+"core/scst* /usr/local/bin" ,self.destinationIP)



