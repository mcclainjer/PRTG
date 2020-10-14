import sys
import csv
import os
import urllib2
import re
import time
import xml.etree.ElementTree as ET

os.getcwd()
os.chdir('/tmp')

sensorId = 0
deviceRoot = ''
grpIdList = []
devIdList = []
sensIdList = []
workingDevId = None
sensorClonesDict = {'1':'12261', '2':'12254', '3':'12260', '4':'12262', '5':'12259', '6':'12263'}

def getAllDevs():
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=devices&output=xml&columns=objid,name&action=1&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    groupRoot = ET.fromstring(response)
    global allDevDict
    allDevDict = {item.find('name').text:item.find('objid').text for item in groupRoot.iter('item')}

def findDev(devName):
    global workingDevId
    workingDevId = allDevDict.get(devName)


def cloneUrl(cloneId, sensorNameNew, targetId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/duplicateobject.htm?id=', cloneId, '&name=', sensorNameNew, '&targetid=', targetId, '&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).geturl()
    newSensorId = re.search('id%3D(\d+)', response)
    global sensorId
    sensorId = newSensorId.group(1)
    print 'duplicating sensor'

def startUrl(sensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/pause.htm?id=', sensorId, '&action=1&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print 'starting sensor'

def scanUrl(sensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/scannow.htm?id=', sensorId, '&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print 'initiating scan'

def tagUrl(sensorId, newTag):
    receive = ('https://prtg.oc.unlv.edu/api/getobjectproperty.htm?id=', sensorId, '&name=tags', '&username=api_update&passhash=4150398368')
    buildReceiveUrl = ''.join(receive)
    receiveRequest = urllib2.Request(buildReceiveUrl)
    receiveResponse = urllib2.urlopen(receiveRequest).read()
    tags = re.search('\<result\>([ -,a-zA-Z0-9]+)', receiveResponse)
    tagsList = str.split(tags.group(1))
    print tagsList
    tagsStr = ','.join(tagsList)
    newTagsStr = (newTag, ',', tagsStr)
    buildNewTagsStr = ''.join(newTagsStr)
    print buildNewTagsStr
    send = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', sensorId, '&name=tags&value=', buildNewTagsStr, '&username=api_update&passhash=4150398368')
    buildSendUrl = ''.join(send)
    print buildSendUrl
    sendRequest = urllib2.Request(buildSendUrl)
    sendResponse = urllib2.urlopen(sendRequest).read()
    print 'tagging', sendResponse

with open('all-devices-3.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print 'starting ' + row[0]
        findDev(row[0])
        if workingDevId == None:
            print 'Not Found',row[0],row[1]
        else:
            pass
        if re.search('\d+', row[1]):  
            supplyNum = re.search('\d+', row[1])
            sensorNameNew = (row[0], ' - System Health Power Supplies')
            buildSensorNewName = ''.join(sensorNameNew)
            cloneId = sensorClonesDict.get(supplyNum.group())
            cloneUrl(cloneId, buildSensorNewName, workingDevId)
            startUrl(sensorId)
            scanUrl(sensorId)
        else:
            pass
        print 'finished ',supplyNum.group(),workingDevId,row[0]

