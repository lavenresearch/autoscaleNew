import redis,subprocess,json
from utils.staticConfig import staticConfig

def executeCmd(cmd):
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    p.wait()
    output = p.stdout.read()
    print output
    return output

#if __name__ == "__main__":
def run():
    cmd = "ifconfig | grep inet\ addr:192.168 | awk '{print $2}' | cut -d \":\" -f 2"
    ip = executeCmd(cmd).split('\n')[0]
    cmd = "ls -l /dev/sd* | grep \"/dev/sd\" | awk \'{print $9}\'"
    devL1 = []
    devL1 = executeCmd(cmd).split('\n')
    print devL1
    for x in range(len(devL1)):
        print x,devL1[x]
    devL11 = devL1[0:]
    for x in range(len(devL11)):
        d =  devL11[x]
        print d
        if d.find('sda') != -1:
            print "remove %s"%(d)
            devL1.remove(d)
	if d == "":
	    devL1.remove(d)
    cmdLV = "lvs | grep raid | awk \'{print $1}\'"
    cmdVG = "lvs | grep raid | awk \'{print $2}\'"
    lvL = executeCmd(cmdLV).split('\n')
    vgL = executeCmd(cmdVG).split('\n')
    devL2 = []
    for i in xrange(len(lvL)):
	if vgL[i].find('raid') == -1:
	    continue
        devL2.append("/dev/%s/%s"%(vgL[i],lvL[i]))
    devLall = []
    devLall = devL1 + devL2
    sconf = staticConfig()
    infoC = sconf.getInfoCLocation()
    hostip = infoC.get("ipInfoC")
    hostport = infoC.get("portInfoC")
    redisClient = redis.StrictRedis(host = hostip, port=hostport, db=0)
    remotePInfo = redisClient.get("providerInformation")
    if remotePInfo == None:
        remotePInfo = "{}"
    remotePInfo = json.loads(remotePInfo)
    remotePInfo[ip] = devLall
    remotePInfo = json.dumps(remotePInfo)
    redisClient.set("providerInformation",remotePInfo)
    print remotePInfo
