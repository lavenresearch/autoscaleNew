import sys

def getDevicesInfo():
    devices = []
    devicesDev = []
    dev_pattern = ['dm.*']
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                devices.append(device)
    for d in devices:
        dpathdev = "/dev/"+d.split("/")[-1]
        devicesDev.append(dpathdev)
    return devicesDev

def dmapper(devicepathDev):
    dpathdev = devicepathDev.split("/")
    if len(dpathdev) == 2:
        devicepathSys = "/sys/block/"+ devicepathDev.split("/").[-1]
        return devicepathSys
    if len(dpathdev) == 3:
    	
        
