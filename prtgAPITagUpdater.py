import sys
import csv
import os
import urllib2
import re
import time
import xml.etree.ElementTree as ET

os.getcwd()
os.chdir('/tmp')

def updateTag(sensorId, tags):
    buildUrl = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', sensorId, '&name=tags&value=', tags, '&username=api_update&passhash=4150398368')
    buildUrlStr = ''.join(buildUrl)
    request = urllib2.Request(buildUrlStr)
    response = urllib2.urlopen(request).read()
    print buildUrlStr, response


with open('prtgapitest-tonn.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        updateTag(row[0], row[2])

