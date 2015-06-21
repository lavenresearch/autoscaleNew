from utils.staticConfig import staticConfig
import redis

def run(arg):
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    ip = infoCLocation.get("ipInfoC")
    port = infoCLocation.get("portInfoC")
    redisClient = redis.StrictRedis(host= ip,port = port,db =0)
    print redisClient.get("providerInformation")
