from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
import sys,os

# Needed arguments including:
#
# userName : user1
# consumerIP : 192.168.16.121
# stepSize : 100 (in MB)
# tag1     : security
# tag2     : highSpeed
#
# For example:
#
# python requestBookedStorage.py user1 192.168.16.121 100 highSpeed security
#
# in which the "100" means 100MB

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
    logger.writeLog(arg)
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    userName = arg[0]
    stepSize = arg[1]
    startTime = arg[2]
    endTime = arg[3]
    tagList = arg[4:]
    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        return False
    groupName = groupList[0]
    res = gchooser.applyTimeslot(groupName,startTime,endTime,stepSize)
    if res == False:
        print "booking failed"
        return False

    # update user booking table

    userBooking = cHelper.getUserBookingTable()
    userBookingForUser = userBooking.get(userName)
    if userBookingForUser == None:
        userBookingForUser = {}
    userBookingForUserForGroup = userBookingForUser.get(groupName)
    if userBookingForUserForGroup == None:
        userBookingForUserForGroup = {}
    stKey = startTime/3600
    etKey = endTime/3600
    for t in xrange(stKey,etKey):
        s = userBookingForUserForGroup.get(t)
        if s == None:
            s = 0
        userBookingForUserForGroup[t] = s + size
    cHelper.setUserBookingTable(userBooking)
    print "booking succeded"
    return True

if __name__ == '__main__':
    run(sys.argv[1:])
