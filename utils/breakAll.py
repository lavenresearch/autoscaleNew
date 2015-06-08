import os

def executeCmd(cmd):
    print cmd
    output = os.popen(cmd).read()
    print output
    return output



def run():
    iplist = ["192.168.16.122","192.168.16.123","192.168.16.124"]
    cmd = "ssh-copy-id -i root@"
    executeCmd("ssh-keygen -t rsa")
    for ip in iplist:
        executeCmd(cmd+ip)
