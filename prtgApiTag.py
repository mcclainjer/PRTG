import sys
import csv
import os

os.chdir('/tmp')

with open('prtgapitest.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        receive = ('https://prtg.oc.unlv.edu/api/getobjectproperty.htm?id=', row[0], '&name=tags', '&username=api_update&passhash=4150398368')
        buildReceiveUrl = ''.join(receive)
        receiveRequest = urllib2.Request(buildReceiveUrl)
        receiveResponse = urllib2.urlopen(receiveRequest).read()
        tags = re.search('\<result\>([ -,a-zA-Z0-9]+)', receiveResponse)
        tagsList = str.split(tags.group(1))
        print tagsList
        tagsStr = ','.join(tagsList)
        newTagsStr = (row[2], ',', tagsStr)
        buildNewTagsStr = ''.join(newTagsStr)
        print buildNewTagsStr
        send = ('https://prtg.oc.unlv.edu/api/setobjectproperty.htm?id=', row[0], '&name=tags&value=', buildNewTagsStr, '&username=api_update&passhash=4150398368')
        buildSendUrl = ''.join(send)
        sendRequest = urllib2.Request(buildSendUrl)
        try:
            sendResponse = urllib2.urlopen(sendRequest).read()
            print sendResponse
            outFile = open('outfile.csv', 'a')
            outFile.wrtie(sendResponse)
        except urllib2.URLError as e:
            print "Encountered an exception: {0}".format(e)
