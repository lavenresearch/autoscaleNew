from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys
import json

# Needed arguments including:
#
# groupName : highSpeedGroup

# For example:
#
# python createGroup.py highSpeedGroup tag1 tag2 tag3 ...

def run(arg):
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    groupName = arg[0]
    tagList = arg[1:]
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    providersConf = cHelper.getProviderConf()
    if providersConf.get(groupName) == None:
        # providersConf[groupName] = {"tags":tagList}
        providersConf[groupName] = {}
    else:
        print "group exist"
        sys.exit(1)
    logger.writeLog(providersConf)
    print json.dumps(providersConf)
    gmConf = cHelper.getGroupMConf()
    groupAmount = len(gmConf)
    if gmConf.get(groupName) == None:
        gmConf[groupName] = {}
        gmConf[groupName]["currentTid"] = 500+200*groupAmount
        gmConf[groupName]["gmIP"] = sConf.getGroupMIP()
        gmConf[groupName]["devicesLoaded"] = []
        gmConf[groupName]["consumersLoaded"] = []
    else:
        print "group exist"
        sys.exit(1)
    logger.writeLog(gmConf)
    print json.dumps(gmConf)
    tagsManager = cHelper.getTagsManager()
    if tagsManager.get(groupName) == None:
    	tagsManager[groupName] = tagList
    else:
        print "group exist"
        sys.exit(1)
    cHelper.setProviderConf(providersConf)
    cHelper.setGroupMConf(gmConf)
    cHelper.setTagsManager(tagsManager)
    logger.shutdownLog()

if __name__ == '__main__':
    groupName = sys.argv[1]
    tagList = sys.argv[2:]
    run([groupName,tagList])
