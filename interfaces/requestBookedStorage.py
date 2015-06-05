from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
from interfaces import getUsageInfo
from interfaces import releaseExtraStorage
import sys,os,time

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
    consumerLocation = arg[1]
    stepSize = arg[2]
    tagList = arg[3:]
    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        return False
    groupName = groupList[0]
    currentTime = time.time()
    ctKey = currentTime/3600
    userBooking = cHelper.getUserBookingTable()
    userBookingForUser = userBooking.get(userName)
    if userBookingForUser == None:
        print "User did not book any storage"
        return False
    userBookingForUserForGroup = userBookingForUser.get(groupName)
    if userBookingForUserForGroup == None:
        print "User did not book storage for "+str(tagList)
        return False
    bookedStorageSize = userBookingForUserForGroup.get(ctKey)
    if bookedStorageSize == None:
        print "User did not book storage for this period"
        return False
    if bookedStorageSize < stepSize:
        print "User do not have enough booked storage space"
        return False

    # check current available space, if not enough , release

    currentUsageInfo = getUsageInfo.run([])
    asize = currentUsageInfo.get(groupName).get('groupSize')
    neededSize = 0
    if stepSize > asize:
        neededSize = stepSize - asize
    if neededSize > 0:
        releaseConsumerList = []
        releaseCandidates = cHelper.getReleaseCandidates()
        for deviceMapConsumerIP,size in releaseCandidates.items():
            neededSize = neededSize - size
            releaseConsumerList.append(deviceMapConsumerIP)
            if neededSize <= 0:
                break
        if neededSize > 0:
            print "Do not have enough space sorry"
            return False
        # release consumers
        for deviceMapConsumerIP in releaseConsumerList:
            deviceMap, consumerIP = deviceMapConsumerIP.split("@")
            releaseExtraStorage.run([consumerIP,deviceMap])

    requestStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py requestStorage "+groupName+" "+str(stepSize)+"\""
    executedCmd(requestStorageCmd)

    userBookingForUserForGroup[ctKey] = bookedStorageSize - stepSize
    cHelper.setUserBookingTable(userBooking)
    print "get booked storage succeded"
    return True


if __name__ == '__main__':
    run(sys.argv[1:])
