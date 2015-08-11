import os
from utils.staticConfig import staticConfig

def executeCmd(cmd):
    print cmd
    output = os.popen(cmd).read()
    print output
    return output



def run():
    sConf = staticConfig()
    iplist = sConf.getAllNodesList()
    print iplist
    # iplist = ["192.168.0.98","192.168.0.99","192.168.16.122"]
    cmd = "ssh-copy-id -i root@"
    executeCmd("ssh-keygen -t rsa")
    for ip in iplist:
        executeCmd(cmd+ip)
