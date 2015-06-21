#coding=utf-8
import sys,time
from operations.extendGroup import extendGroup
from operations.requestStorage import requestStorage
from operations.releaseStorage import releaseStorage
from operations.startConsumer import startConsumer
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from utils import timeManager

from interfaces import createGroup, addDeviceToGroup, addStorageConsumer, requestExtraStorage, releaseExtraStorage, getInfo, getUsageInfo, bookStorage, requestBookedStorage

# PROCEDURE:
#
# createGroup: add group information to providerConf and groupMConf
# addStorageConsumer
# getInfo
# getUsageInfo
#
# addDeviceToGroup
# addDeviceToGroup
# getInfo
# getUsageInfo
#
# requestExtraStorage
# requestExtraStorage
# getInfo
# getUsageInfo
#
# releaseExtraStorage
# getInfo
# getUsageInfo
#
# ARRANGEMENT:
#
# de62: call web interface here
# de10: information center, groupManager
# ca01, de62: storage consumers
# ca32, ca07: storage providers(/dev/loop0, /dev/loop1)

class testAll():
    cgARG1 = ["high","tag1","tag2"]
    cgARG2 = ["low","tag3","tag4"]

    ascARG1 = ["user1","192.168.16.122"]
    ascARG2 = ["user2","192.168.16.124"]
    #ascARG2 = ["192.168.3.62"]

    adtgARG1 = ["192.168.0.98","/dev/raid21434548043/lvv1","high"]
    adtgARG2 = ["192.168.0.98","/dev/raid21434548043/lvv2","low"]
    #adtgARG3 = ["192.168.0.98","/dev/raid21434548043/cryptsource_lvv3","high"]
    adtgARG4 = ["192.168.0.98","/dev/raid21434548043/cryptsource_lvv4","low"]

    rqesARG1 = ["192.168.16.122","35000","tag1","tag2"]
    rqesARG2 = ["192.168.16.122","25000","tag3","tag4"]
    rqesARG3 = ["192.168.16.122","35000","tag1","tag2"]
    rqesARG4 = ["192.168.16.122","40000","tag5"]
    #rqesARG5 = ["192.168.16.123","low",500]

    bookStorageARG1 = ['user1',"50000","1434835582","1434845582",'tag1','tag2']
    bookStorageARG2 = ['user2',"60000","1434837582","1434855582",'tag2','tag2']

    rqbsARG1 = ['user1',"192.168.16.122","49000","tag1","tag2"]
    rqbsARG2 = ['user2',"192.168.16.124","59000","tag1","tag2"]

    # rlesARG1
    def __init__(self):
        print "Test Program Begins"

    def viewResult(self):
        getInfo.run([])
        getUsageInfo.run([])
        raw_input("press enter to continue:")

    def run(self, stepCode):
        print "Enter Test Procedure!\nstepCode:"+stepCode
        stepCode = int(stepCode)
        if stepCode <= 1:
            print "\n\n########################"
            print "createGroup 1"
            print "########################\n\n"
            createGroup.run(self.cgARG1)
            createGroup.run(self.cgARG2)
            self.viewResult()
        if stepCode <= 2:
            print "\n\n########################"
            print "addStorageConsumer 2"
            print "########################\n\n"
            addStorageConsumer.run(self.ascARG1)
            #addStorageConsumer.run(self.ascARG2)
            self.viewResult()
        if stepCode <= 3:
            print "\n\n########################"
            print "addDeviceToGroup 3"
            print "########################\n\n"
            addDeviceToGroup.run(self.adtgARG1)
            addDeviceToGroup.run(self.adtgARG2)
            #addDeviceToGroup.run(self.adtgARG3)
            addDeviceToGroup.run(self.adtgARG4)
            self.viewResult()
        if stepCode <= 4:
            print "\n\n########################"
            print "requestExtraStorage 4"
            print "########################\n\n"
            startT = time.clock()
            requestExtraStorage.run(self.rqesARG1)
            firstT = time.clock()
            requestExtraStorage.run(self.rqesARG2)
            secondT = time.clock()
            requestExtraStorage.run(self.rqesARG3)
            thirdT = time.clock()
            requestExtraStorage.run(self.rqesARG4)
            fourthT = time.clock()
            print startT
            print firstT
            print secondT
            print thirdT
            print fourthT
            #requestExtraStorage.run(self.rqesARG5)
            self.viewResult()
        if stepCode <= 5:
            print "\n\n########################"
            print "releaseExtraStorage 5"
            print "########################\n\n"
            for i in xrange(1):
                rlesARGcl = raw_input("consumerLocation:")
                rlesARGldm = raw_input("localDeviceMap:")
                releaseExtraStorage.run([rlesARGcl,rlesARGldm])
                self.viewResult()
        if stepCode <= 6:
            print "\n\n########################"
            print "bookStorage 6"
            print "#########################\n\n"
            timeManager.run("1434835582")
            print time.ctime(1434835582)
            bookStorage.run(self.bookStorageARG1)
            bookStorage.run(self.bookStorageARG2)
            self.viewResult()
            timeManager.run("1434838982")
            print time.ctime(1434838982)
        if stepCode <= 7:
            print "\n\n########################"
            print "requestBookedStorage 7"
            print "#########################\n\n"
            requestBookedStorage.run(self.rqbsARG1)
            requestBookedStorage.run(self.rqbsARG2)
            self.viewResult()
            
