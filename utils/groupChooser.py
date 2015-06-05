from utils.autoScaleLog import autoscaleLog
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from interfaces import getUsageInfo

class groupChooser:
    logger = None
    sConf = None
    cHelper = None
    def __init__(self):
        self.logger = autoscaleLog(__file__)
        self.logger.writeLog(sys.argv)
        self.sConf = staticConfig()
        infoCLocation = sConf.getInfoCLocation()
        self.cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))

    def chooseGroup(self, tagList):
        tagsManager = self.cHelper.getTagsManager()
        groupList = []
        tagNum = len(tagList)
        for gname,tagsl in tagsManager.items():
            n = 0        
            for tag in tagList:
                if tag in tagsl:
                    n++
            if n == tagNum:
            groupList.append(gname)
        self.logger.writeLog(groupList)
        return groupList

    def applyTimeslot(self, groupName, startTime, endTime, size):
        stKey = startTime/3600
        etKey = endTime/3600
        usageInfo = getUsageInfo.run([])
        availableSpace = usageInfo[groupName].get('groupSize')
        if size > availableSpace:
            self.logger.writeLog("Booking resources failed, no enough space!")
            return False
        timeslotBooking = self.cHelper.getTimeSlotBookingTable()
        timeslotBookingForGroup = timeslotBooking.get(groupName)
        if timeslotBookingForGroup == None:
            timeslotBookingForGroup = {}
        for t in xrange(stKey,etKey):
            asize = timeslotBookingForGroup.get(t)
            if asize == None:
                asize = availableSpace
            if size > asize:
                self.logger.writeLog("Booking resources failed, no enough space!")
                return False
            timeslotBookingForGroup[t] = asize - size
        timeslotBooking[groupName] = timeslotBookingForGroup
        self.cHelper.setTimeSlotBookingTable(timeslotBooking)
        self.logger.writeLog("Booking resources successfully!")
        return True
        
