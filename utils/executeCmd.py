#coding=utf-8
import subprocess

def executeCmdSp(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    p.wait()
    return p.stdout.read()
if __name__=='__main__':
    cmd = "ssh -t root@192.168.12.56 \"ls /home/pi/Desktop/000.云存储平台验收文档/\""
    print cmd
    output = executeCmdSp(cmd)
    print output
