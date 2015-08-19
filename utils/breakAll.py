import os
from utils.staticConfig import staticConfig

def executeCmd(cmd):
    print cmd
    output = os.popen(cmd).read()
    print output
    return output

# def remoteCmd(rcmd,remoteip):
    # cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
    # return executeCmd(cmd)

def run():
    sConf = staticConfig()
    iplist = sConf.getAllNodesList()
    print iplist
    # iplist = ["192.168.0.98","192.168.0.99","192.168.16.122"]
    cmd = "ssh-copy-id -i root@"
    # for ip1 in iplist:
        # remoteCmd("ssh-keygen -t rsa",ip1)
        # for ip in iplist:
            # remoteCmd(cmd+ip,ip1)
    for ip in iplist:
        executeCmd(cmd+ip)
