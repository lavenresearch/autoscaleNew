import redis,json

class configHelper():
    ipInfoC = ""
    portInfoC = 6379
    r = None
    groupManagerConfKey = "groupckey"
    providerConfKey = "pckey"
    comsumerConfKey = "cckey"
    availTidKey = "atidkey"
    userBookingKey = "ubookkey"
    timeslotBookingKey = "tsbookkey"
    releaseCandidatesKey = "rcandidateskey"
    tagsManagerKey = "tmkey"
    def __init__(self, ipInfoC, portInfoC):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.r = redis.StrictRedis( host=self.ipInfoC, port=self.portInfoC, db=0)

    def setConfig(self,key,value):
        print "\nSET:\n"+str(value)
        self.r.set(key,value)
    def getConfig(self,key):
        value = self.r.get(key)
        # print "\nGET:\n"+str(value)
        if value == None:
            value = '{}'
        return value

    def setGroupMConf(self,conf):
        '''
        group manager conf in redis:
        {
            groupname1:{"gmIP":"192.168.3.161","currentTid":152,"devicesLoaded":[deviceID1,deviceID2,]},
            groupname2:{},
        }
        '''
        self.setConfig(self.groupManagerConfKey,json.dumps(conf))
    def getGroupMConf(self):
        confJson = self.getConfig(self.groupManagerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf

    def setProviderConf(self,conf):
        '''
        provider conf in redis.
        {
            groupname1:{deviceID1:conf1,deviceID2:conf2,},
            groupname2:{},
        }
        '''
        self.setConfig(self.providerConfKey,json.dumps(conf))
    def getProviderConf(self):
        confJson = self.getConfig(self.providerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf

    def setConsumerConf(self,conf):
        '''
        consumer conf in redis
        {
            consumerID1:{
                "mountPoint":/home/suyi/consumer1,...,
                "extraDevicesList":[
                    {
                        "localDeviceMap":"/dev/sdc",
                        "remoteLV":"removeLV",
                        "groupName":"groupName",
                        "remoteVG":"groupName"+"VG",
                        "remoteLVPath":"/dev/"+"remoteVG"+"/"+"remoteLV"
                        "remoteSize":"size",
                        "remoteTid":"remoteTid",
                        "remoteIQN":"remoteIQN",
                    },
                ]
            }
        }
        '''
        self.setConfig(self.comsumerConfKey,json.dumps(conf))
    def getConsumerConf(self):
        confJson = self.getConfig(self.comsumerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf

    def getAvailTid(self):
        '''
        availTid in redis
        {
            deviceIP:tid,
        }
        '''
        atidJson = self.getConfig(self.availTidKey)
        atid = json.loads(atidJson)
        return atid
    def setAvailTid(self,atid):
        atidJson = json.dumps(atid)
        self.setConfig(self.availTidKey,atidJson)

    def getUserBookingTable(self):
        '''
        user booking table
        {
            user:{groupName:{timeslot1:1111,
                             timeslot2:2222}
                 }
        }
        '''
        userBookingJson = self.getConfig(self.userBookingKey)
        userBooking = json.loads(userBookingJson)
        return userBooking
    def setUserBookingTable(self,userBooking):
        self.setConfig(self.userBookingKey, json.dumps(userBooking))

    def getTimeSlotBookingTable(self):
        '''
        timeslot booking table
        {
            groupName:{timeslot1: available Space,
                       timeslot2: available Space,}
        }
        '''
        timeslotBookingJson = self.getConfig(self.timeslotBookingKey)
        timeslotBooking = json.loads(timeslotBookingJson)
        return timeslotBooking
    def setTimeSlotBookingTable(self, timeslotBooking):
        timeslotBookingJson = json.dumps(timeslotBooking)
        self.setConfig(self.timeslotBookingkey, timeslotBookingJson)

    def getReleaseCandidates(self):
        '''
        release Candidates list
        {
            consumerIP1:space
            consumerIP2:space
        }
        '''
        releaseCandidatesJson = self.getConfig(self.releaseCandidatesKey)
        releaseCandidates = json.loads(releaseCandidatesJson)
        return releaseCandidates
    def setReleaseCandidates(self, releaseCandidates):
        releaseCandidatesJson = json.dumps(releaseCandidates)
        self.setConfig(self.releaseCandidatesKey, releaseCandidatesJson)

    def getTagsManager(self):
        '''
        {
            groupName:[tag1,tag2],
            groupName:[tag2,tag3]
        }
        '''
        tagsManagerJson = self.getConfig(self.tagsManagerKey)
        tagsManager = json.loads(tagsManagerJson)
        return tagsManager
    def setTagsManager(self, tagsManager):
        tagsManagerJson = json.dumps(tagsManager)
        self.setConfig(self.tagsManagerKey, tagsManagerJson)


if __name__ == '__main__':
    ipInfoC = "127.0.0.1"
    portInfoC = 6379
    cHelper = configHelper(ipInfoC, portInfoC)
