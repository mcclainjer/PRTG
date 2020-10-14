import sys
import csv
import os
import urllib2
import re
import time

os.getcwd()
os.chdir('/tmp')

sensorId = 0

def submitUrl(buildNewName, targetId, cloneId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/duplicateobject.htm?id=', cloneId, '&name=', buildNewName, '&targetid=', targetId, '&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).geturl()
    newSensorId = re.search('id%3D(\d+)', response)
    global sensorId
    sensorId = newSensorId.group(1)
    print 'duplicating sensor'

def submitUrl2(sensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/pause.htm?id=', sensorId, '&action=1&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print 'starting sensor'

def submitUrl3(stackValueSensorId, stackValueCompareSensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/getobjectstatus.htm?id=', stackValueSensorId, '&name=status&show=text&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    status = re.search('\<result\>(\w+)', response)
    statusStr = status.group(1)
    print 'checking status'
    while statusStr != 'Up':
        request = urllib2.Request(buildUrlStr)
        response = urllib2.urlopen(request).read()
        print response
        status = re.search('\<result\>(\w+)', response)
        statusStr = status.group(1)
        time.sleep(2)
        pass
    print 'sensor is up'
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=channels&output=xml&columns=name,lastvalue_&id=', stackValueSensorId, '&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    sensor = re.search('\<lastvalue\>(\w+)', response)
    sensorVal = sensor.group(1)
    print sensorVal
    buildUrl = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', stackValueCompareSensorId, '&name=includemust&value=', sensorVal, '&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print response


def submitUrl4(stackValueCompareSensorId):
    buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=channels&output=xml&columns=name,lastvalue_&id=', stackValueSensorId, '&username=api_update&passhash=4150398368&count=10000')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    sensor = re.search('\<lastvalue\>(\w+)', response)
    sensorVal = status.group(1)


with open('prtgapitest.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        targetId = row[1]
        targetName = row[0]
        print targetName
        newName = (row[0], ' - Stack Value')
        cloneId = '10205'
        buildNewName = ''.join(newName)
        submitUrl(buildNewName, targetId, cloneId)
        stackValueSensorId = sensorId
        submitUrl2(sensorId)
        time.sleep(1)
        newName = (row[0], ' - Stack Value Compare')
        cloneId = '10206'
        buildNewName = ''.join(newName)
        submitUrl(buildNewName, targetId, cloneId)
        stackValueCompareSensorId = sensorId
        submitUrl2(sensorId)
        time.sleep(1)
        submitUrl3(stackValueSensorId, stackValueCompareSensorId)



https://prtg.oc.unlv.edu/api/table.xml?content=sensors&output=csvtable&columns=objid,name&id=10168&username=api_update&passhash=4150398368
