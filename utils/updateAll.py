import os,sys
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog

class updateAll():
    destinationIP = ""
    path = ""
    webPath = "/opt/lampp/htdocs/myweb/php/mod/manage/"
    webIP = "192.168.16.102"
    def __init__(self, arg):
        self.destinationIP = arg
        sConf = staticConfig()
        self.path = sConf.getPath()
        # self.executeCmd("ssh-copy-id -i "+self.destinationIP)

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
	currentPwd = os.popen("pwd").read()
        currentPwd = currentPwd.split("\n")[0]+"/"
        cmd = "scp -r "+currentPwd+"* root@"+self.destinationIP+":"+self.path
        self.executeCmd(cmd)
        rcmd = "dos2unix "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "chmod +x "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)
    def updateWeb(self):
        currentPwd = os.popen("pwd").read()
        currentPwd = currentPwd.split("\n")[0]+"/*"
        cmd = "scp -r "+currentPwd+"* root@"+self.webIP+":"+self.webPath
        self.executeCmd(cmd)
        rcmd = "dos2unix "+self.webPath+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.webIP)
        rcmd = "chmod +x "+self.webPath+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.webIP)


def run():
    ua = updateAll("0.0.0.0")
    ua.updateWeb()
    a = raw_input("input yes to continue:")
    if a != "yes":
        sys.exit()
    sConf = staticConfig()
    iplist = sConf.getAllNodesList()
    print iplist
    # iplist = ["192.168.0.99","192.168.0.98","192.168.16.122"]
    for ip in iplist:
        ua = updateAll(ip)
        ua.run()
