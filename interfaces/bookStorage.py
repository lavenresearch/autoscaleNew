from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
from utils.codecSwitcher import codecSwitcher
from utils.executeCmd import executeCmdSp
import sys,os

# Needed arguments including:
#
# userName : user1
# stepSize : 100 (in MB)
# startTime: 111111111
# endTime  : 222222222
# tag1     : security
# tag2     : highSpeed
#
# For example:
#
# python bookStorage.py user1 100 1111111 2222222 highSpeed security
#
# in which the "100" means 100MB

def executeCmd(cmd):
    logger = autoscaleLog(__file__)
    print cmd
    logger.writeLog(cmd)
    #output = os.popen(cmd).read()
    output = executeCmdSp(cmd)
    print output
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    cswitcher = codecSwitcher()
    logger = autoscaleLog(__file__)
    logger.writeLog(arg)
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    userName = arg[0]
    stepSize = arg[1]
    startTime = int(arg[2])
    endTime = int(arg[3])
    #tagList = []
    #for a in arg[4:]:
    #    tagList.append(unicode(a))
    tagList = cswitcher.getEncode(arg[4:])
    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        print "failed1failed2failed"
        return False
    groupName = groupList[0]
    res = gchooser.applyTimeslot(groupName,startTime,endTime,stepSize)
    if res == False:
        print "Do not have enough space, booking failed"
        print "failed1failed2failed"
        return False

    # update user booking table

    userBooking = cHelper.getUserBookingTable()
    print userBooking
    userBookingForUser = userBooking.get(userName)
    if userBookingForUser == None:
        userBookingForUser = {}
    userBookingForUserForGroup = userBookingForUser.get(groupName)
    if userBookingForUserForGroup == None:
        userBookingForUserForGroup = {}
    stKey = startTime/3600
    etKey = endTime/3600
    for t in xrange(stKey,etKey):
        s = userBookingForUserForGroup.get(str(t))
        if s == None:
            s = 0
        userBookingForUserForGroup[str(t)] = s + int(stepSize)
    userBookingForUser[groupName] = userBookingForUserForGroup
    print userBookingForUserForGroup
    userBooking[userName] = userBookingForUser
    print userBookingForUser
    print userBooking
    cHelper.setUserBookingTable(userBooking)
    print "booking succeded"
    return True

if __name__ == '__main__':
    run(sys.argv[1:])
