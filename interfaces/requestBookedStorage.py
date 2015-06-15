from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils.groupChooser import groupChooser
from utils.timeManager import timeManager
from interfaces import getUsageInfo
from interfaces import releaseExtraStorage
from utils.codecSwitcher import codecSwitcher
from utils.executeCmd import executeCmdSp
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
    consumerLocation = arg[1]
    stepSize = int(arg[2])
    tagList = cswitcher.getEncode(arg[3:])
    gchooser = groupChooser()
    groupList = gchooser.chooseGroup(tagList)
    if groupList == []:
        print "No storage resource available"
        return False
    groupName = groupList[0]
    # currentTime = time.time()
    timeM = timeManager()
    currentTime = timeM.getTime()
    # print "currentTime"
    # print currentTime
    ctKey = str(currentTime/3600)
    # print "ctKey"
    # print ctKey
    userBooking = cHelper.getUserBookingTable()
    # print "userBooking GET"
    # print userBooking
    userBookingForUser = userBooking.get(userName)
    # print "userBookingForUser"
    # print userBookingForUser
    if userBookingForUser == None:
        print "User did not book any storage"
        return False
    userBookingForUserForGroup = userBookingForUser.get(groupName)
    # print "userBookingForUserForGroup"
    # print userBookingForUserForGroup
    if userBookingForUserForGroup == None:
        print "User did not book storage for "+str(tagList)
        return False
    bookedStorageSize = userBookingForUserForGroup.get(ctKey)
    # print "bookedStorageSize"
    # print bookedStorageSize
    if bookedStorageSize == None:
        print "User did not book storage for this period"
        return False
    bookedStorageSize = int(bookedStorageSize)
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

    requestStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py requestStorage "+groupName+" "+str(stepSize)+" booked\""
    print requestStorageCmd
    executedCmd(requestStorageCmd)

    userBookingForUserForGroup[ctKey] = bookedStorageSize - stepSize
    cHelper.setUserBookingTable(userBooking)
    print "get booked storage succeded"
    return True


if __name__ == '__main__':
    run(sys.argv[1:])
