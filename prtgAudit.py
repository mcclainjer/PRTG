#!/usr/bin/python

import sys
import os
import urllib2
import re
import datetime
import syslog
import xml.etree.cElementTree as ET

root = 'null'

# Here we get the entire XML provided by the PRTG API, this is equivalent to 'sensortree: A tree-like structure of groups, devices and sensors' from the API docu
buildUrl = ('https://prtg.oc.unlv.edu/api/table.xml?content=sensortree&output=xml&action=1&username=api_update&passhash=4150398368')
buildUrlStr = ''.join(buildUrl)
request = urllib2.Request(buildUrlStr)
response = urllib2.urlopen(request).read()
global root
root = ET.fromstring(response)

# Misc stuff, sets the destination directory and creates the filename
os.chdir('/var/log/prtg_audit')
curTime = datetime.datetime.now()
ctcurTime = datetime.datetime.strftime(curTime, '%Y%m%d-%H%M%S')
fileName = 'prtg' + ctcurTime + '.csv'

# More XML parsing hell.  We open a new file to write the CSV.  
# We start iterating from the root element down through the tree collecting variables as we go then write each line.
# If all goes well we write a confimation log to syslog with the filename.
try:
    with open(fileName, 'w') as f:
        for device in root.getiterator('device'):
            for child in device:
                if child.tag == 'name':
                    # print device.get('id'), child.text
                    devName = child.text
            for child in device:
                if child.tag == 'sensor':
                    for i in child:
                        if i.tag == 'id':
                            # print i.text
                            sensorId = i.text
                    for i in child:
                        if i.tag == 'name':
                            # print i.text
                            if re.search(',', i.text):
                                sensorName = re.sub(',', '', i.text)
                            else:
                                sensorName = i.text
                    for i in child:
                        if i.tag == 'tags':
                            # print i.text
                            sensorTags = i.text
                    # print sensorId, sensorName, sensorTags, device.get('id'), devName
                    # print device.get('id'), devName, sensorId, sensorName, sensorTags
                    f.write('{0},{1},{2},{3},{4}\n'.format(sensorId, sensorName, sensorTags, device.get('id'), devName))
        f.close()
        syslog.syslog('PRTG Auditor wrote file {0}'.format(fileName))
# What the heck, lets get all the exceptions
except Exception as e:
    syslog.syslog('PRTG Auditor caught exception \'{0}\''.format(e))