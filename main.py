import sys
from operations.startProvider import startProvider
from operations.extendGroup import extendGroup
from operations.requestStorage import requestStorage
from operations.releaseStorage import releaseStorage
from operations.startConsumer import startConsumer
from operations.deleteGroup import deleteGroup
from operations.clearGroup import clearGroup
from operations.stopProvider import stopProvider
from test.testAll import testAll

from interfaces import createGroup, addDeviceToGroup, addStorageConsumer, requestExtraStorage, releaseExtraStorage, getInfo, getUsageInfo, bookStorage, requestBookedStorage, getUserConsumers, clearGroupInterface, deleteGroupInterface, getProviderInfo, removeStorageConsumer,getUserBookingInfo

from utils.deployALL import deployALL
from utils import updateAll, breakAll, timeManager, collectProviderInfo, viewer

ops = ["startProvider","extendGroup","releaseStorage","requestStorage","startConsumer","deleteGroup","clearGroup","stopProvider"]
ifs = ["createGroup", "addDeviceToGroup", "addStorageConsumer", "requestExtraStorage", "releaseExtraStorage", "getInfo", "getUsageInfo", "bookStorage", "requestBookedStorage", "getUserConsumers", "clearGroupInterface", "deleteGroupInterface","getProviderInfo", "removeStorageConsumer","getUserBookingInfo"]

if __name__ == '__main__':
    prefix = "operations."
    moduleName = sys.argv[1]
   # print moduleName
    if moduleName in ops:
       # print "in ops"
        operation = globals()[moduleName]
        op = operation(sys.argv[2:])
        # op = operationa(*args, **kwargs)
        op.run()
        sys.exit(0)
    if moduleName in ifs:
        #print "in ifs"
        interface = globals()[moduleName]
        interface.run(sys.argv[2:])
        sys.exit(0)
    if moduleName == "deployALL":
        print "in deployALL"
        operation = globals()[moduleName]
        op = operation(sys.argv[2:])
        op.run()
        sys.exit(0)
    if moduleName == "updateAll":
        print "in updateAll"
        operation = globals()[moduleName]
        operation.run()
        sys.exit(0)
    if moduleName == "breakAll":
        print "in breakAll"
        operation = globals()[moduleName]
        operation.run()
        sys.exit(0)
    if moduleName == "timeManager":
        print "in timeManager"
        operation = globals()[moduleName]
        operation.run(sys.argv[2:])
        sys.exit(0)
    if moduleName == "testAll":
        print "in testAll"
        operation = globals()[moduleName]
        op = operation()
        op.run(sys.argv[2])
        sys.exit(0)
    if moduleName == "collectProviderInfo":
        print "in collectProviderInfo"
        operation = globals()[moduleName]
        op = operation.run()
        sys.exit(0)
    if moduleName == "viewer":
        print "in viewer"
        operation = globals()[moduleName]
        op = operation.run(sys.argv[2:])
        sys.exit(0)        
    print "do nothing"
    sys.exit(1)
