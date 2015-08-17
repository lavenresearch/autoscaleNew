from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os
import json
import time

def executeCmd(cmd):
    logger = autoscaleLog(__file__)
    print cmd
    logger.writeLog(cmd)
    output = os.popen(cmd).read()
    print output
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    logger = autoscaleLog(__file__)
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    usersBooking = cHelper.getUserBookingTable()
    print usersBooking
    tagManager = cHelper.getTagsManager()
    userName = unicode(arg[0],'utf-8')
    print userName
    userBooking = usersBooking.get(userName)
    print userBooking
    userBookingRecords = []
    if userBooking == None:
        print json.dumps(userBookingRecords)
        return userBookingRecords
    for group, bookingTable in userBooking.items():
        tags = tagManager.get(group)
        userBookingForGroup = userBooking.get(group)
        timestamps = []
        for t in  userBookingForGroup.keys():
            timestamps.append(int(t))
        timestamps.sort()
        print timestamps
        try:
            bookingRecord = {}
            startT = timestamps[0]
            startS = userBookingForGroup.get(str(startT))
            endT = None
            for i in xrange(len(timestamps)):
                middleT = timestamps[i]
                endT = middleT
                middleS = userBookingForGroup.get(str(middleT))
                print middleT, middleS, timestamps[i+1]
                print endT
                print middleT != (timestamps[i+1]-1)
                print middleS != userBookingForGroup.get(str(timestamps[i+1]))
                print (middleT != (timestamps[i+1]-1)) or (middleS != userBookingForGroup.get(str(timestamps[i+1])))
                if (middleT != (timestamps[i+1]-1)) or (middleS != userBookingForGroup.get(str(timestamps[i+1]))):
                    bookingRecord["StartTime"]=time.ctime(startT*3600)
                    bookingRecord["EndTime"]=time.ctime(endT*3600+3600)
                    bookingRecord["Size"]="%s MB"%(str(startS))
                    bookingRecord["User"]=userName
                    bookingRecord["Tag1"]=tags[0]
                    bookingRecord["Tag2"]=tags[1]
                    userBookingRecords.append(bookingRecord)
                    bookingRecord = {}
                    startT = timestamps[i+1]
                    startS = userBookingForGroup.get(str(startT))
        except:
            bookingRecord["StartTime"]=time.ctime(startT*3600)
            bookingRecord["EndTime"]=time.ctime(endT*3600+3600)
            bookingRecord["Size"]="%s MB"%(str(startS))
            bookingRecord["User"]=userName
            bookingRecord["Tag1"]=tags[0]
            bookingRecord["Tag2"]=tags[1]
            userBookingRecords.append(bookingRecord)
            print json.dumps(userBookingRecords)
            return userBookingRecords
    print json.dumps(userBookingRecords)
    return userBookingRecords

if __name__ == '__main__':
    run(["user1"])
